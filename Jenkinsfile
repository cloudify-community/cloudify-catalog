def podTemplate = """
                apiVersion: v1
                kind:
                spec:
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
                        cpu: 1
                        memory: 2Gi
                      limits:
                        cpu: 1
                        memory: 2Gi
                    command:
                    - cat
                    tty: true
                    securityContext:
                      runAsUser: 0
                      privileged: true
                  nodeSelector:
                    instance-type: spot
                """.stripIndent().trim()

@Library('pipeline-shared-library') _

pipeline{
  agent{
    kubernetes{
      defaultContainer 'jnlp'
      yaml "${podTemplate}"
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
        withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-key', 
                        usernameVariable: 'USER', 
                        passwordVariable: 'PASS'
                        )]) {
                    sh '''
                        echo "The username is: ${USER}"
                        echo "The password is : ${PASS}"
                    '''
                }
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
        container('python'){
          dir("${env.WORKSPACE}/${env.PROJECT}"){
            setupGithubSSHKey()
            sh """
              python upload_artifacts.py
            """
          }
        }
      }
    }
  }
}