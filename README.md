# Cloudify Catalog

TODO: Add a pipeline to generate the artifacts and upload to S3 bucket

## General

The catalog repo includes all the data requires to generate the catalogs files that are used inside marketplace in CloudifyManager.

There are 3 main components:

`Blueprints` - All the blueprints are located inside the directories.

The directories are structured logically per topics.

Each topic has subdirectory and subdirectory might has other subdirectories.

Each blueprint should be in a dedicated directory and following files should be provided:

`blueprint.yaml` - The blueprint file must be 

`logo.png` - The blueprint log should be 

`README.md` - Describes the 


## The catalog.yaml structure:

### Global Proerties:

`git_url` - The base URL to the catalog git repo

`target_path` - The base URL to the location where the resources will be uploaded

`github_url` - The base URL to the git repository branch

`raw_github_url` - The base URL to raw git repository branch

### Topics Properties

`name` - the catalog name, used as the file name with `json` extension

Let's say the name is `certified_environments` all the blueprints defined in the `blueprints` property will be add to the catalog. The name of the catalog will be `certified_environments.json`

#### Blueprints Properies

Blueprints is an array of the blueprints to be added to the catalog.

Each item in the `blueprints` has the following structure:

`id` - Blueprint ID

`name` - Blueprint Name, the name can't contain spaces

`path` - path to the blueprint directory withing the catalog

`descritpion` - the blueprint description

`html_url` - [Optional] URL to the blueprint page, use if the blueprint is not located within the catalog repo

`zip_url` - [Optional] URL to the blueprint archive, use if the blueprint is not part of the catalog repo

`readme_url` - [Optional] URL to the README file, use if the blueprint is not part of the catalog repo

`main_blueprint` - [Optional] The main blueprint name in archive, the default value is `blueprint.yaml`

`image_url` - [Optional] The URL to the blueprint logo, use if the logo is not provided in the path

## Generated Resources

The catalog items structure:

`id` - Retrieved from the id property

`name` - Retrieved from the name property

`description` - Retrieved from the description property

`html_url` - if `html_url` is not provided, the `html_url` is calculated by concatinating `github_url` and `path`

`zip_url` - if `zip_url` is not provided, the `zip_url` is calculated by concatinating `target_path` and the relative archived location

`readme_url` - if `readme_url` is not provided, the `readme_url` is calculated by concatinating `raw_github_url` the `path` and "README.md"

`main_blueprint` - if `main_blueprint` is not provided the default value "blueprint.yaml" is used

`image_url` - if `image_url` is not provide, the `image_url` is calculated by concatinating `raw_github_url`, `path` and logo.png

`crated_at` - is auto calculated with the current date

`updated_at` - is auto calculated with the current date

## Auto generate

The python that generates all the resources is `catalog.py`.

Create a virtual environment `venv` in the root directory.

In the root directory run:
```
python3 -m venv venv
source venv/bin/activate
```

To run the code it's required to install 2 packages:
```
pip install pyyaml
pip install pygit2
pip install boto3
```

To generate all the resources run the following command:
```
python catalog.py
```

The script will generate all the resources under `build` directory.

All the catalogs will be created in `build/catalogs`

All the blueprint archives will be created in `build/[PATH]/[ID].zip` directory, where the path is the `PATH` and `ID` are properties provided in each blueprint in the `catalog.yaml`
