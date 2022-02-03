import os
import yaml
import json
import shutil
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

with open("catalog.yaml", 'r') as stream:
    try:
        catalog = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

git_url = catalog['git_url']
target_path = catalog['target_path']
github_url = catalog['github_url']

def get_zip_url(blueprint):
	zip_url = blueprint['zip_url'] if 'zip_url' in blueprint.keys() else None

	if zip_url is None and 'path' in blueprint:
		path = blueprint['path'][0:blueprint['path'].rfind("/")]
		filename_path = ("%s/%s") % (path, blueprint['id'])
		zip_url = "{}/{}.zip".format(target_path, filename_path)

	return zip_url

def get_html_url(blueprint):
	html_url = blueprint['html_url'] if 'html_url' in blueprint.keys() else None

	if html_url is None and 'path' in blueprint.keys():
		path = blueprint['path'][0:blueprint['path'].rfind("/")]
		html_url = "{}/{}".format(github_url, path)

	return html_url

for package in catalog['topics']:
	catalog = []
	logging.info('processing catalog %s' % package['name'])
	if 'blueprints' in package:
		result = []
		

		for blueprint in package['blueprints']:
			zip_url = get_zip_url(blueprint)
			html_url = get_html_url(blueprint)

			if 'path' in blueprint:
				path = blueprint['path'][0:blueprint['path'].rfind("/")]
				dir_name = blueprint['path'][blueprint['path'].rfind("/")+1:]

				output_filename = ("build/%s/%s") % (path, blueprint['id'])	


				shutil.make_archive(output_filename, 'zip', path, dir_name)

				filename_path = ("%s/%s") % (path, blueprint['id'])	

			logging.info("processing blueprint %s" % blueprint['id'])

			catalog_item = {
			  "id": blueprint['id'],
			  "name": blueprint['name'],
			  "description": blueprint['description'],
			  "html_url": html_url,
			  # "zip_url": ("%s/%s.zip") % (target_path, blueprint['id']),
			  "zip_url": zip_url,
			  "readme_url": blueprint['readme_url'],
			  "main_blueprint": blueprint['main_blueprint'],
			  "image_url": blueprint["image_url"],
			  "crated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
			  "updated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
			}
			catalog.append(catalog_item)

		json_object = json.dumps(catalog, indent=4)
		catalog_filename = "build/catalogs/%s.json" % package['name']
		# catalog_filename = "build/%s.json" % package['name']
		if not os.path.exists("build/catalogs"):
			os.mkdir("build/catalogs")
		with open(catalog_filename, "w+") as outfile:
			outfile.write(json_object)