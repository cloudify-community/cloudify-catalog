import re
import os.path
import yaml
import logging
import validators

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

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


def validate_url(value: str) -> bool:
	return value is not None and validators.url(value)

def validate_id_value(value: str) -> bool:
	regexp = re.compile('^[0-9a-zA-Z\-\_]+$')
	return value and regexp.search(value)

def validate_path(value: str) -> bool:
	regexp = re.compile('^[0-9a-zA-Z\-\_\/]+$')
	return value and regexp.search(value)

def validate_path_exists(value: str) -> bool:
	return validate_path(value) and os.path.isdir(value)

class Blueprint:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def validate_mandatory_fields(self) -> bool:
		result = True
		mandatory_fields = ["id", "name", "path", "description"]
		for mandatory_field in mandatory_fields:
			if mandatory_field not in self.__dict__.keys():
				logging.error("Blueprint \"{}\" is missing a mandatory field \"{}\"".format(self.name, mandatory_field))
				result = False
		return result

	def validate_allowed_properies_only(self) -> bool:
		result = True
		allowed_fields = ["id", "name", "path", "description", "html_url", "zip_url", "readme_url", "main_blueprint", "image_url"]
		for field in self.__dict__.keys():
			if field not in allowed_fields:
				logging.error("Blueprint \"{}\" has unknown field \"{}\"".format(self.name, field))
				result = False
		return result

	def validate(self) -> bool:
		result = self.validate_mandatory_fields()
		if not self.validate_allowed_properies_only():
			result = False
		if not validate_id_value(self.id):
			logging.error("Blueprint \"{}\" has invalid id value \"{}\"".format(self.name, self.id))
			result = False
		if not validate_id_value(self.name):
			logging.error("Blueprint \"{}\" has invalid name value \"{}\"".format(self.name, self.name))
			result = False
		if not validate_path(self.path):
			logging.error("Blueprint \"{}\" has invalid path value \"{}\"".format(self.name, self.path))
			result = False
		if not validate_path_exists(self.path):
			logging.error("Blueprint \"{}\" has non existing path \"{}\"".format(self.name, self.path))
			result = False
		if "html_url" in self.__dict__.keys():
			if not validate_url(self.html_url):
				logging.error("Blueprint \"{}\" has invalid html_url value \"{}\"".format(self.name, self.html_url))
				result = False
		if "zip_url" in self.__dict__.keys():
			if not validate_url(self.zip_url):
				logging.error("Blueprint \"{}\" has invalid zip_url value \"{}\"".format(self.name, self.zip_url))
				result = False
		if "readme_url" in self.__dict__.keys():
			if not validate_url(self.readme_url):
				logging.error("Blueprint \"{}\" has invalid readme_url value \"{}\"".format(self.name, self.readme_url))
				result = False
		if "image_url" in self.__dict__.keys():
			if not validate_url(self.image_url):
				logging.error("Blueprint \"{}\" has invalid image_url value \"{}\"".format(self.name, self.image_url))
				result = False
		else:
			if not os.path.isfile("{}/{}".format(self.path, "logo.png")):
				logging.error("Blueprint \"{}\" doesn't have logo.png file in the path \'{}\"".format(self.name, self.path))
				result = False
		if "main_blueprint" in self.__dict__.keys():
			if not validate_path(self.main_blueprint):
				logging.error("Blueprint \"{}\" has invalid main_blueprint value \"{}\"".format(self.name, self.main_blueprint))
				result = False
		else:
			if not os.path.isfile("{}/{}".format(self.path, "blueprint.yaml")):
				logging.error("Blueprint \"{}\" doesn't have blueprint.yaml file in the path \'{}\"".format(self.name, self.path))
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
		result = True
		mandatory_fields = ["name", "target_path", "blueprints"]
		for mandatory_filed in mandatory_fields:
			if mandatory_filed not in self.__dict__.keys():
				logging.error("Topic \"{}\" is missing a mandatory field {}".format(self.name, mandatory_filed))
				result = False
		return result

	def validate_blueprints_ids_unique(self) -> bool:
		result = False
		blueprints_ids = []
		if "blueprints" in self.__dict__.keys():
			for blueprint in self.blueprints:
				if blueprint.id in blueprints_ids:
					logging.error("Topic \"{}\" has multiple blueprints with the same id \"{}\" already exist".format(self.name, blueprint.id))
					result = False
				else:
					blueprints_ids.append(blueprint.id)
		return False

	def validate(self) -> bool:
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

	def validate_mandatory_fields(self) -> bool:
		result = True
		mandatory_fileds = [S3_BASE_URL, S3_BUCKET_NAME, S3_BUCKET_DIRECTORY, GIT_URL, TARGET_PATH, GITHUB_URL, RAW_GITHUB_URL]
		for mandatory_filed in mandatory_fileds:
			if mandatory_filed not in self.__dict__.keys():
				logging.error("mandatory filed {} is missing".format(mandatory_filed))
				result = False
		return result

	def validate_topics_names_unique(self) -> bool:
		result = True
		topic_names = []
		for topic in self.topics:
			if topic.name in topic_names:
				logging.error("topic \"{}\" already existis".format(topic.name))
				result = False
			else:
				topic_names.append(topic.name)
		return False

	def validate(self) -> bool:
		result = True
		result = result or self.validate_mandatory_fields()
		if not validate_url(self.s3_base_url):
			logging.error("s3_base_url is not a valid URL")
			result = False
		if not validate_id_value(self.s3_bucket_name):
			logging.error("s3_bucket_name value \"{}\" is not valid".format(self.s3_bucket_name))
			result = False
		if not validate_path(self.s3_bucket_directory):
			logging.error("s3_bucket_directory value \"{}\" is not a valid path".format(self.s3_bucket_directory))
			result = False
		if not validate_url(self.git_url):
			logging.error("git_url value \"{}\" is not a valid url".format(self.git_url))
			result = False
		if not validate_url(self.target_path):
			logging.error("target_path value \"{}\" is not a valud url".format(self.target_path))
			result = False
		if not validate_url(self.github_url):
			logging.error("github_url value \"{}\" is not a valid url".format(self.github_url))
			result = False
		if not validate_url(self.raw_github_url):
			logging.error("raw_github_url value \"{}\" is not a valid url".format(self.raw_github_url))
			result = False
		self.validate_topics_names_unique()
		for topic in self.topics:
			if not topic.validate():
				result = False
		return result

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
