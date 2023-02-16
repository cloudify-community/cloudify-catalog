from cloudify.exceptions import NonRecoverableError
from cloudify.manager import get_rest_client
from cloudify import ctx
import requests
import json
import time
import copy
import sys
PY2 = sys.version_info[0] == 2

if PY2:
    import httplib
else:
    import http.client as httplib

sys.tracebacklimit = -1


def authorize_with_azure(azure_tenant, azure_client_id, azure_secret):

    url = "https://login.microsoftonline.com/{0}/oauth2/token".format(
        azure_tenant)
    body = {
        "resource": "https://management.core.windows.net/",
        "client_id": azure_client_id,
        "grant_type": "client_credentials",
        "client_secret": azure_secret
    }
    response = requests.post(url, data=body)
    return response.json()


def list_resource_groups(azure_tenant, azure_client_id, azure_secret, azure_subscription_id):
    client = get_rest_client()
    azure_subscription_id = client.secrets.get('azure_subscription_id', None)
    url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups?api-version=2022-09-01".format(
        subscriptionId=azure_subscription_id,
    )
    bearer_token = authorize_with_azure(
        azure_tenant, azure_client_id, azure_secret).get(
        'access_token', 'invalid_creds')
    if bearer_token == 'invalid_creds':
        return 401, "Invalid Token -it wasn't created-"
    headers = {
        'Authorization': 'Bearer ' + authorize_with_azure(azure_tenant, azure_client_id, azure_secret)['access_token'],
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.status_code, response.json()


def validate_azure():

    client = get_rest_client()
    azure_tenant = client.secrets.get('azure_tenant_id').get('value', None)
    azure_client_id = client.secrets.get('azure_client_id').get('value', None)
    azure_secret = client.secrets.get('azure_client_id').get('value', None)
    azure_subscription_id = client.secrets.get('azure_subscription_id').get('value', None)

    if azure_tenant is None or azure_client_id is None or azure_secret is None or azure_subscription_id is None:
        msg = "Missing credentials for Azure cloud provider: azure_tenant_id, \
            azure_client_id, azure_client_secret and azure_subscription_id"
        ctx.logger.error(msg)
        raise NonRecoverableError(msg)

    else:

        status_code, response_content = list_resource_groups(
            azure_tenant, azure_client_id, azure_secret, azure_subscription_id)

        if status_code != 200:
            ctx.logger.error(
                "Invalid Azure credentials : {}".format(response_content))
            raise NonRecoverableError(
                "Invalid Azure credentials : {}".format(response_content))
