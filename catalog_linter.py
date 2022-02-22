import re
import yaml
import logging
import validators

from os import listdir
from os.path import isfile, join


NO_SPACES_ERROR_MESSAGE = "Blueprint property {} value can't have spaces, the value is \"{}\""
EMPTY_VALUE_ERROR_MESSAGE = "Blueprint property {} value can't be empty"
URL_ERROR_MESSAGE = "Blueprint property {} value must be a valid URL, the value is \"{}\""
YAML_FILE_ERROR_MESSAGE = "Blueprint property {} value must be a path to a yaml file, the value is \"{}\""
DATE_ERROR_MESSAGE = "Blueprint property {} value must be a value, the value is \"{}\""

# logging.basicConfig(level=logging.DEBUG)
# logging.info('processing catalog %s' % package['name'])

def validate_id_value(value: str) -> bool:
	regexp = re.compile('^[0-9a-zA-Z\-\_]+$')
	return value and regexp.search(value)

def contains_space(value: str) -> bool:
	return " " in value

def is_empty(value: str) -> bool:
	return value is None or value.strip() == ""

def validate_url(value: str) -> bool:
	return value is not None and validators.url(value)

def validate_blueprint_path(value: str) -> bool:
	regexp = re.compile('^[0-9a-zA-Z\-\_\/]+\w+\.yaml$')
	return value and regexp.search(value)

class Blueprint:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def validate_mandatory_fields(self):
		mandatory_fields = [
			"id", "name", "description", "html_url", 
			"zip_url", "readme_url", "main_blueprint", 
			"image_url", "created_at", "updated_at"
			]
	def validate_id(self):
		if is_empty(self.id):
			logging.error(EMPTY_VALUE_ERROR_MESSAGE.format("id"))
		if contains_space(self.id):
			logging.error(NO_SPACES_ERROR_MESSAGE.format("id", self.id))

	def validate_name(self) -> bool:
		if is_empty(self.name):
			logging.error(EMPTY_VALUE_ERROR_MESSAGE.format("name"))
		if contains_space(self.name):
			logging.error(NO_SPACES_ERROR_MESSAGE.format("name", self.name))

	def validate(self) -> bool:
		result = True
		if not validate_id_value(self.id):
			logging.error("invalid id value \"{}\"".format(self.id))
			result = False
		if not validate_id_value(self.name):
			logging.error("invalid name value \"{}\"".format(self.name))
			result = False
		if not validate_url(self.html_url):
			logging.error(URL_ERROR_MESSAGE.format("html_url", self.html_url))
			result = False
		
		if not validate_url(self.readme_url):
			logging.error(URL_ERROR_MESSAGE.format("readme_url", self.readme_url))
			result = False

		if not validate_url(self.image_url):
			logging.error(URL_ERROR_MESSAGE.format("image_url", self.image_url))
			result = False

		if not validate_blueprint_path(self.main_blueprint):
			logging.error("invalid main_blueprint value \"{}\"".format(self.main_blueprint))
			result = False

		return result

result = True
catalogs_files = [join('build/catalogs', f) for f in listdir('build/catalogs') if isfile(join('build/catalogs', f))]
for catalog_file in catalogs_files:
	with open(catalog_file, 'r') as stream:
		try:
			catalog = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			logging.error(exc)
			logging.error("Failed to process {} file".format(catalog_file))
			continue
	for item in catalog:
		blueprint = Blueprint(**item)
		if not blueprint.validate():
			result = False
if not result:
	exist(1)



