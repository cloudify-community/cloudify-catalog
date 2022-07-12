def createEc2Instance(){
  sh """#!/bin/bash
    set -euxo pipefail
    python -m venv .venv
    source .venv/bin/activate

    cfy profile use ${env.AWS_MANAGER_IP} -u ${env.AWS_MANAGER_USERNAME} -p ${env.AWS_MANAGER_PASSWORD} -t ${env.AWS_MANAGER_TENANT} --ssl

    pushd 'bp'
      cfy install -b ${env.BP_ID} -i cloudify_manager_suffix=${env.SUFFIX} ec2-cloudify-catalog-blueprint.yaml
    popd

    cfy deployments capabilities ${env.BP_ID} --json > capabilities.json
    jq -r '.key_content.value' capabilities.json > ~/.ssh/ec2_ssh_key && chmod 600 ~/.ssh/ec2_ssh_key
    for i in {1..16}; do ssh-keyscan -H \$(jq -r '.endpoint.value' capabilities.json) >> ~/.ssh/known_hosts && break || sleep 10; done
    echo 'ClientAliveInterval 50' >> /etc/ssh/sshd_config
  """
}

def configureCloudifyManager(){
  sh """#!/bin/bash
    ssh -i ~/.ssh/ec2_ssh_key -l centos \$(cat capabilities.json | jq '.endpoint.value' | tr -d '"') <<'EOT'
for i in {1..16}; do [[ \$(curl https://localhost/api/v3.1/ok --insecure -s) == *"OK"* ]] && break || echo "Waiting for api.." && sleep 10; done\n
cfy_manager configure --private-ip \$(curl ${env.EC2_META_DATA}/local-ipv4) --public-ip \$(curl ${env.EC2_META_DATA}/public-ipv4) -a admin\n
echo ${env.LICENSE} | base64 -d > /tmp/cfy-license.yaml\n
cfy license upload /tmp/cfy-license.yaml
cfy secrets create aws_access_key_id -s ${env.AWS_ACCESS_KEY_ID}
cfy secrets create aws_secret_access_key -s ${env.AWS_SECRET_ACCESS_KEY}
EOT
"""
}

def testBlueprints(){
    sh """#!/bin/bash
    scp -i ~/.ssh/ec2_ssh_key -r * centos@\$(cat capabilities.json | jq '.endpoint.value' | tr -d '"'):/home/centos
    ssh -i ~/.ssh/ec2_ssh_key -l centos \$(cat capabilities.json | jq '.endpoint.value' | tr -d '"') <<'EOT'
sudo pip3 install -U parameterized pyyaml nose rednose
cd /home/centos
nosetests --verbosity=2 --rednose ./ -a type=${env.TEST_CASE} --with-xunit
sudo cp nosetests.xml /tmp/data/nosetests.xml
EOT
"""
}

def terminateCloudifyManager(){
  sh """#!/bin/bash
    source .venv/bin/activate
    dep_id=\$(cfy deployments list | grep ${env.BP_ID} | awk '{ print \$2 }')
    cfy exec start uninstall --force -d \${dep_id}
    cfy dep del -f \${dep_id}
    cfy blu del -f ${env.BP_ID}
  """
}

def checkCoverage(){
  sh """#!/bin/bash
    set -euxo pipefail
    export NVM_DIR='/root/.nvm'
    . "\$NVM_DIR/nvm.sh"

    echo Checking coverage...
    npm run coverageCheck
  """
}

def createPackage(){
  sh """#!/bin/bash
    set -euxo pipefail
    echo "Installing dependencies..."
    apt-get update -y
    apt-get install -y libxcomposite-dev rsync libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb

    export NVM_DIR='/root/.nvm'
    . "\$NVM_DIR/nvm.sh"

    echo "Creating package..."
    npm run beforebuild
    npm run build:coverage
    npm run zip
  """
}


def runComponentTests(){
  sh """#!/bin/bash
    set -euxo pipefail
    export NVM_DIR='/root/.nvm'
    . "\$NVM_DIR/nvm.sh"

    echo Starting cypress components tests...
    export NODE_OPTIONS='--max-old-space-size=8192'
    npm run test:frontend:components
  """
}

def runTests(){
  sh """#!/bin/bash
    set -euxo pipefail
    export MANAGER_PROTOCOL=https
    export MANAGER_IP=\$(cat ${env.WORKSPACE}/pipelines-k8s/system-ui-tests/capabilities.json | jq '.endpoint.value' | tr -d '"')
    export MANAGER_USER=centos
    export SSH_KEY_PATH=~/.ssh/ec2_ssh_key

    export NVM_DIR='/root/.nvm'
    . "\$NVM_DIR/nvm.sh"

    echo "Uploading package..."
    npm run upload

    echo "Starting system tests..."
    npm run e2e -- -s '\${TEST_SPEC:-**/*}'
  """
}

return this