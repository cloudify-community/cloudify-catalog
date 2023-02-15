from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
    load_ssh_public_key,
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPrivateNumbers,
    RSAPublicKey,
    RSAPublicNumbers,
    rsa_crt_dmp1,
    rsa_crt_dmq1,
    rsa_crt_iqmp,
    rsa_recover_prime_factors,
)
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cloudify import ctx
import requests
import datetime
import calendar
import base64
import json
from cloudify.exceptions import NonRecoverableError
import sys
sys.tracebacklimit = -1


def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace(b"=", b"")


def from_base64url_uint(val):
    data = base64.base64url_decode(force_bytes(val))
    return int.from_bytes(data, byteorder="big")


def bytes_from_int(val):
    remaining = val
    byte_length = 0

    while remaining != 0:
        remaining >>= 8
        byte_length += 1

    return val.to_bytes(byte_length, "big", signed=False)


def to_base64url_uint(val):
    if val < 0:
        raise ValueError("Must be a positive integer")

    int_bytes = bytes_from_int(val)

    if len(int_bytes) == 0:
        int_bytes = b"\x00"

    return base64url_encode(int_bytes)


def force_bytes(value):
    if isinstance(value, str):
        return value.encode("utf-8")
    elif isinstance(value, bytes):
        return value
    else:
        raise TypeError("Expected a string value")


class Algorithm:
    def compute_hash_digest(self, bytestr):
        hash_alg = getattr(self, "hash_alg", None)
        if hash_alg is None:
            raise NotImplementedError

        if (
            True
            and isinstance(hash_alg, type)
            and issubclass(hash_alg, hashes.HashAlgorithm)
        ):
            digest = hashes.Hash(hash_alg(), backend=default_backend())
            digest.update(bytestr)
            return bytes(digest.finalize())
        else:
            return bytes(hash_alg(bytestr).digest())

    def prepare_key(self, key):
        raise NotImplementedError

    def sign(self, msg, key):
        raise NotImplementedError

    def verify(self, msg, key, sig):
        raise NotImplementedError

    @staticmethod
    def to_jwk(key_obj):
        raise NotImplementedError

    @staticmethod
    def from_jwk(jwk):
        raise NotImplementedError


class RSAAlgorithm(Algorithm):
    SHA256 = hashes.SHA256

    def __init__(self, hash_alg):
        self.hash_alg = hash_alg

    def prepare_key(self, key):
        if isinstance(key, (RSAPrivateKey, RSAPublicKey)):
            return key

        if not isinstance(key, (bytes, str)):
            raise TypeError("Expecting a PEM-formatted key.")

        key_bytes = force_bytes(key)

        try:
            if key_bytes.startswith(b"ssh-rsa"):
                return load_ssh_public_key(key_bytes)
            else:
                return load_pem_private_key(key_bytes, password=None)
        except ValueError:
            return load_pem_public_key(key_bytes)

    @staticmethod
    def to_jwk(key_obj):
        obj = None

        if getattr(key_obj, "private_numbers", None):
            # Private key
            numbers = key_obj.private_numbers()

            obj = {
                "kty": "RSA",
                "key_ops": ["sign"],
                "n": to_base64url_uint(numbers.public_numbers.n).decode(),
                "e": to_base64url_uint(numbers.public_numbers.e).decode(),
                "d": to_base64url_uint(numbers.d).decode(),
                "p": to_base64url_uint(numbers.p).decode(),
                "q": to_base64url_uint(numbers.q).decode(),
                "dp": to_base64url_uint(numbers.dmp1).decode(),
                "dq": to_base64url_uint(numbers.dmq1).decode(),
                "qi": to_base64url_uint(numbers.iqmp).decode(),
            }

        elif getattr(key_obj, "verify", None):
            # Public key
            numbers = key_obj.public_numbers()

            obj = {
                "kty": "RSA",
                "key_ops": ["verify"],
                "n": to_base64url_uint(numbers.n).decode(),
                "e": to_base64url_uint(numbers.e).decode(),
            }
        else:
            raise Exception("Not a public or private key")

        return json.dumps(obj)

    @staticmethod
    def from_jwk(jwk):
        try:
            if isinstance(jwk, str):
                obj = json.loads(jwk)
            elif isinstance(jwk, dict):
                obj = jwk
            else:
                raise ValueError
        except ValueError:
            raise Exception("Key is not valid JSON")

        if obj.get("kty") != "RSA":
            raise Exception("Not an RSA key")

        if "d" in obj and "e" in obj and "n" in obj:
            # Private key
            if "oth" in obj:
                raise Exception(
                    "Unsupported RSA private key: > 2 primes not supported"
                )

            other_props = ["p", "q", "dp", "dq", "qi"]
            props_found = [prop in obj for prop in other_props]
            any_props_found = any(props_found)

            if any_props_found and not all(props_found):
                raise Exception(
                    "RSA key must include all parameters if any are present besides d"
                )

            public_numbers = RSAPublicNumbers(
                from_base64url_uint(obj["e"]),
                from_base64url_uint(obj["n"]),
            )

            if any_props_found:
                numbers = RSAPrivateNumbers(
                    d=from_base64url_uint(obj["d"]),
                    p=from_base64url_uint(obj["p"]),
                    q=from_base64url_uint(obj["q"]),
                    dmp1=from_base64url_uint(obj["dp"]),
                    dmq1=from_base64url_uint(obj["dq"]),
                    iqmp=from_base64url_uint(obj["qi"]),
                    public_numbers=public_numbers,
                )
            else:
                d = from_base64url_uint(obj["d"])
                p, q = rsa_recover_prime_factors(
                    public_numbers.n, d, public_numbers.e
                )

                numbers = RSAPrivateNumbers(
                    d=d,
                    p=p,
                    q=q,
                    dmp1=rsa_crt_dmp1(d, p),
                    dmq1=rsa_crt_dmq1(d, q),
                    iqmp=rsa_crt_iqmp(p, q),
                    public_numbers=public_numbers,
                )

            return numbers.private_key()
        elif "n" in obj and "e" in obj:
            # Public key
            return RSAPublicNumbers(
                from_base64url_uint(obj["e"]),
                from_base64url_uint(obj["n"]),
            ).public_key()
        else:
            raise Exception("Not a public or private key")

    def sign(self, msg, key):
        return key.sign(msg, padding.PKCS1v15(), self.hash_alg())

    def verify(self, msg, key, sig):
        try:
            key.verify(sig, msg, padding.PKCS1v15(), self.hash_alg())
            return True
        except InvalidSignature:
            return False


def get_bearer_token(jwt_token):
    url = "https://www.googleapis.com/oauth2/v4/token"
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token
    }
    ctx.logger.info('data {0}'.format(data))
    response = requests.post(url, data=data)
    return response.json().get('access_token', None)


def list_machine_types(token, project_id):
    url = "https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/us-west1-a/machineTypes".format(
        project_id=project_id,
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

            segments = []

            payload = {
                "iss": issuer,
                "sub": subject,
                "iat": iat,
                "exp": exp,
                "aud": aud,
                "scope": scope,
            }

            json_payload = json.dumps(
                payload,
                separators=(",", ":"),
                cls=None,
            ).encode("utf-8")

            headers = {
                "typ": "JWT",
                "alg": "RS256",
                "kid": private_key_id
            }

            json_header = json.dumps(
                headers, separators=(",", ":"), cls=None, sort_keys=True
            ).encode()

            segments.append(base64url_encode(json_header))
            msg_payload = base64url_encode(json_payload)
            segments.append(msg_payload)
            signing_input = b".".join(segments)
            alg_obj = RSAAlgorithm(RSAAlgorithm.SHA256)
            key = alg_obj.prepare_key(private_key)
            signature = alg_obj.sign(signing_input, key)
            segments.append(base64url_encode(signature))
            encoded_string = b".".join(segments)
            jwt_token = encoded_string.decode("utf-8")

            ctx.logger.info('jwt_token {0}'.format(jwt_token))

            bearer_token = get_bearer_token(jwt_token)

            ctx.logger.info('bearer_token {0}'.format(bearer_token))

            status_code, response_content = list_machine_types(bearer_token, project_id)

            if status_code != 200:
                ctx.logger.error(
                    "Invalid Azure credentials : {}".format(response_content))
                raise NonRecoverableError(
                    "Invalid Azure credentials : {}".format(response_content))
