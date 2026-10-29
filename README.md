# Lost-Item Intelligence Network

Campus-focused lost-and-found web application built with Java 21, Spring Boot 3.5.16, Thymeleaf, Spring Security, Spring Data JPA, and MySQL.

## Prerequisites

- Java 21
- Maven 3.9+
- Docker Desktop (optional, for Compose)

## Run locally

1. Copy `.env.example` to `.env` and set strong database, MySQL root, and initial admin passwords.
2. Start MySQL with `docker compose up -d db` or provide an existing MySQL database.
3. Run `mvn spring-boot:run` from this directory.
4. Open http://localhost:8080.

Flyway creates the schema at startup. The bootstrap process creates only the configured administrator; report data starts empty. Set a strong admin password before first startup. Password change and account recovery screens are not part of this prototype. The application uses a database-backed user account store and BCrypt password hashes.

## Build and test

```sh
mvn clean verify
```

## Docker

```sh
docker compose up --build
```

The app is available at http://localhost:8080. Compose reads placeholders from `.env`; do not commit secrets.

## Matching score

The supplied project instructions specify weights of category 25%, description 35%, location 25%, and date/time 15%. The deck lists these factors without numeric weights. The threshold defaults to 55%; all values are configurable. See `docs/MATCHING.md`.

## Operations

- Jenkins: `Jenkinsfile` runs Maven verification and an optional SonarQube stage.
- SonarQube: run `mvn sonar:sonar` with server URL and token configured in Jenkins credentials.
- Git workflow: `docs/BRANCHING.md`.
- Synthetic demonstration scenario: `docs/DEMO_DATA.md`.
- REST endpoints are under `/api`; public pages use Thymeleaf.

## Verification status

The local environment used for the latest project audit has Java 21, Maven 3.10.0, Docker 29.9.2, and Docker Compose 5.6.1. The project passed `mvn -B clean verify` with 18 tests passing and no failures or skips. A Dockerized application and MySQL 8.4 database were running during the audit; health and application routes are checked separately and reported with the audit results. This directory is not a Git checkout, so branch or remote operations cannot be verified here. No live Jenkins, GitHub, or SonarQube execution is claimed. The older `PROJECT_REPORT.docx` predates this verification and should not be used as current test evidence.
