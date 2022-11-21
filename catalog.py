import datetime
import json
import logging
import os
import re
import shutil
import xml.etree.ElementTree as ET

import yaml
from pygit2 import Repository

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

TEST_RESULT_PATH = os.environ["TEST_RESULT_PATH"]
BP_NAME = re.compile("(?<=\[)(.*)(?=\])")

def read_xml(path):
    try:
        test_suites = ET.parse(path)
        return test_suites.getroot()
    except FileNotFoundError:
        logging.info(
            'The test result file was not found under: {} path'.format(path))
        return None

def get_broken_bps_ids():
    test_suites = read_xml(TEST_RESULT_PATH)
    broken_bps = []
    if test_suites:
        for suite in test_suites:   
            for test_case in suite:
                if list(test_case):
                    match = BP_NAME.search(test_case.attrib.get('name'))
                    if match: 
                        broken_bps.append(match[0])
    return broken_bps

def create_build_directories():
    """Creates a build directory and catalogs directory in it
    """
    if not os.path.exists("build"):
        os.mkdir("build")

    if not os.path.exists("build/catalogs"):
        os.mkdir("build/catalogs")


def get_zip_url(blueprint: dict, target_path: str) -> str:
    """Retrieves zip_url for blueprint

    :param blueprint: blueprint settings
    :return: zip_url from blueprint if exists other wise calculated 
    """
    zip_url = blueprint['zip_url'] if 'zip_url' in blueprint.keys() else None

    if zip_url is None and 'path' in blueprint:
        path = blueprint['path'][0:blueprint['path'].rfind("/")]
        filename_path = ("%s/%s") % (path, blueprint['id'])
        zip_url = "{}/{}.zip".format(target_path, filename_path)

    return zip_url


def get_html_url(blueprint: dict, github_url: str) -> str:
    html_url = blueprint['html_url'] if 'html_url' in blueprint.keys(
    ) else None

    if html_url is None and 'path' in blueprint.keys():
        html_url = "{}/{}".format(github_url, blueprint['path'])

    return html_url


def get_readme_url(blueprint: dict, raw_github_url: str) -> str:
    readme_url = blueprint['readme_url'] if 'readme_url' in blueprint.keys(
    ) else None

    if readme_url is None and 'path' in blueprint.keys():
        readme_url = "{}/{}/README.md".format(
            raw_github_url, blueprint['path'])

    return readme_url


def get_image_url(blueprint: dict, raw_github_url: str, broken_bps: list) -> str:
    image_url = blueprint['image_url'] if 'image_url' in blueprint.keys(
    ) else None
    if image_url is None and 'path' in blueprint.keys():
        image_url = "{}/{}/logo.png".format(raw_github_url, blueprint['path'])
    if blueprint.get("id") in broken_bps:
        logging.info("Broken bp: {}".format(blueprint.get('id')))
        image_url = "{}/logos/logo.png".format(raw_github_url)
    return image_url


def get_main_blueprint(blueprint: dict) -> str:
    main_blueprint = blueprint["main_blueprint"] if 'main_blueprint' in blueprint.keys(
    ) else "blueprint.yaml"
    return main_blueprint


def archive_blueprint(blueprint: dict):
    if 'path' in blueprint:
        path = blueprint['path'][0:blueprint['path'].rfind("/")]
        dir_name = blueprint['path'][blueprint['path'].rfind("/")+1:]

        output_filename = ("build/%s/%s") % (path, blueprint['id'])

        shutil.make_archive(output_filename, 'zip', path, dir_name)


def create_catalog(catalog_name: str, catalog: dict):
    json_object = json.dumps(catalog, indent=4)
    catalog_filename = "build/catalogs/%s.json" % catalog_name

    with open(catalog_filename, "w+") as outfile:
        outfile.write(json_object)


def get_target_sub_folder(branch: str) -> str:
    pattern = re.compile("(\\d+\\.\\d+)\\.\\d+\\-build")
    result = re.match(pattern, branch)
    return result.group(1) if result else "staging/{}".format(branch)


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
    with open("catalog.yaml", 'r') as stream:
        try:
            catalog = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    head = set_head()
    target_path_subfolder = get_target_sub_folder(head)

    git_url = catalog['git_url']
    target_path = "{}/{}".format(catalog['target_path'], target_path_subfolder)
    github_url = "{}/{}".format(catalog['github_url'], head)
    raw_github_url = "{}/{}".format(catalog['raw_github_url'], head)

    create_build_directories()
    for package in catalog['topics']:
        catalog = []
        logging.info('processing catalog %s' % package['name'])
        if 'blueprints' in package:
            result = []
            broken_bps = get_broken_bps_ids()
            for blueprint in package['blueprints']:
                logging.info("processing blueprint %s" % blueprint['id'])

                zip_url = get_zip_url(blueprint, target_path)
                html_url = get_html_url(blueprint, github_url)
                readme_url = get_readme_url(blueprint, raw_github_url)
                main_blueprint = get_main_blueprint(blueprint)
                
                image_url = get_image_url(blueprint, raw_github_url, broken_bps)

                archive_blueprint(blueprint)

                catalog_item = {
                    "id": blueprint['id'],
                    "name": blueprint['name'],
                    "description": blueprint['description'],
                    "html_url": html_url,
                    "zip_url": zip_url,
                    "readme_url": readme_url,
                    "main_blueprint": main_blueprint,
                    "image_url": image_url,
                    "crated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "updated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                catalog.append(catalog_item)

            create_catalog(package['name'], catalog)


if __name__ == "__main__":
    main()