pipeline {
  agent any

  parameters {
    booleanParam(name: 'RUN_SONAR', defaultValue: true, description: 'Run SonarQube analysis and enforce its quality gate')
    booleanParam(name: 'PUBLISH_IMAGE', defaultValue: false, description: 'Push the built image to Docker Hub after all checks pass')
    string(name: 'IMAGE_REPOSITORY', defaultValue: '', description: 'Docker Hub repository, for example username/lost-item-intelligence-network; required when publishing')
  }

  tools {
    jdk 'jdk21'
    maven 'maven3'
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script {
          env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(12)}"
        }
      }
    }

    stage('Maven Verify and JUnit') {
      steps {
        script {
          if (isUnix()) {
            sh 'mvn -B clean verify'
          } else {
            bat 'mvn -B clean verify'
          }
        }
      }
    }

    stage('SonarQube Analysis') {
      when { expression { params.RUN_SONAR } }
      steps {
        withSonarQubeEnv('sonarqube') {
          withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
            script {
              if (isUnix()) {
                sh 'mvn -B sonar:sonar -Dsonar.host.url="$SONAR_HOST_URL" -Dsonar.qualitygate.wait=false'
              } else {
                bat 'mvn -B sonar:sonar -Dsonar.host.url="%SONAR_HOST_URL%" -Dsonar.qualitygate.wait=false'
              }
            }
          }
        }
      }
    }

    stage('SonarQube Quality Gate') {
      when { expression { params.RUN_SONAR } }
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          def repository = params.IMAGE_REPOSITORY?.trim()
          if (params.PUBLISH_IMAGE && !repository) {
            error('Set IMAGE_REPOSITORY to a Docker Hub repository before enabling PUBLISH_IMAGE.')
          }
          if (repository && !(repository ==~ /[a-z0-9]+(?:[._-][a-z0-9]+)*(?:\/[a-z0-9]+(?:[._-][a-z0-9]+)*)*/)) {
            error('IMAGE_REPOSITORY must use lowercase Docker Hub namespace/name characters.')
          }
          env.IMAGE_NAME = repository ?: 'lost-item-intelligence-network'
          if (isUnix()) {
            sh 'docker build --pull -t "$IMAGE_NAME:$IMAGE_TAG" .'
          } else {
            bat 'docker build --pull -t "%IMAGE_NAME%:%IMAGE_TAG%" .'
          }
        }
      }
    }

    stage('Publish Docker Image') {
      when { expression { params.PUBLISH_IMAGE } }
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'REGISTRY_USERNAME', passwordVariable: 'REGISTRY_PASSWORD')]) {
          script {
            try {
              if (isUnix()) {
                sh '''
                  set +x
                  printf '%s' "$REGISTRY_PASSWORD" | docker login --username "$REGISTRY_USERNAME" --password-stdin
                  docker push "$IMAGE_NAME:$IMAGE_TAG"
                '''
              } else {
                powershell '''
                  $ErrorActionPreference = 'Stop'
                  $env:REGISTRY_PASSWORD | docker login --username $env:REGISTRY_USERNAME --password-stdin
                  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                  docker push "${env:IMAGE_NAME}:$env:IMAGE_TAG"
                  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                '''
              }
            } finally {
              if (isUnix()) {
                sh 'docker logout >/dev/null 2>&1 || true'
              } else {
                powershell '$ErrorActionPreference = "SilentlyContinue"; docker logout | Out-Null; exit 0'
              }
            }
          }
        }
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml'
      archiveArtifacts allowEmptyArchive: true, artifacts: 'target/*.jar,target/site/jacoco/**'
    }
  }
}
