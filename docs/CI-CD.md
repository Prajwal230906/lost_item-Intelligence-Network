# Jenkins, Maven, JUnit, SonarQube, and Docker

The root `Jenkinsfile` runs this delivery pipeline:

1. Checks out the branch configured by the Jenkins job.
2. Runs `mvn -B clean verify`. Maven compiles the application, runs the JUnit tests, and writes JaCoCo coverage output.
3. Runs SonarQube analysis and waits for the quality gate when `RUN_SONAR` is enabled (enabled by default).
4. Builds a Docker image tagged with the Jenkins build number and checked-out commit.
5. Replaces the pipeline-managed application container and starts the new image at `http://localhost:8093`.
6. Optionally pushes that image to Docker Hub when `PUBLISH_IMAGE` is enabled.

The run stage uses the Jenkins agent's Docker engine. It binds the app to loopback on port 8093 and connects to MySQL on the Docker host at port 3306. Each run replaces the prior container named `lost-item-intelligence-network-ci`.

## Configure Jenkins once

1. Install Jenkins and these plugins: **Pipeline**, **Git**, **Credentials Binding**, **JUnit**, **SonarQube Scanner for Jenkins**, **PowerShell** (for Windows agents), and **GitHub Branch Source** (for GitHub Multibranch jobs). The pipeline calls the Docker CLI directly, so the build agent must have Docker Engine/CLI available; the Docker Pipeline plugin is not required.
2. Add a Jenkins JDK tool named exactly `jdk21` using Java 21. Add a Maven tool named exactly `maven3` using Maven 3.9 or newer.
3. Use a Jenkins agent with Git, Docker CLI, and access to its Docker daemon. Grant Docker access only to a trusted CI agent; Docker daemon access is effectively privileged machine access. The Jenkinsfile supports both Windows and Unix-like agents. Windows image publishing also needs the Jenkins PowerShell plugin and PowerShell available on the agent.
4. In **Manage Jenkins → System → SonarQube installations**, add the server with the name `sonarqube`. Store its token in Jenkins Credentials as **Secret text**, ID `sonar-token`; never put the token in the repository or Jenkinsfile.
5. Add a Jenkins **Username with password** credential with ID `application-db-credentials`. Set the username and password to a MySQL account with access to `lost_item_network`. MySQL must accept connections from Docker Desktop through the host's port 3306.
6. In SonarQube, configure a webhook to `https://<your-jenkins-url>/sonarqube-webhook/` (include the final slash). Jenkins needs this callback to receive the quality gate result. Ensure the Jenkins URL is reachable by SonarQube.
7. Create a **Multibranch Pipeline** job for the GitHub repository, authenticate to GitHub as needed, and set the script path to `Jenkinsfile`. For prompt builds, configure a GitHub webhook to `https://<your-jenkins-url>/github-webhook/` and enable push and pull-request events. Protect the target GitHub branches and require the Jenkins status check before merging.

If Jenkins is exposed outside your local network, use HTTPS and appropriate authentication. Do not publish an unauthenticated Jenkins instance to the internet.

The local URL `http://localhost:8081` works only from this computer. GitHub cannot deliver webhooks to a localhost address; use a secured, externally reachable Jenkins URL or configure branch polling for a local-only setup. The updated files must also be committed and pushed to GitHub before a Multibranch Pipeline can read them.

## First run and expected behavior

Run the multibranch job after the JDK, Maven, SonarQube server, token, webhook, GitHub connection, and Docker-enabled agent are configured. `RUN_SONAR` defaults to true, so a missing SonarQube configuration should be fixed rather than treated as a successful quality check. For a deliberate Maven-and-Docker-only diagnostic run, turn `RUN_SONAR` off; the quality-gate stages will be skipped for that build. The pipeline passes `SONAR_TOKEN` through the environment; use SonarScanner for Maven 5.0 or newer, which supports this authentication method.

JUnit XML files under `target/surefire-reports/` are published by Jenkins even when a later stage fails. The Maven test stage must pass before the image is built. A failed SonarQube quality gate blocks image build and application restart. The run stage checks `http://localhost:8093/login` for readiness and prints the container logs if the app does not start.

## Optional Docker Hub publishing

1. Add a Jenkins **Username with password** credential with ID `docker-registry-credentials`; use a Docker Hub access token as its password.
2. Run the job with `PUBLISH_IMAGE` checked and set `IMAGE_REPOSITORY` to the Docker Hub repository, such as `your-namespace/lost-item-intelligence-network`.
3. On a successful run, Jenkins publishes `IMAGE_REPOSITORY:BUILD_NUMBER-COMMIT` (the commit is shortened to 12 characters).

Keep registry credentials in Jenkins and do not echo them in build steps. `PUBLISH_IMAGE` defaults to false, so normal verification does not require registry credentials.

## Local pipeline prerequisites

Run the same application checks locally with `mvn -B clean verify`; build the container with `docker build -t lost-item-intelligence-network:local .`. The Compose stack in `compose.yaml` is for local app/database use and needs the required values from an untracked `.env` file. Do not copy production credentials into that file or commit it.
