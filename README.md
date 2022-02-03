#Cloudify Catalog


The catalog global properties:

`git_url` - The base URL to the catalog git repo
`target_path` - The base URL to the location where the resources will be uploaded
`github_url` - The base URL to the git repository branch
`raw_github_url` - The base URL to raw git repository branch


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