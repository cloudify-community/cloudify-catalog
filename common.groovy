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
cfy secrets create infracost_api_key -s ${env.INFRACOST_API_KEY}
EOT
"""
}

def testBlueprints(){
    sh """#!/bin/bash
    cfy profiles use \$(cat capabilities.json | jq '.endpoint.value' | tr -d '"') -u admin -p admin --skip-credentials-validation --ssl
    export CLOUDIFY_SSL_TRUST_ALL=true
    export PYTHONWARNINGS="ignore:Unverified HTTPS request"
    pytest --capture=sys --verbose --color=yes --code-highlight=yes -m ${env.TEST_CASE} --junitxml=${env.TEST_RESULT_PATH}
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

def checkChanges(){
    sh returnStdout: true, script: """#!/bin/bash
      export GH_TOKEN=${env.GH_TOKEN}
      python3 get_changes.py | wc -l
    """
}

def runCfyLinter(){
  sh """#!/bin/bash
      declare counter=0
      declare regex="\\s+ERROR\\s+"
      for filePath in \$(python3 get_changes.py | grep blueprint.yaml); do
        echo \$filePath
        cfy-lint -b \$filePath |& tee cfy_lint_error.txt;
        declare file_content=\$( cat cfy_lint_error.txt )
        if [[ " \$file_content " =~ \$regex ]] 
          then
              echo "found"
          ((counter+=1))
          echo "There is \$counter not properly formatted blueprint/s"
        fi
      done

      if [[ \$counter -gt 0 ]] 
      then
        echo "Errors found in \$counter blueprint/s."
        exit 1
      else
        echo "No errors found in tested blueprint/s."
        exit 0
      fi
  """
}

return this