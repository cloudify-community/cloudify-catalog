import logging
import os.path
import re
from urllib.parse import urlparse

import yaml

S3_BASE_URL = "s3_base_url"
S3_BUCKET_NAME = "s3_bucket_name"
S3_BUCKET_DIRECTORY = "s3_bucket_directory"
GIT_URL = "git_url"
TARGET_PATH = "target_path"
GITHUB_URL = "github_url"
RAW_GITHUB_URL = "raw_github_url"

catalog_mandatory_fileds = [
    S3_BASE_URL,
    S3_BUCKET_NAME,
    S3_BUCKET_DIRECTORY,
    GIT_URL,
    TARGET_PATH,
    GITHUB_URL,
    RAW_GITHUB_URL
]

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)


def validate_url(value: str) -> bool:
    """Validates if the value is URL

    :param value: string to be validated
    :return: True if the vlue is URL
    """
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def validate_id_value(value: str) -> bool:
    """Validates if the value contains of digits, latters, -, _ only

    :param value: string to be validated
    :return: True if the value is not None and valid id
    """

    regexp = re.compile('^[0-9a-zA-Z\-\_]+$')
    return value and regexp.search(value)


def validate_path(value: str) -> bool:
    """Validates if the value is a path

    :param value: string to be validated
    :return: True if the value is a path
    """
    regexp = re.compile('^[0-9a-zA-Z\-\_\/]+$')
    return value and regexp.search(value)


def validate_path_exists(value: str) -> bool:
    """Validates if the value is a relative path within the directory

    :param value: path to be validated
    :retrun: True if the value is existing path
    """
    return validate_path(value) and os.path.isdir(value)


class Blueprint:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return " ".join(['Blueprint(', self.name, self.id, self.path, self.description, ')'])

    def __hash__(self):
        return hash(repr(self))

    def validate_mandatory_fields(self) -> bool:
        """Validates if the instance's mandatory properties are defined:
                - id
                - name
                - path
                - description
        :return: True if all the required properties are defined
        """
        result = True
        mandatory_fields = ["id", "name", "path", "description"]
        for mandatory_field in mandatory_fields:
            if mandatory_field not in self.__dict__.keys():
                logging.error("Blueprint \"{}\" is missing a mandatory field \"{}\"".format(
                    self.name, mandatory_field))
                result = False
        return result

    def validate_allowed_properies_only(self) -> bool:
        """Validates that the instance has only known properties
                - id
                - name
                - path
                - description
                - html_url
                - zip_url
                - readme_url
                - main_blueprint
                - image_url

        :return: True if only known properties are defined
        """
        result = True
        allowed_fields = ["id", "name", "path", "description", "html_url",
                          "zip_url", "readme_url", "main_blueprint", "image_url"]
        for field in self.__dict__.keys():
            if field not in allowed_fields:
                logging.error(
                    "Blueprint \"{}\" has unknown field \"{}\"".format(self.name, field))
                result = False
        return result

    def validate(self) -> bool:
        """Validates if the instance addresses the following criteria:
                - All the mandatory properties are defined
                - All the defined properties are known
                - if and name property are correct
                - path is valid directory path and exists
                - html_url, zip_url, readme_url, image_url are valid URLs

        :return: True if all the validations passed
        """
        result = self.validate_mandatory_fields()
        if not self.validate_allowed_properies_only():
            result = False
        if not validate_id_value(self.id):
            logging.error(
                "Blueprint \"{}\" has invalid id value \"{}\"".format(self.name, self.id))
            result = False
        if not validate_id_value(self.name):
            logging.error("Blueprint \"{}\" has invalid name value \"{}\"".format(
                self.name, self.name))
            result = False
        if not validate_path(self.path):
            logging.error("Blueprint \"{}\" has invalid path value \"{}\"".format(
                self.name, self.path))
            result = False
        if not validate_path_exists(self.path):
            logging.error("Blueprint \"{}\" has non existing path \"{}\"".format(
                self.name, self.path))
            result = False
        if "html_url" in self.__dict__.keys():
            if not validate_url(self.html_url):
                logging.error("Blueprint \"{}\" has invalid html_url value \"{}\"".format(
                    self.name, self.html_url))
                result = False
        if "zip_url" in self.__dict__.keys():
            if not validate_url(self.zip_url):
                logging.error("Blueprint \"{}\" has invalid zip_url value \"{}\"".format(
                    self.name, self.zip_url))
                result = False
        if "readme_url" in self.__dict__.keys():
            if not validate_url(self.readme_url):
                logging.error("Blueprint \"{}\" has invalid readme_url value \"{}\"".format(
                    self.name, self.readme_url))
                result = False
        if "image_url" in self.__dict__.keys():
            if not validate_url(self.image_url):
                logging.error("Blueprint \"{}\" has invalid image_url value \"{}\"".format(
                    self.name, self.image_url))
                result = False
        else:
            if not os.path.isfile("{}/{}".format(self.path, "logo.png")):
                logging.error("Blueprint \"{}\" doesn't have logo.png file in the path \'{}\"".format(
                    self.name, self.path))
                result = False
        if "main_blueprint" in self.__dict__.keys():
            if not validate_path(self.main_blueprint):
                logging.error("Blueprint \"{}\" has invalid main_blueprint value \"{}\"".format(
                    self.name, self.main_blueprint))
                result = False
        else:
            if not os.path.isfile("{}/{}".format(self.path, "blueprint.yaml")):
                logging.error("Blueprint \"{}\" doesn't have blueprint.yaml file in the path \'{}\"".format(
                    self.name, self.path))
                result = False
        return result


class Topic:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if "blueprints" in kwargs.keys():
            self.blueprints = []
            for blueprint in kwargs["blueprints"]:
                self.blueprints.append(Blueprint(**blueprint))

    def validate_mandatory_fields(self) -> bool:
        """Validates if the instance's mandatory properties are defined:
                - name
                - target_path
                - blueprints

        :return: True if all the required properties are defined
        """
        result = True
        mandatory_fields = ["name", "target_path", "blueprints"]
        for mandatory_filed in mandatory_fields:
            if mandatory_filed not in self.__dict__.keys():
                logging.error("Topic \"{}\" is missing a mandatory field {}".format(
                    self.name, mandatory_filed))
                result = False
        return result

    def validate_blueprints_ids_unique(self) -> bool:
        """All the blueprints has unique ids

        :return: True if there are no two blueprints with the same id
        """
        result = True
        blueprints_ids = []
        if "blueprints" in self.__dict__.keys():
            for blueprint in self.blueprints:
                if blueprint.id in blueprints_ids:
                    logging.error("Topic \"{}\" has multiple blueprints with the same id \"{}\" already exist".format(
                        self.name, blueprint.id))
                    result = False
                else:
                    blueprints_ids.append(blueprint.id)
        return result

    def validate(self) -> bool:
        """Validates if the instance addresses:
                - all the mandatory properties defined
                - all the blueprints have unique id
                - all the blueprints are valid

        :return: True if the instance is valid
        """
        result = self.validate_mandatory_fields()
        if not validate_id_value(self.name):
            logging.error("name \"{}\" is not valid".format(self.name))
            result = False
        if not self.validate_blueprints_ids_unique():
            result = False
        if "blueprints" in self.__dict__.keys():
            for blueprint in self.blueprints:
                if not blueprint.validate():
                    result = False
        return result


class Catalog:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if "topics" in kwargs.keys():
            self.topics = []
            for topic in kwargs["topics"]:
                self.topics.append(Topic(**topic))

    def validate_duplicate_fields(self) -> bool:
        """Validates if the instance's properties are not duplicated:
                - id
                - name
                - path
        """
        result = True
        for topic in self.topics:
            print(topic.id)
        return result

    def validate_mandatory_fields(self) -> bool:
        """Validates if the instance's mandatory properties are defined:
                - s3_base_url
                - s3_bucket_name
                - s3_bucket_directory
                - git_url
                - target_path
                - github_url
                - raw_github_url

        :return: True if all the required properties are defined
        """
        result = True
        mandatory_fileds = [S3_BASE_URL, S3_BUCKET_NAME, S3_BUCKET_DIRECTORY,
                            GIT_URL, TARGET_PATH, GITHUB_URL, RAW_GITHUB_URL]
        for mandatory_filed in mandatory_fileds:
            if mandatory_filed not in self.__dict__.keys():
                logging.error(
                    "mandatory filed {} is missing".format(mandatory_filed))
                result = False
        return result

    def validate_topics_names_unique(self) -> bool:
        """All the topics has unique name

        :return: True if there are no two topics with the same name
        """
        result = True
        topic_names = []
        for topic in self.topics:
            if topic.name in topic_names:
                logging.error(
                    "topic \"{}\" already existis".format(topic.name))
                result = False
            else:
                topic_names.append(topic.name)
        return result

    def validate_paths_equal_properties(self) -> bool:
        """Test if items with the same path has the same properties such
                - id
                - name
                - description
        """
        blueprints = sum([topic.blueprints for topic in self.topics], [])
        result = True
        paths = {}

        for bp in blueprints:
            if bp.path not in paths:
                paths[bp.path] = [bp]
            else:
                if hash(bp) not in [hash(item) for item in paths[bp.path]]:
                    paths[bp.path].append(bp)

        for _, props in paths.items():

            if len(props) > 1:
                msg = ""
                for bp in props:
                    msg += "id: {}\nname: {}\npath: {}\ndescription: {}\n\n".format(
                        bp.id, bp.name, bp.path, bp.description)
                logging.error(
                    """The different values for the same blueprint path"""
                    """ were detected in below catalog items: \n\n{}""".format(msg))
                result = False
        return result

    def validate(self) -> bool:
        """Validates if the instance addresses:
                - all the mandatory properties defined
                - s3_bucket_name is valid
                - s3_bucket_directory is a path
                - git_url, target_path, github_url, raw_github_url are URLs
                - all the topics have unique names
                - all the topics are valid

        :return: True if the instance is valid
        """
        result = True
        result = result or self.validate_mandatory_fields()

        if not validate_url(self.s3_base_url):
            logging.error("s3_base_url is not a valid URL")
            result = False
        if not validate_id_value(self.s3_bucket_name):
            logging.error("s3_bucket_name value \"{}\" is not valid".format(
                self.s3_bucket_name))
            result = False
        if not validate_path(self.s3_bucket_directory):
            logging.error("s3_bucket_directory value \"{}\" is not a valid path".format(
                self.s3_bucket_directory))
            result = False
        if not validate_url(self.git_url):
            logging.error(
                "git_url value \"{}\" is not a valid url".format(self.git_url))
            result = False
        if not validate_url(self.target_path):
            logging.error(
                "target_path value \"{}\" is not a valud url".format(self.target_path))
            result = False
        if not validate_url(self.github_url):
            logging.error(
                "github_url value \"{}\" is not a valid url".format(self.github_url))
            result = False
        if not validate_url(self.raw_github_url):
            logging.error("raw_github_url value \"{}\" is not a valid url".format(
                self.raw_github_url))
            result = False
        result = self.validate_topics_names_unique()
        result = self.validate_paths_equal_properties()
        for topic in self.topics:
            if not topic.validate():
                result = False
        return result


def main():
    with open("catalog.yaml", 'r') as stream:
        try:
            catalog = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)
            logging.error("Failed to process catalog.yaml file")
            exit(1)

    c = Catalog(**catalog)
    if not c.validate():
        exit(1)


if __name__ == "__main__":
    main()
