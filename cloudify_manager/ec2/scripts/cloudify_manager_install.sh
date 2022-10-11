#!/usr/bin/env bash


# Script takes the following inputs:
# - LICENSE - valid license for the Cloudify Manager
# - PRIVATE_IP - private IP of the host VM
# - PUBLIC_IP - public IP of the host VM
# - ADMIN_PASSWORD - password to set for the Cloudify Manager's admin user

RPM_NAME='cloudify-manager-install.rpm'

curl ${CM_RPM_URL} -o ${RPM_NAME}
sudo yum install -y ${RPM_NAME}

sudo cfy_manager install \
    --private-ip "${PRIVATE_IP}" \
    --public-ip "${PUBLIC_IP}" \
    --admin-password "${ADMIN_PASSWORD}"