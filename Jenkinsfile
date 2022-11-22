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
                    memory: 1Gi
                  limits:
                    memory: 2Gi
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
    booleanParam(name: 'TEST_BLUEPRINTS', defaultValue: true, description: 'Test blueprints from marketplace.')
    choice(name: 'TEST_CASE', choices: "upload\ninstall", description: 'Test case type, applicable only if TEST_BLUEPRINTS set to true.')
  }

  environment {
    PROJECT = 'cloudify-catalog'
    WORKSPACE = "${env.WORKSPACE}"
    BP_ID = "ec2-cloudify-catalog-blueprint-${env.GIT_BRANCH}-${env.BUILD_NUMBER}"
    SUFFIX = "6.4.0-.dev1" 
    TEST_CASE = "${params.TEST_CASE}"
    TEST_RESULT_DIR = "/tmp/data"
    TEST_RESULT_PATH = "${env.TEST_RESULT_DIR}/junit_report.xml"
  }
  stages{
    stage('prepare'){
      when { expression { params.TEST_BLUEPRINTS } }
      steps {
        script{ 
          container('cloudify'){
            dir("${env.WORKSPACE}/${env.PROJECT}"){
              common = load "common.groovy"
              sh """
                set -eux
                pip install --upgrade pip
                pip install -r requirements.txt
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
    stage('deploy_cloudify_manager') {
      when { expression { params.TEST_BLUEPRINTS } }
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
      when { expression { params.TEST_BLUEPRINTS } }
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
    stage('download_test_artifacts'){
      steps{
        script{
          container('cloudify'){
             dir("${env.WORKSPACE}/${env.PROJECT}") {
              echo 'Copy artifacts'
              common.downloadTestReport("/tmp/junit_report.xml", "${env.TEST_RESULT_PATH}")
            }
          }
        }
      }
    }
    stage('build'){
      steps{
        container('cloudify'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            setupGithubSSHKey()
            sh """
            export TEST_RESULT_PATH=${env.TEST_RESULT_PATH}
            python catalog.py
            """
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