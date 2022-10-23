import base64
import json

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

token = base64.b64decode(inputs['kube_token']).decode('utf-8')
ctx.instance.runtime_properties['token'] = token
ssl_ca_cert = base64.b64decode(inputs['ssl_certificate']).decode('utf-8')
ctx.instance.runtime_properties['ssl_ca_cert'] = ssl_ca_cert