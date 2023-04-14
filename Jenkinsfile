def configuration = [vaultUrl: "${VAULT_URL}",  vaultCredentialId: "vault-app-role", engineVersion: 2]

def secrets = [
  [path: 'secret/jenkins/cloudifyaws', engineVersion: 2, secretValues: [
    [envVar: 'AWS_MANAGER_USERNAME', vaultKey: 'username'],
    [envVar: 'AWS_MANAGER_TENANT', vaultKey: 'tenant'],
    [envVar: 'AWS_MANAGER_IP', vaultKey: 'ip'],
    [envVar: 'AWS_MANAGER_PASSWORD', vaultKey: 'password']]
  ],
  [path: 'secret/jenkins/aws', engineVersion: 2, secretValues: [
    [envVar: 'AWS_ACCESS_KEY_ID', vaultKey: 'aws_access_key_id'],
    [envVar: 'AWS_SECRET_ACCESS_KEY', vaultKey: 'aws_secret_access_key']]
  ],
  [path: 'secret/jenkins/cloudify', engineVersion: 2, secretValues: [
    [envVar: 'LICENSE', vaultKey: 'license']]
  ],
  [path: 'secret/jenkins/infracost', engineVersion: 2, secretValues: [
    [envVar: 'INFRACOST_API_KEY', vaultKey: 'api_key']]
  ],
  [path: 'secret/jenkins/catalog', engineVersion: 2, secretValues: [
    [envVar: 'GH_TOKEN', vaultKey: 'gh_token']]
  ]
]

@Library('pipeline-shared-library') _

pipeline{
  agent{
    kubernetes{
      defaultContainer 'jnlp'
      yaml '''
          spec:
            volumes:
              - name: dshm
                emptyDir:
                  medium: Memory
              - name: shared-data-volume
                peristentVolumeClaim:
                  claimName: shared-data
            containers:
              - name: jnlp
                image: jenkins/inbound-agent:4.11.2-2
                resources:
                  limits:
                    cpu: 0.3
                    memory: 256Mi
              - name: cloudify
                image: 263721492972.dkr.ecr.eu-west-1.amazonaws.com/cloudify-python3.10
                volumeMounts:
                  - mountPath: /tmp/data
                    name: shared-data-volume
                command:
                - cat
                tty: true
                resources:
                  requests:
                    cpu: 1.0
                    memory: 3Gi
                  limits:
                    memory: 3.5Gi
                securityContext:
                  runAsUser: 0
                  privileged: true
            nodeSelector:
              instance-type: spot
          '''
    }
  }
  options {
    checkoutToSubdirectory('cloudify-catalog')
    buildDiscarder(logRotator(numToKeepStr:'10'))
    timeout(time: 60, unit: 'MINUTES')
    timestamps()
  }

  triggers {
    cron(env.BRANCH_NAME == '6.4.0-build' ? '0 */12 * * *' : '')
  }

  parameters {
    string(name: 'TEST_BLUEPRINT', defaultValue: '', description: 'Blueprint ID to test.')
    choice(name: 'TEST_CASE', choices: "upload\ninstall\nsingle_upload\nsingle_install", description: 'Test case type, applicable only if TEST_BLUEPRINTS set to true, single_{option} takes into account the value from TEST_BLUEPRINT')
    choice(name: 'BPS_SCOPE', choices: "changed\nall", description: 'Test all or only changed bps from Pull Request.')
  }

  environment {
    PROJECT = 'cloudify-catalog'
    WORKSPACE = "${env.WORKSPACE}"
    BP_ID = "ec2-cloudify-catalog-blueprint-${env.GIT_BRANCH}-${env.BUILD_NUMBER}"
    SUFFIX = "6.4.0-.dev1"
    BPS_SCOPE = "${params.BPS_SCOPE}"
    TEST_CASE = "${params.TEST_CASE}"
    TEST_BLUEPRINT = "${params.TEST_BLUEPRINT}"
    TEST_RESULT_DIR = "/tmp/data"
    TEST_RESULT_PATH = "${env.TEST_RESULT_DIR}/junit_report.xml"
    EC2_META_DATA = "http://169.254.169.254/latest/meta-data/"
  }

  stages{
    stage('prepare'){
      steps {
        script{
          container('cloudify'){
            dir("${env.WORKSPACE}/${env.PROJECT}"){
              common = load "common.groovy"
              sh """
                set -eux
                pip install --upgrade pip
                pip install -r requirements.txt
                curl -sfL https://cloudify.co/get-lint | sh -
                export TEST_RESULT_PATH=${env.TEST_RESULT_PATH}
                export GH_TOKEN=${env.GH_TOKEN}
                export BPS_SCOPE=${env.BPS_SCOPE}
            """
            }
          }
        }
      }
    }
    stage('validate_catalog_yaml'){
      steps{
        container('cloudify'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            sh """
              python catalog_definition_linter.py
            """
          }
        }
      }
    }
    stage('build'){
      steps{
        container('cloudify'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            withVault([configuration: configuration, vaultSecrets: secrets]){
              setupGithubSSHKey()
              sh """
              python catalog.py
              """
            }
          }
        }
      }
    }
    stage('validate_built_catalogs'){
      steps{
        container('cloudify'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            setupGithubSSHKey()
            sh """
              python catalog_linter.py
            """
          }
        }
      }
    }
    stage('test'){
      when { 
        anyOf {
          expression {
            container('cloudify'){
              dir("${env.WORKSPACE}/${env.PROJECT}"){
                withVault([configuration: configuration, vaultSecrets: secrets]){
                  common.checkChanges().trim() != '0' 
                }
              }
            }
          }
          expression { params.BPS_SCOPE == 'all' }
        }
      }
      stages {
        stage('run_cfy_lint_cm_tests'){
          parallel{
            stage('run_cfy_lint'){
              steps{
                container('cloudify'){
                  dir("${env.WORKSPACE}/${env.PROJECT}"){
                    withVault([configuration: configuration, vaultSecrets: secrets]){
                      script{
                        catchError(message: 'Failure on: Test cfy lint', buildResult: 'SUCCESS', stageResult:
                      'FAILURE') {
                          common.runCfyLinter()
                        }
                      }
                    }
                  }
                }
              }
            }
            stage('run_cm_tests'){
              stages {
                stage('deploy_cloudify_manager') {
                  steps {
                    script {
                      buildState = 'FAILURE'
                      catchError(message: 'Failure on: Deploy Cloudify Manager', buildResult: 'SUCCESS', stageResult:
                      'FAILURE') {
                        container('cloudify') {
                          setupGithubSSHKey()
                          dir("${env.WORKSPACE}/${env.PROJECT}") {
                            withVault([configuration: configuration, vaultSecrets: secrets]){
                              echo 'Create EC2 instance'
                              common.createEc2Instance()
                              echo 'Configure Cloudify Manager'
                              common.configureCloudifyManager()
                            }
                          }
                        }
                        // If we reach here that means all of the above passed
                        buildState = 'SUCCESS'
                      }
                    }
                  }
                }
                stage('test_blueprints'){
                  steps {
                    script {
                      buildState = 'FAILURE'
                      catchError(message: 'Failure on: Test blueprints', buildResult: 'SUCCESS', stageResult:
                      'FAILURE') {
                        container('cloudify') {
                          dir("${env.WORKSPACE}/${env.PROJECT}") {
                            withVault([configuration: configuration, vaultSecrets: secrets]){
                              echo 'Test blueprints'
                              common.testBlueprints()
                            }
                          }
                          // If we reach here that means all of the above passed
                          buildState = 'SUCCESS'
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    stage('upload_artifacts'){
      steps{
        withCredentials([
          usernamePassword(
              credentialsId: 'aws-cli',
              usernameVariable: 'ID',
              passwordVariable: 'SECRET'
              )]) {
          container('cloudify'){
            dir("${env.WORKSPACE}/${env.PROJECT}"){
              setupGithubSSHKey()
              sh '''
                export ID="$ID"
                export SECRET="$SECRET"
                python upload_artifacts.py
              '''
            }
          }
        }
      }
    }
  }
}