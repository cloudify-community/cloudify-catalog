import logging

NO_SPACES_ERROR_MESSAGE = "Blueprint property {} value can't have spaces, the value is \"{}\""
EMPTY_VALUE_ERROR_MESSAGE = "Blueprint property {} value can't be empty"
URL_ERROR_MESSAGE = "Blueprint property {} value must be a valid URL, the value is \"{}\""
YAML_FILE_ERROR_MESSAGE = "Blueprint property {} value must be a path to a yaml file, the value is \"{}\""
DATE_ERROR_MESSAGE = "Blueprint property {} value must be a value, the value is \"{}\""

# logging.basicConfig(level=logging.DEBUG)
# logging.info('processing catalog %s' % package['name'])

def contains_space(value: str) -> bool:
	return " " in value

def is_empty(value: str) -> bool:
	return value is None or value.strip() == ""

def is_url(value: str) -> bool:
	# TODO replace with a proper regex
	pattern = re.compile("(http|https}:\\/\\/.+")
	return re.match(pattern, value):

def is_yaml_file(value: str) -> bool:
	#TODO replace with a propert path validation
	pattern = re.compile("(\\w+\\/)*[\\w_\\-]+\\.yaml")
	return re.match(pattern, value)

class Blueprint:
	def __init__(self, 
		id:  str, name: str, description: str, html_url: str, zip_url: str, readme_url: str, 
		main_blueprint: str, image_url: str):
		self.id: str = id
		self.name: str = name
		self.description: str = description
		self.html_url: str = html_url
		self.zip_url: str = zip_url
		self.readme_url: str = readme_url
		self.main_blueprint: str = main_blueprint
		self.image_url: str = image_url
		# self.created_at: str = created_at
		# self.updated_at: str = updated_at

	def validate_id(self):
		if is_empty(self.id):
			logging.error(EMPTY_VALUE_ERROR_MESSAGE.format("id"))
		if contains_space(self.id):
			logging.error(NO_SPACES_ERROR_MESSAGE.format("id", self.id))

	def validate_name(self):
		if is_empty(self.name):
			logging.error(EMPTY_VALUE_ERROR_MESSAGE.format("name"))
		if contains_space(self.name):
			logging.error(NO_SPACES_ERROR_MESSAGE.format("name", self.name))

	def validate(self):
		self.validate_id()
		self.validate_name()
		if not is_url(self.html_url):
			logging.error(URL_ERROR_MESSAGE.format("html_url", self.html_url))
		
		if not is_url(self.readme_url):
			logging.error(URL_ERROR_MESSAGE.format("readme_url", self.readme_url))

		if not is_url(self.image_url):
			logging.error(URL_ERROR_MESSAGE.format("image_url", self.image_url))

		validate_yaml_filve(self.main_blueprint)

		# validate_date(self.created_at)
		# validate_date(self.updated_at)

http://test.test.co/asdf

