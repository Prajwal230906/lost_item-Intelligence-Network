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
        script {
          def checkoutDetails = checkout scm
          env.IMAGE_TAG = "${env.BUILD_NUMBER}-${checkoutDetails.GIT_COMMIT.take(12)}"
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

    stage('Run Application') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'application-db-credentials', usernameVariable: 'DB_USERNAME', passwordVariable: 'DB_PASSWORD')]) {
          script {
            if (isUnix()) {
              sh '''
                docker rm --force lost-item-intelligence-network-ci >/dev/null 2>&1 || true
                docker run --detach --name lost-item-intelligence-network-ci --restart unless-stopped \\
                  --publish 127.0.0.1:8093:8080 \\
                  --add-host=host.docker.internal:host-gateway \\
                  --env 'DB_URL=jdbc:mysql://host.docker.internal:3306/lost_item_network?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC' \\
                  --env DB_USERNAME --env DB_PASSWORD \\
                  "$IMAGE_NAME:$IMAGE_TAG"
              '''
            } else {
              powershell '''
                $ErrorActionPreference = 'Stop'
                docker rm --force lost-item-intelligence-network-ci 2>$null | Out-Null
                docker run --detach --name lost-item-intelligence-network-ci --restart unless-stopped --publish 127.0.0.1:8093:8080 --add-host=host.docker.internal:host-gateway --env 'DB_URL=jdbc:mysql://host.docker.internal:3306/lost_item_network?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC' --env DB_USERNAME --env DB_PASSWORD "${env:IMAGE_NAME}:$env:IMAGE_TAG"
                if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

                $ready = $false
                for ($attempt = 0; $attempt -lt 24; $attempt++) {
                  try {
                    Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:8093/login' -TimeoutSec 5 | Out-Null
                    $ready = $true
                    break
                  } catch {
                    Start-Sleep -Seconds 5
                  }
                }
                if (-not $ready) {
                  docker logs lost-item-intelligence-network-ci
                  throw 'Application did not become ready at http://localhost:8093/login.'
                }
              '''
            }
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
