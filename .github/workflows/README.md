# GitHub Actions

CI/CD workflows are intentionally not enabled yet. Before adding image publishing or deployment:

1. Resolve the missing API model artifact and prove a clean API build.
2. Run API regression tests and frontend validation in CI.
3. Store Docker Hub credentials as GitHub Actions secrets.
4. Verify AWS Systems Manager connectivity and the EC2 instance role before implementing OIDC + SSM deployment.
5. Require health checks and a rollback path.

Do not create a workflow that automatically starts EC2 on every push. Keep the current production deployment stable until the build and deployment process has been tested.
