from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.manager import get_rest_client

client = get_rest_client()
token = inputs['kube_token']
client.secrets.create('kubernetes_token', token, update_if_exists=True)
