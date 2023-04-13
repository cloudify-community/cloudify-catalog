import os
import sys
import shutil
import zipfile
import yaml
from os.path import dirname
from string import ascii_lowercase

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.utils import id_generator
from jinja2 import Environment, FileSystemLoader

def _handle_parent_directory(into_dir):
    extracted_files = os.listdir(into_dir)
    ctx.logger.info(extracted_files)
    if len(extracted_files) == 1:
        inner_dir = os.path.join(into_dir, extracted_files[0])
        if os.path.isdir(inner_dir):
            return inner_dir
    return into_dir

def unzip_archive(archive_path, skip_parent_directory=True):
    """
    Unzip a zip archive.
    this method memic strip components
    """
    into_dir = dirname(__file__)
    ctx.logger.info("Unzipping to {}".format(into_dir))
    zip_in = None
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(into_dir)
            for info in zip_ref.infolist():
                reset_target = os.path.join(into_dir, info.filename)
                if info.external_attr >> 16 > 0:
                    os.chmod(reset_target, info.external_attr >> 16)
        if skip_parent_directory:
            into_dir = _handle_parent_directory(into_dir)
    except zipfile.BadZipFile as e:
        # clean up that temp directory and raise the exception
        shutil.rmtree(into_dir)
        raise e
    finally:
        if zip_in:
            zip_in.close()
            os.remove(archive_path)
    return into_dir

class_path = ctx.download_resource('scripts/templates.zip')
unziped_class = unzip_archive(class_path, False)

ctx.instance.runtime_properties['value'] =  id_ = id_generator(size=6, chars=ascii_lowercase)

ports = inputs["ports"]
provider = inputs["provider"]

if provider == 'aws':
    rules = [ {"from_port" : port, "to_port" : port } for port in ports ]
elif provider == 'azure':
    rules = [ {"port" : port, "description" : f"Access rule #{i}", \
               "name" : f"Rule #{i}", "prority" : str(101+i) } for i, port in enumerate(ports) ]

path = os.path.join(unziped_class, 'templates/')
environment = Environment(loader=FileSystemLoader(path), autoescape = True)

results_filename = "{}.j2".format(provider)
results_template = environment.get_template(results_filename)

context = {
    "rules": rules
}

ctx.instance.runtime_properties['value'] = yaml.safe_load(results_template.render(context))


