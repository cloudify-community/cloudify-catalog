import os
import sys
import zipfile
#import tempfile
from inspect import getsourcefile
from os.path import dirname

from cloudify import ctx
from cloudify_rest_client import exceptions
from cloudify.exceptions import NonRecoverableError
from cloudify.manager import get_rest_client
from cloudify.state import ctx_parameters as inputs

sys.tracebacklimit = -1

client = get_rest_client()
secrets = [secret.lower() for secret in inputs["secrets"]]
missing = []

def _handle_parent_directory(into_dir):
    extracted_files = os.listdir(into_dir)
    ctx.logger.info(extracted_files)
    if len(extracted_files) == 1:
        inner_dir = os.path.join(into_dir, extracted_files[0])
        if os.path.isdir(inner_dir):
            return inner_dir
    return into_dir

def unzip_archive(archive_path, skip_parent_directory=True):
    """
    Unzip a zip archive.
    this method memic strip components
    """
    into_dir = dirname(__file__) #tempfile.mkdtemp()
    ctx.logger.info("Unzipping to {}".format(into_dir))
    zip_in = None
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(into_dir)
            for info in zip_ref.infolist():
                reset_target = os.path.join(into_dir, info.filename)
                if info.external_attr >> 16 > 0:
                    os.chmod(reset_target, info.external_attr >> 16)
        if skip_parent_directory:
            into_dir = _handle_parent_directory(into_dir)
    except zipfile.BadZipFile as e:
        # clean up that temp directory and raise the exception
        shutil.rmtree(into_dir)
        raise e
    finally:
        if zip_in:
            zip_in.close()
            os.remove(archive_path)
    return into_dir

class_path = ctx.download_resource('scripts/check_connection.zip')
unziped_class = unzip_archive(class_path)

# inject the unzip class to use the module
sys.path.append(unziped_class)
from check_connection.aws import validate_aws
from check_connection.azure import validate_azure
from check_connection.gcp import validate_gcp

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
else:
    if inputs["provider"].lower() == "aws":
        validate_aws()
    elif inputs["provider"].lower() == "azure":
        validate_azure()
    elif inputs["provider"].lower() == "gcp":
        validate_gcp()
    else:
        ctx.logger.error("Unsupported provider for secret validation!")