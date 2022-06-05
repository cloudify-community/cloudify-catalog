def configuration = [vaultUrl: "${VAULT_URL}",  vaultCredentialId: "vault-app-role", engineVersion: 2]

def secrets = [
  [path: 'secret/jenkins/cloudifyaws', engineVersion: 2, secretValues: [
    [envVar: 'AWS_MANAGER_USERNAME', vaultKey: 'username'],
    [envVar: 'AWS_MANAGER_TENANT', vaultKey: 'tenant'],
    [envVar: 'AWS_MANAGER_IP', vaultKey: 'ip'],
    [envVar: 'AWS_MANAGER_PASSWORD', vaultKey: 'password']]],
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
            containers:
              - name: jnlp
                image: jenkins/inbound-agent:4.3-4
                resources:
                  limits:
                    cpu: 0.3
                    memory: 256Mi
              - name: python
                image: python:3.8
                resources:
                  requests:
                    cpu: 0.5
                    memory: 1Gi
                  limits:
                    cpu: 1
                    memory: 1Gi
                command:
                - cat
                tty: true
                securityContext:
                  runAsUser: 0
                  privileged: true
              - name: cloudify
                image: 263721492972.dkr.ecr.eu-west-1.amazonaws.com/cloudify-python3.6
                volumeMounts:
                - mountPath: /dev/shm
                  name: dshm
                command:
                - cat
                tty: true
                resources:
                  requests:
                    cpu: 0.5
                    memory: 1Gi
                  limits:
                    memory: 1Gi
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
  environment {
    PROJECT = 'cloudify-catalog'
    WORKSPACE = "${env.WORKSPACE}"
  }
  stages{
    stage('prepare'){
      steps {
        script{ 
          container('cloudify'){
            dir("${env.WORKSPACE}/${env.PROJECT}"){
              common = load "common.groovy"
            }
          }
        }
      }
    }
    stage('install dependencies'){
      steps {
        container('python'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            sh """
              set -eux
              pip install --upgrade pip
              pip install -r requirements.txt
            """
          }
        }
      }
    }
    stage('validate_catalog_yaml'){
      steps{
        container('python'){
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
        container('python'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            setupGithubSSHKey()
            sh """
              python catalog.py
            """
          }
        }
      }
    }
    stage('validate_built_catalogs'){
      steps{
        container('python'){
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
              container('python'){
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

    stage('Deploy Cloudify Manager') {
      steps {
        script {
          buildState = 'FAILURE'
          catchError(message: 'Failure on: Deploy Cloudify Manager', buildResult: 'SUCCESS', stageResult:
          'FAILURE') {
            container('python') {
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
  }
}