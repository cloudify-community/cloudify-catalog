import re
import os
import yaml
import boto3
import logging


from pygit2 import Repository
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.DEBUG)

CATALOG_FILE_NAME = "catalog.yaml"
BUILD_DIRECTORY = "build"
GETTING_STARTED_DIRECTORY = "getting_started"
S3_BASE_URL = "s3_base_url"
S3_BUCKET_NAME = "s3_bucket_name"
S3_BUCKET_DIRECTORY = "s3_bucket_directory"
S3_GETTING_STARTED_DIRECTORY = "s3_getting_started_directory"
AWS_ACCESS_KEY_ID = os.environ["ID"]
AWS_SECRET_ACCCES_KEY = os.environ["SECRET"]


def get_target_sub_folder(branch: str) -> str:
    """Retrieves the directory name where the artifacts should be stored at
    For the branch X.Y.Z-build the folder should be X.Y
    For the rest branches the directory is staging/[BRANCH_NAME]

    :param branch: Git branch name
    """

    pattern = re.compile("(\\d+\\.\\d+)\\.\\d+\\-build")
    result = re.match(pattern, branch)
    return result.group(1) if result else "staging/{}".format(branch)


def upload_file(file_name: str, bucket: str, object_name: str = None) -> bool:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCCES_KEY,
                             region_name="eu-west-1")
    try:
        response = s3_client.upload_file(
            file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
    except ClientError as e:
        logging.error(e)
        return False
    return True


def check_branch(directory: str):
    for version in ['7.0', '6.4', '6.3', '6.2']:
        if version in directory:
            return True
    return False


def set_target_path(directory: str, root: str, file: str):
    if "catalogs" in root and check_branch(directory) or root == "":
        target_file = "{}/{}".format(directory, file)
    else:
        target_file = "{}/{}/{}".format(directory,
                                        root[root.find("/")+1:], file)
    return target_file


def upload_directory(source_directory: str, bucket: str, directory: str, without_root: bool = False):
    """Uploads directories and files in the build to S3

    :param source_directory: build directory where all the artifact are stored
    :param bucket: The S3 bucket name
    :param directory: the base directory in S3 bucket where to upload all the artifacts
    """

    for root, _, files in os.walk(source_directory):
        for file in files:
            if without_root:
                target_file = set_target_path(directory, "", file)
            else:
                target_file = set_target_path(directory, root, file)
            source_file = "{}/{}".format(root, file)
            upload_file(source_file, bucket, target_file)


def print_catalogs_urls(build_directory: str, base_url: str, directory: str, without_root: bool = False):
    """Prints all the catalogs

    :param build_directory: build directory
    :param base_url: The base URL to s3
    :param directory: the base directory in S3 bucket where to upload all the artifacts
    """

    for root, _, files in os.walk(build_directory):
        for file in files:
            if without_root:
                target_file = set_target_path(directory, "", file)
            else:
                target_file = set_target_path(directory, root, file)
            print("{}/{}".format(base_url, target_file))


def set_head():
    try:
        head = os.environ["GIT_BRANCH"]
        if re.match("^PR-[\\d]{1,4}-(merge|head)$", head):
            # it means that we are on the prs branches
            head = os.environ["CHANGE_BRANCH"]
    except KeyError:
        # we are on local machine
        head = Repository('.').head.shorthand
        print(
            "No Jenkins pipeline environment variable. Setting the branch name to: {}".format(head))
    return head


def main():
    with open(CATALOG_FILE_NAME, 'r') as stream:
        try:
            catalog = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    head = set_head()
    target_path_subfolder = get_target_sub_folder(head)

    base_url = catalog[S3_BASE_URL]
    s3_bucket_name = catalog[S3_BUCKET_NAME]
    s3_bucket_directory = "{}/{}".format(
        catalog[S3_BUCKET_DIRECTORY], target_path_subfolder)

    #upload catalog tabs directory
    upload_directory(BUILD_DIRECTORY, s3_bucket_name, s3_bucket_directory)
    print_catalogs_urls(BUILD_DIRECTORY, base_url, s3_bucket_directory)

    # # upload getting started directory
    s3_bucket_directory = "{}/{}".format(
        catalog[S3_GETTING_STARTED_DIRECTORY], target_path_subfolder)
    upload_directory(GETTING_STARTED_DIRECTORY, s3_bucket_name, s3_bucket_directory, True)
    print_catalogs_urls(GETTING_STARTED_DIRECTORY, base_url, s3_bucket_directory, True)


if __name__ == "__main__":
    main()

