# Module 3 — Grading Rubric (Suggested)

## Total: 100 points

### Container quality (35)

- 15: Dockerfile is deterministic and caches dependencies properly
- 10: container runs via env vars (no hardcoded secrets)
- 10: health endpoint present and used

### ECS deployment (45)

- 15: task definition configured correctly (CPU/mem/ports/logs)
- 20: ECS service runs successfully and is reachable
- 10: basic scaling demo (increase desired tasks; verify)

### Operational thinking (20)

- 10: identifies key metrics (CPU/mem, latency) and logs location
- 10: can explain rollback approach (redeploy previous image)


