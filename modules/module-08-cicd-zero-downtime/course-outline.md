# Module 8 — Course Outline (Instructor)

## Recommended duration

3–6 hours

## Learning objectives

- understand CI vs CD and how microservices multiply pipeline needs
- build pipelines that enforce quality (tests, lint, security scanning)
- deploy without downtime (rolling, blue/green)
- implement safe rollback using health checks and alarms

## Lesson plan (suggested)

### Part A — CI/CD fundamentals for microservices (30–45 min)

- one pipeline per service vs shared templates
- artifact promotion vs rebuild-per-env
- “what is a release?” in a multi-service world

### Part B — CI pipeline design (45–75 min)

- build → test → package → scan
- caching and speed
- lab tie-in: `labs/lab-01-ci-pipeline.md`

### Part C — Container registry + image provenance (30–60 min)

- tagging strategy (commit SHA, semver, env tags)
- pushing to ECR
- lab tie-in: `labs/lab-02-ecr-build-push.md`

### Part D — Zero-downtime deploys (60–120 min)

- rolling deployments: simple, sometimes risky
- blue/green: safer, needs infra support + routing
- lab tie-in: `labs/lab-03-ecs-blue-green.md`

### Part E — Rollbacks and release gates (45–75 min)

- automated rollback triggers (alarms, health checks, SLO burn)
- smoke tests as post-deploy gates
- lab tie-in: `labs/lab-04-rollback-gates.md`

## Instructor checkpoints

- students can describe a pipeline with explicit gates and artifacts
- students can explain when to use rolling vs blue/green
- students can define rollback conditions and post-deploy smoke tests


