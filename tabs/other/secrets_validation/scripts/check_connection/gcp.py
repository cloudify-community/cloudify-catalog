import sys
import json
import math
import base64
import hashlib
import calendar
import datetime
import warnings
import threading

from io import StringIO
from pyasn1.codec.der import decoder  # type: ignore
from pyasn1_modules.rfc5208 import PrivateKeyInfo  # type: ignore
from pyasn1_modules import pem  # type: ignore

_PKCS1_MARKER = ("-----BEGIN RSA PRIVATE KEY-----", "-----END RSA PRIVATE KEY-----")
_PKCS8_MARKER = ("-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----")
_PKCS8_SPEC = PrivateKeyInfo()

try:
    from urllib import quote
    from urlparse import urlparse
except ImportError:
    from urllib.parse import quote, urlparse

import requests

from cloudify import ctx

HASH_ASN1 = {
    "MD5": b"\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10",
    "SHA-1": b"\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14",
    "SHA-224": b"\x30\x2d\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x04\x05\x00\x04\x1c",
    "SHA-256": b"\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20",
    "SHA-384": b"\x30\x41\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x02\x05\x00\x04\x30",
    "SHA-512": b"\x30\x51\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40",
}

HASH_METHODS = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-224": hashlib.sha224,
    "SHA-256": hashlib.sha256,
    "SHA-384": hashlib.sha384,
    "SHA-512": hashlib.sha512,
}

def yield_fixedblocks(infile, blocksize):
    while True:
        block = infile.read(blocksize)

        read_bytes = len(block)
        if read_bytes == 0:
            break

        yield block

        if read_bytes < blocksize:
            break


def compute_hash(message, method_name):
    if method_name not in HASH_METHODS:
        raise ValueError("Invalid hash method: %s" % method_name)

    method = HASH_METHODS[method_name]
    hasher = method()

    if isinstance(message, bytes):
        hasher.update(message)
    else:
        assert hasattr(message, "read") and hasattr(message.read, "__call__")
        # read as 1K blocks
        for block in yield_fixedblocks(message, 1024):
            hasher.update(block)

    return hasher.digest()


def bit_size(number):
    if hasattr(number, 'bit_length'):
        return number.bit_length()
    else:
        return len(number)


def ceil_div(num, div):
    quanta, mod = divmod(num, div)
    if mod:
        quanta += 1
    return quanta


def byte_size(number):
    if number == 0:
        return 1
    return ceil_div(bit_size(number), 8)


def _pad_for_signing(message, target_length):
    max_msglength = target_length - 11
    msglength = len(message)

    if msglength > max_msglength:
        raise OverflowError(
            "%i bytes needed for message, but there is only"
            " space for %i" % (msglength, max_msglength)
        )

    padding_length = target_length - msglength - 3

    return b"".join([b"\x00\x01", padding_length * b"\xff", b"\x00", message])


def int2bytes(number, fill_size):
    if number < 0:
        raise ValueError("Number must be an unsigned integer: %d" % number)

    bytes_required = max(1, math.ceil(number.bit_length() / 8))

    if fill_size > 0:
        return number.to_bytes(fill_size, "big")

    return number.to_bytes(bytes_required, "big")


def sign_hash(hash_value, private_key, hash_method):

    # Get the ASN1 code for this hash method
    if hash_method not in HASH_ASN1:
        raise ValueError("Invalid hash method: %s" % hash_method)
    asn1code = HASH_ASN1[hash_method]

    # Encrypt the hash with the private key
    cleartext = asn1code + hash_value
    keylength = 0
    if hasattr(private_key, 'n'):
        keylength = byte_size(private_key.n)
    else:
        keylength = byte_size(private_key)
    padded = _pad_for_signing(cleartext, keylength)

    payload = int.from_bytes(padded, "big", signed=False)
    encrypted = payload
    if hasattr(private_key, 'blinded_encrypt'):
        encrypted = private_key.blinded_encrypt(payload)
    block = int2bytes(encrypted, keylength)

    return block


def sign(message, private_key, hash_method):
    msg_hash = compute_hash(message, hash_method)
    return sign_hash(msg_hash, private_key, hash_method)


def encode(signer, payload, header=None, key_id=None):
    if header is None:
        header = {}

    if key_id is None:
        key_id = signer.key_id

    header.update({"typ": "JWT"})

    if "alg" not in header:
        header.update({"alg": "RS256"})

    if key_id is not None:
        header["kid"] = key_id

    segments = [
        base64.urlsafe_b64encode(json.dumps(header).encode("utf-8")).rstrip(b"="),
        base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")),
    ]

    signing_input = b".".join(segments)
    signature = signer.sign(signing_input)
    segments.append(base64.urlsafe_b64encode(signature))

    return b".".join(segments)


def extended_gcd(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb"""
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo original b
    if ly < 0:
        ly += oa  # If neg wrap modulo original a
    return a, lx, ly  # Return only positive values


class NotRelativePrimeError(ValueError):
    def __init__(self, a: int, b: int, d: int, msg: str = "") -> None:
        super().__init__(msg or "%d and %d are not relatively prime, divider=%i" % (a, b, d))
        self.a = a
        self.b = b
        self.d = d


def inverse(x, n):
    """Returns the inverse of x % n under multiplication, a.k.a x^-1 (mod n)
    >>> inverse(7, 4)
    3
    >>> (inverse(143, 4) * 143) % 4
    1
    """

    (divider, inv, _) = extended_gcd(x, n)

    if divider != 1:
        raise NotRelativePrimeError(x, n, divider)

    return inv

class AbstractKey:
    __slots__ = ("n", "e", "blindfac", "blindfac_inverse", "mutex")

    def __init__(self, n: int, e: int) -> None:
        self.n = n
        self.e = e

        # These will be computed properly on the first call to blind().
        self.blindfac = self.blindfac_inverse = -1

        # Used to protect updates to the blinding factor in multi-threaded
        # environments.
        self.mutex = threading.Lock()

    @classmethod
    def _load_pkcs1_pem(cls, keyfile):
        """Loads a key in PKCS#1 PEM format, implement in a subclass.
        :param keyfile: contents of a PEM-encoded file that contains
            the public key.
        :type keyfile: bytes
        :return: the loaded key
        :rtype: AbstractKey
        """

    @classmethod
    def _load_pkcs1_der(cls, keyfile):
        """Loads a key in PKCS#1 PEM format, implement in a subclass.
        :param keyfile: contents of a DER-encoded file that contains
            the public key.
        :type keyfile: bytes
        :return: the loaded key
        :rtype: AbstractKey
        """

    def _save_pkcs1_pem(self):
        """Saves the key in PKCS#1 PEM format, implement in a subclass.
        :returns: the PEM-encoded key.
        :rtype: bytes
        """

    def _save_pkcs1_der(self):
        """Saves the key in PKCS#1 DER format, implement in a subclass.
        :returns: the DER-encoded key.
        :rtype: bytes
        """

    @classmethod
    def load_pkcs1(cls, keyfile, format="PEM"):
        """Loads a key in PKCS#1 DER or PEM format.
        :param keyfile: contents of a DER- or PEM-encoded file that contains
            the key.
        :type keyfile: bytes
        :param format: the format of the file to load; 'PEM' or 'DER'
        :type format: str
        :return: the loaded key
        :rtype: AbstractKey
        """

        methods = {
            "PEM": cls._load_pkcs1_pem,
            "DER": cls._load_pkcs1_der,
        }

        method = cls._assert_format_exists(format, methods)
        return method(keyfile)

    @staticmethod
    def _assert_format_exists(file_format, methods):
        """Checks whether the given file format exists in 'methods'."""

        try:
            return methods[file_format]
        except KeyError as ex:
            formats = ", ".join(sorted(methods.keys()))
            raise ValueError(
                "Unsupported format: %r, try one of %s" % (file_format, formats)
            ) from ex

    def save_pkcs1(self, format="PEM"):
        """Saves the key in PKCS#1 DER or PEM format.
        :param format: the format to save; 'PEM' or 'DER'
        :type format: str
        :returns: the DER- or PEM-encoded key.
        :rtype: bytes
        """

        methods = {
            "PEM": self._save_pkcs1_pem,
            "DER": self._save_pkcs1_der,
        }

        method = self._assert_format_exists(format, methods)
        return method()

    def blind(self, message):
        """Performs blinding on the message.
        :param message: the message, as integer, to blind.
        :param r: the random number to blind with.
        :return: tuple (the blinded message, the inverse of the used blinding factor)
        The blinding is such that message = unblind(decrypt(blind(encrypt(message))).
        See https://en.wikipedia.org/wiki/Blinding_%28cryptography%29
        """
        blindfac, blindfac_inverse = self._update_blinding_factor()
        blinded = (message * pow(blindfac, self.e, self.n)) % self.n
        return blinded, blindfac_inverse

    def unblind(self, blinded, blindfac_inverse):
        """Performs blinding on the message using random number 'blindfac_inverse'.
        :param blinded: the blinded message, as integer, to unblind.
        :param blindfac: the factor to unblind with.
        :return: the original message.
        The blinding is such that message = unblind(decrypt(blind(encrypt(message))).
        See https://en.wikipedia.org/wiki/Blinding_%28cryptography%29
        """
        return (blindfac_inverse * blinded) % self.n

    def _initial_blinding_factor(self):
        for _ in range(1000):
            blind_r = rsa.randnum.randint(self.n - 1)
            if rsa.prime.are_relatively_prime(self.n, blind_r):
                return blind_r
        raise RuntimeError("unable to find blinding factor")

    def _update_blinding_factor(self):
        """Update blinding factors.
        Computing a blinding factor is expensive, so instead this function
        does this once, then updates the blinding factor as per section 9
        of 'A Timing Attack against RSA with the Chinese Remainder Theorem'
        by Werner Schindler.
        See https://tls.mbed.org/public/WSchindler-RSA_Timing_Attack.pdf
        :return: the new blinding factor and its inverse.
        """

        with self.mutex:
            if self.blindfac < 0:
                # Compute initial blinding factor, which is rather slow to do.
                self.blindfac = self._initial_blinding_factor()
                self.blindfac_inverse = inverse(self.blindfac, self.n)
            else:
                # Reuse previous blinding factor.
                self.blindfac = pow(self.blindfac, 2, self.n)
                self.blindfac_inverse = pow(self.blindfac_inverse, 2, self.n)

            return self.blindfac, self.blindfac_inverse


def assert_int(var, name):
    if isinstance(var, int):
        return

    raise TypeError("%s should be an integer, not %s" % (name, var.__class__))


def encrypt_int(message, ekey, n):
    """Encrypts a message using encryption key 'ekey', working modulo n"""

    assert_int(message, "message")
    assert_int(ekey, "ekey")
    assert_int(n, "n")

    if message < 0:
        raise ValueError("Only non-negative numbers are supported")

    if message > n:
        raise OverflowError("The message %i is too long for n=%i" % (message, n))

    return pow(message, ekey, n)


def _markers(pem_marker):
    """
    Returns the start and end PEM markers, as bytes.
    """

    if not isinstance(pem_marker, bytes):
        pem_marker = pem_marker.encode("ascii")

    return (
        b"-----BEGIN " + pem_marker + b"-----",
        b"-----END " + pem_marker + b"-----",
    )


def _pem_lines(contents, pem_start, pem_end):
    """Generator over PEM lines between pem_start and pem_end."""

    in_pem_part = False
    seen_pem_start = False

    for line in contents.splitlines():
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Handle start marker
        if line == pem_start:
            if in_pem_part:
                raise ValueError('Seen start marker "%r" twice' % pem_start)

            in_pem_part = True
            seen_pem_start = True
            continue

        # Skip stuff before first marker
        if not in_pem_part:
            continue

        # Handle end marker
        if in_pem_part and line == pem_end:
            in_pem_part = False
            break

        # Load fields
        if b":" in line:
            continue

        yield line

    # Do some sanity checks
    if not seen_pem_start:
        raise ValueError('No PEM start marker "%r" found' % pem_start)

    if in_pem_part:
        raise ValueError('No PEM end marker "%r" found' % pem_end)


def load_pem(contents, pem_marker):
    """Loads a PEM file.
    :param contents: the contents of the file to interpret
    :param pem_marker: the marker of the PEM content, such as 'RSA PRIVATE KEY'
        when your file has '-----BEGIN RSA PRIVATE KEY-----' and
        '-----END RSA PRIVATE KEY-----' markers.
    :return: the base64-decoded content between the start and end markers.
    @raise ValueError: when the content is invalid, for example when the start
        marker cannot be found.
    """

    # We want bytes, not text. If it's text, it can be converted to ASCII bytes.
    if not isinstance(contents, bytes):
        contents = contents.encode("ascii")

    (pem_start, pem_end) = _markers(pem_marker)
    pem_lines = [line for line in _pem_lines(contents, pem_start, pem_end)]

    # Base64-decode the contents
    pem = b"".join(pem_lines)
    return base64.standard_b64decode(pem)


def save_pem(contents, pem_marker):
    """Saves a PEM file.
    :param contents: the contents to encode in PEM format
    :param pem_marker: the marker of the PEM content, such as 'RSA PRIVATE KEY'
        when your file has '-----BEGIN RSA PRIVATE KEY-----' and
        '-----END RSA PRIVATE KEY-----' markers.
    :return: the base64-encoded content between the start and end markers, as bytes.
    """

    (pem_start, pem_end) = _markers(pem_marker)

    b64 = base64.standard_b64encode(contents).replace(b"\n", b"")
    pem_lines = [pem_start]

    for block_start in range(0, len(b64), 64):
        block = b64[block_start : block_start + 64]
        pem_lines.append(block)

    pem_lines.append(pem_end)
    pem_lines.append(b"")

    return b"\n".join(pem_lines)


class PrivateKey(AbstractKey):
    """Represents a private RSA key.
    This key is also known as the 'decryption key'. It contains the 'n', 'e',
    'd', 'p', 'q' and other values.
    Supports attributes as well as dictionary-like access. Attribute access is
    faster, though.
    >>> PrivateKey(3247, 65537, 833, 191, 17)
    PrivateKey(3247, 65537, 833, 191, 17)
    exp1, exp2 and coef will be calculated:
    >>> pk = PrivateKey(3727264081, 65537, 3349121513, 65063, 57287)
    >>> pk.exp1
    55063
    >>> pk.exp2
    10095
    >>> pk.coef
    50797
    """

    __slots__ = ("d", "p", "q", "exp1", "exp2", "coef")

    def __init__(self, n, e, d, p, q):
        AbstractKey.__init__(self, n, e)
        self.d = d
        self.p = p
        self.q = q

        # Calculate exponents and coefficient.
        self.exp1 = int(d % (p - 1))
        self.exp2 = int(d % (q - 1))
        self.coef = inverse(q, p)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return "PrivateKey(%i, %i, %i, %i, %i)" % (
            self.n,
            self.e,
            self.d,
            self.p,
            self.q,
        )

    def __getstate__(self):
        """Returns the key as tuple for pickling."""
        return self.n, self.e, self.d, self.p, self.q, self.exp1, self.exp2, self.coef

    def __setstate__(self, state):
        """Sets the key from tuple."""
        self.n, self.e, self.d, self.p, self.q, self.exp1, self.exp2, self.coef = state
        AbstractKey.__init__(self, self.n, self.e)

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, PrivateKey):
            return False

        return (
            self.n == other.n
            and self.e == other.e
            and self.d == other.d
            and self.p == other.p
            and self.q == other.q
            and self.exp1 == other.exp1
            and self.exp2 == other.exp2
            and self.coef == other.coef
        )

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.n, self.e, self.d, self.p, self.q, self.exp1, self.exp2, self.coef))

    def blinded_decrypt(self, encrypted):
        """Decrypts the message using blinding to prevent side-channel attacks.
        :param encrypted: the encrypted message
        :type encrypted: int
        :returns: the decrypted message
        :rtype: int
        """

        # Blinding and un-blinding should be using the same factor
        blinded, blindfac_inverse = self.blind(encrypted)

        # Instead of using the core functionality, use the Chinese Remainder
        # Theorem and be 2-4x faster. This the same as:
        #
        # decrypted = rsa.core.decrypt_int(blinded, self.d, self.n)
        s1 = pow(blinded, self.exp1, self.p)
        s2 = pow(blinded, self.exp2, self.q)
        h = ((s1 - s2) * self.coef) % self.p
        decrypted = s2 + self.q * h

        return self.unblind(decrypted, blindfac_inverse)

    def blinded_encrypt(self, message):
        """Encrypts the message using blinding to prevent side-channel attacks.
        :param message: the message to encrypt
        :type message: int
        :returns: the encrypted message
        :rtype: int
        """

        blinded, blindfac_inverse = self.blind(message)
        encrypted = encrypt_int(blinded, self.d, self.n)
        return self.unblind(encrypted, blindfac_inverse)

    @classmethod
    def _load_pkcs1_der(cls, keyfile):
        """Loads a key in PKCS#1 DER format.
        :param keyfile: contents of a DER-encoded file that contains the private
            key.
        :type keyfile: bytes
        :return: a PrivateKey object
        First let's construct a DER encoded key:
        >>> import base64
        >>> b64der = 'MC4CAQACBQDeKYlRAgMBAAECBQDHn4npAgMA/icCAwDfxwIDANcXAgInbwIDAMZt'
        >>> der = base64.standard_b64decode(b64der)
        This loads the file:
        >>> PrivateKey._load_pkcs1_der(der)
        PrivateKey(3727264081, 65537, 3349121513, 65063, 57287)
        """

        from pyasn1.codec.der import decoder

        (priv, _) = decoder.decode(keyfile)

        # ASN.1 contents of DER encoded private key:
        #
        # RSAPrivateKey ::= SEQUENCE {
        #     version           Version,
        #     modulus           INTEGER,  -- n
        #     publicExponent    INTEGER,  -- e
        #     privateExponent   INTEGER,  -- d
        #     prime1            INTEGER,  -- p
        #     prime2            INTEGER,  -- q
        #     exponent1         INTEGER,  -- d mod (p-1)
        #     exponent2         INTEGER,  -- d mod (q-1)
        #     coefficient       INTEGER,  -- (inverse of q) mod p
        #     otherPrimeInfos   OtherPrimeInfos OPTIONAL
        # }

        if priv[0] != 0:
            raise ValueError("Unable to read this file, version %s != 0" % priv[0])

        as_ints = map(int, priv[1:6])
        key = cls(*as_ints)

        exp1, exp2, coef = map(int, priv[6:9])

        if (key.exp1, key.exp2, key.coef) != (exp1, exp2, coef):
            warnings.warn(
                "You have provided a malformed keyfile. Either the exponents "
                "or the coefficient are incorrect. Using the correct values "
                "instead.",
                UserWarning,
            )

        return key

    def _save_pkcs1_der(self) -> bytes:
        """Saves the private key in PKCS#1 DER format.
        :returns: the DER-encoded private key.
        :rtype: bytes
        """

        from pyasn1.type import univ, namedtype
        from pyasn1.codec.der import encoder

        class AsnPrivKey(univ.Sequence):
            componentType = namedtype.NamedTypes(
                namedtype.NamedType("version", univ.Integer()),
                namedtype.NamedType("modulus", univ.Integer()),
                namedtype.NamedType("publicExponent", univ.Integer()),
                namedtype.NamedType("privateExponent", univ.Integer()),
                namedtype.NamedType("prime1", univ.Integer()),
                namedtype.NamedType("prime2", univ.Integer()),
                namedtype.NamedType("exponent1", univ.Integer()),
                namedtype.NamedType("exponent2", univ.Integer()),
                namedtype.NamedType("coefficient", univ.Integer()),
            )

        # Create the ASN object
        asn_key = AsnPrivKey()
        asn_key.setComponentByName("version", 0)
        asn_key.setComponentByName("modulus", self.n)
        asn_key.setComponentByName("publicExponent", self.e)
        asn_key.setComponentByName("privateExponent", self.d)
        asn_key.setComponentByName("prime1", self.p)
        asn_key.setComponentByName("prime2", self.q)
        asn_key.setComponentByName("exponent1", self.exp1)
        asn_key.setComponentByName("exponent2", self.exp2)
        asn_key.setComponentByName("coefficient", self.coef)

        return encoder.encode(asn_key)

    @classmethod
    def _load_pkcs1_pem(cls, keyfile):
        """Loads a PKCS#1 PEM-encoded private key file.
        The contents of the file before the "-----BEGIN RSA PRIVATE KEY-----" and
        after the "-----END RSA PRIVATE KEY-----" lines is ignored.
        :param keyfile: contents of a PEM-encoded file that contains the private
            key.
        :type keyfile: bytes
        :return: a PrivateKey object
        """

        der = load_pem(keyfile, b"RSA PRIVATE KEY")
        return cls._load_pkcs1_der(der)

    def _save_pkcs1_pem(self) -> bytes:
        """Saves a PKCS#1 PEM-encoded private key file.
        :return: contents of a PEM-encoded file that contains the private key.
        :rtype: bytes
        """

        der = self._save_pkcs1_der()
        return save_pem(der, b"RSA PRIVATE KEY")

class RSASigner(object):

    def __init__(self, private_key, key_id=None):
        self._key = private_key
        self._key_id = key_id

    @property  # type: ignore
    def key_id(self):
        return self._key_id

    def sign(self, message):
        if hasattr(message, 'encode'):
            message = message.encode('utf-8')
        return sign(message, self._key, "SHA-256")

    @classmethod
    def from_string(cls, key, key_id=None):
        key = key.decode("utf-8")
        marker_id, key_bytes = pem.readPemBlocksFromFile(
            StringIO(key), _PKCS1_MARKER, _PKCS8_MARKER
        )

        # Key is in pkcs1 format.
        if marker_id == 0:
            private_key = PrivateKey.load_pkcs1(key_bytes, format="DER")
        # Key is in pkcs8.
        elif marker_id == 1:
            key_info, remaining = decoder.decode(key_bytes, asn1Spec=_PKCS8_SPEC)
            if remaining != b"":
                raise Exception("Unused bytes", remaining)
            private_key_info = key_info.getComponentByName("privateKey")
            private_key = PrivateKey.load_pkcs1(
                private_key_info.asOctets(), format="DER"
            )
        else:
            raise Exception("No key could be detected.")

        return cls(private_key, key_id=key_id)


def get_bearer_token(jwt_token):
    url = "https://www.googleapis.com/oauth2/v4/token"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer".encode('utf-8'),
        "assertion": jwt_token
    }
    ctx.logger.info('data {0}'.format(data))
    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.json()


def list_machine_types(token, project_id):
    url = "https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/us-west1-a/machineTypes".format(
            project_id = project_id,
        )
    headers = {
        'Authorization': 'Bearer {0}'.format(token),
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    return response.status_code, response.json()

def validate_gcp():

    gcp_credentials = ctx.node.properties.get('gcp_credentials', None)

    if gcp_credentials is None:
        ctx.instance.runtime_properties['connection_status'] = 'Invalid Credentials'
        ctx.instance.runtime_properties['debug_action'] = 'Check your input values'
    else:
        gcp_credentials_json = json.loads(gcp_credentials)

        issuer = subject = gcp_credentials_json.get('client_email', None)
        private_key = gcp_credentials_json.get('private_key', None)
        private_key_id = gcp_credentials_json.get('private_key_id', None)
        project_id = gcp_credentials_json.get('project_id', None)

        ctx.logger.info('issuer {0}, private_key {1}, private_key_id {2}, project_id {3}'.format(
            issuer, private_key, private_key_id, project_id
        ))

        if issuer is None or private_key is None or private_key_id is None or project_id is None:
            ctx.instance.runtime_properties['connection_status'] = 'Invalid Credentials'
            ctx.instance.runtime_properties['debug_action'] = 'Check your input values'
        else:


            now = datetime.datetime.utcnow()
            lifetime = datetime.timedelta(seconds=3600)
            expiry = now + lifetime
            iat = calendar.timegm(now.utctimetuple())
            exp = calendar.timegm(expiry.utctimetuple())
            aud = 'https://www.googleapis.com/oauth2/v4/token'
            scope = 'https://www.googleapis.com/auth/cloud-platform'


            payload = {
                "iss": issuer,
                "sub": subject,
                "iat": iat,
                "exp": exp,
                "aud": aud,
                "scope": scope,
            }

            signer = RSASigner(private_key, private_key_id)

            jwt_token = encode(signer, payload)

            ctx.logger.info('jwt_token {0}'.format(jwt_token))

            bearer_token = get_bearer_token(jwt_token)

            ctx.logger.info('bearer_token {0}'.format(bearer_token))

            status_code, response_content = list_machine_types(bearer_token, project_id)

            if status_code != 200:
                ctx.logger.error(
                    "Invalid GCP credentials : {}".format(response.content.decode('utf-8')))
                raise NonRecoverableError(
                    "Invalid GCP credentials : {}".format(response.content.decode('utf-8')))
