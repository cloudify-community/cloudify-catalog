import os
import yaml
import json
import shutil
import logging
import datetime

with open("catalog.yaml", 'r') as stream:
    try:
        catalog = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

logging.basicConfig(level=logging.DEBUG)
git_url = catalog['git_url']
target_path = catalog['target_path']
for package in catalog['topics']:
	catalog = []
	logging.info('processing catalog %s' % package['name'])
	if 'blueprints' in package:
		result = []
		for blueprint in package['blueprints']:
			logging.info("processing blueprint %s" % blueprint['id'])
			catalog_item = {
			  "id": blueprint['id'],
			  "name": blueprint['name'],
			  "description": blueprint['description'],
			  "html_url": blueprint['html_url'],
			  # "zip_url": ("%s/%s.zip") % (target_path, blueprint['id']),
			  "zip_url": blueprint['zip_url'],
			  "readme_url": blueprint['readme_url'],
			  "main_blueprint": blueprint['main_blueprint'],
			  "image_url": blueprint["image_url"],
			  "crated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
			  "updated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
			}
			catalog.append(catalog_item)
			if 'path' in blueprint:
				path = blueprint['path'][0:blueprint['path'].rfind("/")]
				dir_name = blueprint['path'][blueprint['path'].rfind("/")+1:]

				output_filename = ("build/%s/%s") % (path, blueprint['id'])				
				

				shutil.make_archive(output_filename, 'zip', path, dir_name)

		json_object = json.dumps(catalog, indent=4)
		catalog_filename = "build/catalogs/%s.json" % package['name']
		# catalog_filename = "build/%s.json" % package['name']
		if not os.path.exists("build/catalogs"):
			os.mkdir("build/catalogs")
		with open(catalog_filename, "w+") as outfile:
			outfile.write(json_object)