import base64
from http import client
import json

from cloudify import ctx
from cloudify_rest_client import exceptions
from cloudify.manager import get_rest_client
from cloudify.state import ctx_parameters as inputs

client = get_rest_client()
provider = inputs["provider"].lower()
missing = []
message = { 1 : "Please create missing {} secret: {}" }

if provider == "aws":
    secrets = [ "aws_access_key_id", "aws_secret_access_key"]
elif provider == "azure":
    secrets = [ "azure_tenant_id", "azure_client_id","azure_subscription_id", "azure_client_secret"]

for secret in secrets:
    try: 
        client.secrets.get(secret)
    except exceptions.CloudifyClientError:
        missing.append(secret)

if missing:
    raise exceptions.CloudifyClientError("Please, create missing {} secret value for: {}".format(provider.upper(), " and ".join(missing)), status_code = 404)
