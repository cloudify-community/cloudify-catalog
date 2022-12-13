import sys
import hmac
import hashlib
import datetime

try:
    from urllib import quote
    from urlparse import urlparse
except ImportError:
    from urllib.parse import quote, urlparse

import requests

from cloudify import ctx
from cloudify.manager import get_rest_client
from cloudify.exceptions import NonRecoverableError

sys.tracebacklimit = -1

host = 'ec2.amazonaws.com'
region = ctx.node.properties.get('aws_region_name', 'us-east-1')
service = 'ec2'

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4{0}'.format(key)).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

class AWSRequestsAuth(requests.auth.AuthBase):
    def __init__(self,
                 aws_access_key,
                 aws_secret_access_key,
                 aws_host,
                 aws_region,
                 aws_service,
                 aws_token=None):
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_host = aws_host
        self.aws_region = aws_region
        self.service = aws_service
        self.aws_token = aws_token

    def __call__(self, r):
        aws_headers = self.get_aws_request_headers_handler(r)
        r.headers.update(aws_headers)
        return r

    def get_aws_request_headers_handler(self, r):
        return self.get_aws_request_headers(r=r,
                                            aws_access_key=self.aws_access_key,
                                            aws_secret_access_key=self.aws_secret_access_key,
                                            aws_token=self.aws_token)

    def get_aws_request_headers(self, r, aws_access_key, aws_secret_access_key, aws_token):
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        canonical_uri = AWSRequestsAuth.get_canonical_path(r)
        canonical_querystring = AWSRequestsAuth.get_canonical_querystring(r)
        canonical_headers = ('host:' + self.aws_host + '\n' +
                             'x-amz-date:' + amzdate + '\n')
        if aws_token:
            canonical_headers += 'x-amz-security-token:' + aws_token + '\n'

        signed_headers = 'host;x-amz-date'
        if aws_token:
            signed_headers += ';x-amz-security-token'

        body = r.body if r.body else bytes()
        try:
            body = body.encode('utf-8')
        except (AttributeError, UnicodeDecodeError):
            body = body

        payload_hash = hashlib.sha256(body).hexdigest()

        canonical_request = (r.method + '\n' + canonical_uri + '\n' +
                             canonical_querystring + '\n' + canonical_headers +
                             '\n' + signed_headers + '\n' + payload_hash)

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = (datestamp + '/' + self.aws_region + '/' +
                            self.service + '/' + 'aws4_request')
        string_to_sign = (algorithm + '\n' + amzdate + '\n' + credential_scope +
                          '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())

        signing_key = getSignatureKey(aws_secret_access_key,
                                      datestamp,
                                      self.aws_region,
                                      self.service)

        string_to_sign_utf8 = string_to_sign.encode('utf-8')
        signature = hmac.new(signing_key,
                             string_to_sign_utf8,
                             hashlib.sha256).hexdigest()

        authorization_header = (algorithm + ' ' + 'Credential=' + aws_access_key +
                                '/' + credential_scope + ', ' + 'SignedHeaders=' +
                                signed_headers + ', ' + 'Signature=' + signature)

        headers = {
            'Authorization': authorization_header,
            'x-amz-date': amzdate,
            'x-amz-content-sha256': payload_hash
        }
        if aws_token:
            headers['X-Amz-Security-Token'] = aws_token
        return headers

    @classmethod
    def get_canonical_path(cls, r):
        parsedurl = urlparse(r.url)
        return quote(parsedurl.path if parsedurl.path else '/', safe='/-_.~')

    @classmethod
    def get_canonical_querystring(cls, r):
        canonical_querystring = ''
        parsedurl = urlparse(r.url)
        querystring_sorted = '&'.join(sorted(parsedurl.query.split('&')))

        for query_param in querystring_sorted.split('&'):
            key_val_split = query_param.split('=', 1)

            key = key_val_split[0]
            if len(key_val_split) > 1:
                val = key_val_split[1]
            else:
                val = ''

            if key:
                if canonical_querystring:
                    canonical_querystring += "&"
                canonical_querystring += u'='.join([key, val])

        return canonical_querystring

def validate_aws():
    
    client = get_rest_client() 
    access_key = client.secrets.get('aws_access_key_id')
    secret_key = client.secrets.get('aws_secret_access_key')

    aws_auth = AWSRequestsAuth(access_key, secret_key, host, region, service)

    response = requests.get('http://ec2.amazonaws.com/?Action=DescribeInstances',
                            auth=aws_auth)

    if response.status_code != 200:
        ctx.logger.error(
            "Invalid AWS credentials : {}".format(response.content.decode('utf-8')))
        raise NonRecoverableError(
            "Invalid AWS credentials : {}".format(response.content.decode('utf-8')))
