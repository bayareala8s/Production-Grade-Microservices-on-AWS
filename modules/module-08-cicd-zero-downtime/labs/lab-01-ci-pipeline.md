# Lab 01 — CI Pipeline (Build → Test → Package)

## Outcome

You will define a CI pipeline for one microservice and enforce quality gates.

## Steps

### 1) Define pipeline stages

Minimum recommended stages:

- checkout
- install deps
- run tests
- build container image
- (optional) scan dependencies/image

### 2) Pick a CI system

Choose one:

- GitHub Actions
- AWS CodePipeline/CodeBuild

### 3) Use starter templates

See templates:

- `starter/github-actions/ci.yml`
- `starter/codebuild/buildspec.yml`

## Checkpoint

- A failing test blocks image publishing.


