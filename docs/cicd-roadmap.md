# CI/CD roadmap (not yet enabled)

No deployment workflow is enabled by this initial source import. Implement CI/CD only after the real model artifact is safely versioned or retrieved by an approved artifact mechanism and a clean build is reproducible.

## Planned stages

1. **Validation:** Python syntax checks, API unit tests (they mock inference), frontend syntax/contract tests, and Dockerfile/context checks.
2. **Build and publish:** GitHub Actions builds only the changed service, uses BuildKit caching, tags images with both the commit SHA and `latest`, and publishes to the already-used Docker Hub account `rockstar1505`. The token belongs in GitHub Actions secrets, never YAML.
3. **Controlled deploy:** manually triggered after EC2 has been started. Prefer GitHub OIDC for short-lived AWS credentials plus Systems Manager Run Command if the instance is registered and the IAM role is least-privileged.
4. **Post-deploy health checks:** API `/health`, public UI, Prometheus target `resume-api` up, and Grafana dashboard available.
5. **Rollback:** keep a previously working SHA-tagged image and replace only `api`/`ui` if post-deploy health checks pass; restore prior tags if checks fail.

## Conditions before implementation

- Add the genuine ModernBERT model files (the safetensors weight is approximately 570.84 MiB) via Git LFS or a controlled artifact store. Do not use placeholder weights.
- Verify GitHub Actions can checkout the model artifact within available LFS/artifact bandwidth.
- Verify Docker Hub push token, repository permissions, and build contexts.
- Verify EC2 Systems Manager connectivity and IAM role before selecting SSM; do not open SSH broadly as a fallback.
- Keep deployment manual at first so a Git push does not start EC2 or incur unplanned compute usage.

CI/CD must not run `docker compose down -v`, delete `prometheus`/`grafana`, wipe volumes, recreate the EC2 instance, or change security-group rules.
