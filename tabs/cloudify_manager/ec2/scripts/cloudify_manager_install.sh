#!/usr/bin/env bash


# Script takes the following inputs:
# - CM_RPM_URL - the rpm for manager installation
# - PRIVATE_IP - private IP of the host VM
# - PUBLIC_IP - public IP of the host VM
# - ADMIN_PASSWORD - password to set for the Cloudify Manager's admin user


RPM_NAME='cloudify-manager-install.rpm'

curl "${CM_RPM_URL}" -o ${RPM_NAME}
sudo yum install -y ${RPM_NAME}
sudo yum update -y && sudo yum install -y openssl-1.0.2k libselinux-utils \
   logrotate python-setuptools python-backports \
   python-backports-ssl_match_hostname which cronie \
   systemd-sysv initscripts tcp_wrappers-libs openssh-clients sudo

sudo cfy_manager install \
    --private-ip "${PRIVATE_IP}" \
    --public-ip "${PUBLIC_IP}" \
    --admin-password "${ADMIN_PASSWORD}"