import sys
from cloudify import ctx
from cloudify_rest_client import exceptions
from cloudify.exceptions import NonRecoverableError
from cloudify.manager import get_rest_client
from cloudify.state import ctx_parameters as inputs

sys.tracebacklimit = -1

client = get_rest_client()
secrets = [secret.lower() for secret in inputs["secrets"]]
missing = []

for secret in secrets:
    try:
        client.secrets.get(secret)
    except exceptions.CloudifyClientError:
        missing.append(secret)

if missing:
    ctx.logger.error(
        "Please, create missing secret value for: {}".format(" and ".join(missing)))
    raise NonRecoverableError(
        "Missing secret value for: {}".format(" and ".join(missing)))
