from cloudify_rest_client import exceptions
from cloudify.exceptions import NonRecoverableError
from cloudify.manager import get_rest_client
from cloudify.state import ctx_parameters as inputs

client = get_rest_client()
provider = inputs["provider"].lower()
missing = []

if provider == "aws":
    secrets = ["aws_access_key_id", "aws_secret_access_key"]
elif provider == "azure":
    secrets = ["azure_tenant_id", "azure_client_id",
               "azure_subscription_id", "azure_client_secret"]

for secret in secrets:
    try:
        client.secrets.get(secret)
    except exceptions.CloudifyClientError:
        missing.append(secret)

if missing:
    raise NonRecoverableError("Please, create missing {} secret value for: {}".format(
        provider.upper(), " and ".join(missing)))
