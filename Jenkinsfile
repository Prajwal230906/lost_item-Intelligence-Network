pipeline {
  agent any
  parameters { booleanParam(name: 'RUN_SONAR', defaultValue: false, description: 'Run analysis when Jenkins has the configured SonarQube server and credential') }
  tools { jdk 'jdk21'; maven 'maven3' }
  options { timestamps(); disableConcurrentBuilds() }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Verify') { steps { sh 'mvn -B clean verify' } }
    stage('SonarQube') {
      when { expression { return params.RUN_SONAR } }
      steps {
        withSonarQubeEnv('sonarqube') {
          withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
            sh 'mvn -B sonar:sonar -Dsonar.host.url="$SONAR_HOST_URL" -Dsonar.token="$SONAR_TOKEN"'
          }
        }
      }
    }
    stage('Quality Gate') {
      when { expression { return params.RUN_SONAR } }
      steps { timeout(time: 5, unit: 'MINUTES') { waitForQualityGate abortPipeline: true } }
    }
    stage('Container Build') { steps { sh 'docker build -t lost-item-intelligence-network:${BUILD_NUMBER} .' } }
  }
  post { always { junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml'; archiveArtifacts allowEmptyArchive: true, artifacts: 'target/*.jar,target/site/jacoco/**' } }
}
