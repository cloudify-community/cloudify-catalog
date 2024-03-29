#!/usr/bin/env bash


set -e

sudo bash -c "echo 'sanity: True' > /opt/manager/sanity_mode"
sudo chown cfyuser. /opt/manager/sanity_mode

export PYTHONPATH='/opt/cfy/lib/python3.6/site-packages:'$PYTHONPATH

AWS_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-aws-plugin/latest/cloudify_aws_plugin-3.0.5-centos-Core-py36-none-linux_x86_64.wgn'
AWS_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-aws-plugin/latest/v2_plugin.yaml'
GCP_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-gcp-plugin/1.8.1/cloudify_gcp_plugin-1.8.1-centos-Core-py36-none-linux_x86_64.wgn'
GCP_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-gcp-plugin/1.8.1/plugin.yaml'
TERRAFORM_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-terraform-plugin/latest/cloudify_terraform_plugin-0.18.16-centos-Core-py36-none-linux_x86_64.wgn'
TERRAFORM_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-terraform-plugin/latest/v2_plugin.yaml'
ANSIBLE_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-ansible-plugin/latest/cloudify_ansible_plugin-2.13.7-centos-Core-py36-none-linux_x86_64.wgn'
ANSIBLE_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-ansible-plugin/latest/v2_plugin.yaml'
DOCKER_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-docker-plugin/2.0.5/cloudify_docker_plugin-2.0.5-centos-Core-py36-none-linux_x86_64.wgn'
DOCKER_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-docker-plugin/2.0.5/v2_plugin.yaml'
FABRIC_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-fabric-plugin/2.0.13/cloudify_fabric_plugin-2.0.13-centos-Core-py36-none-linux_aarch64.wgn'
FABRIC_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-fabric-plugin/2.0.13/plugin.yaml'
UTILITIES_WAGON_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-utilities-plugin/latest/cloudify_utilities_plugin-1.25.7-centos-Core-py36-none-linux_x86_64.wgn'
UTILITIES_PLUGIN_YAML_URL='http://repository.cloudifysource.org/cloudify/wagons/cloudify-utilities-plugin/latest/v2_plugin.yaml'

TERRAFORM_REPO_URL='https://github.com/Cloudify-PS/wwt-tf-templates/archive/refs/heads/master.zip'
EAAS_POC_ZIP_URL='https://github.com/Cloudify-PS/wwt-eaas-poc/archive/refs/heads/main.zip'
EAAS_POC_URL='https://github.com/Cloudify-PS/wwt-eaas-poc.git'
BACKSTAGE_ENTITY_PUSH_BLUEPRINT_ZIP_URL='https://github.com/Cloudify-PS/backstage-entity-generation/archive/refs/heads/main.zip'
BACKSTAGE_ENTITY_REPO_NAME=`echo ${backstage_entities_repo_url##*/} | cut -d '.' -f 1`


cfy plugins upload -y ${AWS_PLUGIN_YAML_URL} ${AWS_WAGON_URL}
cfy plugins upload -y ${GCP_PLUGIN_YAML_URL} ${GCP_WAGON_URL}
cfy plugins upload -y ${TERRAFORM_PLUGIN_YAML_URL} ${TERRAFORM_WAGON_URL}
cfy plugins upload -y ${ANSIBLE_PLUGIN_YAML_URL} ${ANSIBLE_WAGON_URL}
cfy plugins upload -y ${DOCKER_PLUGIN_YAML_URL} ${DOCKER_WAGON_URL}
cfy plugins upload -y ${FABRIC_PLUGIN_YAML_URL} ${FABRIC_WAGON_URL}
cfy plugins upload -y ${UTILITIES_PLUGIN_YAML_URL} ${UTILITIES_WAGON_URL}

cfy secrets create aws_access_key_id -s ${aws_access_key_id}
cfy secrets create aws_secret_access_key --hidden-value -s ${aws_secret_access_key}
cfy secrets create cloudify_host -s ${cloudify_host}
cfy secrets create cloudify_user -s ${cloudify_user}
cfy secrets create cloudify_password --hidden-value -s ${cloudify_password}
cfy secrets create github_token --hidden-value -s ${github_token}
cfy secrets create github_username --hidden-value -s ${github_username}
cfy secrets create runner_host -s ${runner_host}
cfy secrets create runner_vm_user -s ${runner_vm_user}
cfy secrets create runner_root_user -s ${runner_root_user}
cfy secrets create runner_key_private --hidden-value -s "${runner_key_private}"
cfy secrets create eaas_params -s "{
        \"aws\": {
            \"blueprint\": \"aws-nginx\",
            \"deployment\": \"aws-nginx-prod\",
            \"message\": \"Production on AWS\",
            \"inputs\": {
                \"instance_type\": \"t3.large\",
                \"vpc_cidr\": \"10.0.0.0/16\",
                \"subnet_cidr\": \"10.0.1.0/24\",
                \"aws_region_name\": \"${region_name}\"
                }
        },
        \"gcp\": {
            \"blueprint\": \"gcp-nginx\",
            \"deployment\": \"gcp-nginx-prod\",
            \"message\": \"Production on GCP\",
            \"inputs\": {
                \"project_id\": \"wwt-poc\",
                \"zone_name\": \"us-west1-a\",
                \"prefix\": \"cfy-prod\",
                \"instance_type\": \"e2-standard-2\"
                }
        }
    }"

sudo yum install -y zip
git clone ${EAAS_POC_URL}
cd wwt-eaas-poc/
zip -r aws_nginx.zip aws/

cfy blueprints upload -b aws-nginx -n aws-nginx.yaml aws_nginx.zip
cfy blueprints upload -b terraform-repository ${TERRAFORM_REPO_URL}
cfy blueprints upload -b eaas_poc -n eaas.yaml ${EAAS_POC_ZIP_URL}

cd /tmp
git clone https://${github_token}@${backstage_entities_repo_url}
chmod -R 777 /tmp/${BACKSTAGE_ENTITY_REPO_NAME}
cd /tmp/${BACKSTAGE_ENTITY_REPO_NAME}
git config user.name ${github_username}
rm -rf wwt-eaas-poc

cfy install -b backstage_entity_push \
            -n blueprint.yaml \
            -d backstage_entity_push \
            -i "cloudify_manager_host=${cloudify_host}" \
            -i "repo_path=/tmp/${BACKSTAGE_ENTITY_REPO_NAME}" \
            -i "repo_url=${backstage_entities_repo_url}" \
            -i "branch_name=main" \
            ${BACKSTAGE_ENTITY_PUSH_BLUEPRINT_ZIP_URL}

sudo rm /opt/manager/sanity_mode