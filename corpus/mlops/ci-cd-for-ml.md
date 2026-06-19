---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-08-04-ci-cd-deployment-strategies.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - CI/CD for ML
  - ci cd machine learning
  - deployment strategies
  - service principals
  - databricks service principal
  - unity catalog hierarchy
  - git flow
  - branch protection
  - github actions matrix
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# CI/CD for ML (on Databricks)

**TL;DR.** Structuring data and assets for robust, secure, scalable ML on Databricks rests on two pillars: **Unity Catalog organization** (a three-tier catalog/schema/asset hierarchy with environment-scoped catalogs and access control) and **automated CI/CD** (Git Flow + branch protection feeding GitHub Actions pipelines that deploy via **Service Principals**) [^src1]. The throughline is that "users only have direct access to the dev workspace; deployments to acc/prd must go through CI/CD pipelines, using service principals for security and traceability" [^src1]. This page covers UC hierarchy & access modes, Service Principals, the Git Flow branching strategy, and the CI/CD pipeline shapes.

## Unity Catalog organization

For a workspace to use Unity Catalog it must be attached to a **metastore** — the top-level container for all data and AI asset metadata [^src1]. You can have **only one metastore per cloud region**, and each workspace can attach to only one metastore in that region [^src1]. UC organizes assets in a **three-tier hierarchy**, referenced as `catalog.schema.asset` [^src1]:

- **Catalogs** (e.g. `mlops_dev`, `mlops_acc`, `mlops_prd`)
- **Schemas** within catalogs (here, `marvel_characters` in each)
- **Assets** within schemas (tables, views, models, etc.)

### Securables & access modes

Permissions are set at two levels [^src1]:

- **Workspace-level securables** — notebooks, clusters, jobs — accessed via ACLs.
- **Unity Catalog-level securables** — tables, schemas, models — accessed via metastore-level privileges.

**Workspace binding / access modes**: a catalog in **OPEN** mode is accessible from any workspace; use **ISOLATED** mode to control cross-project access [^src1]. The ideal setup [^src1]: all ML pipelines (dev/acc/prd) have *read* access to production data (e.g. `prd_gold`) for consistency; each workspace can only *write* to its own catalog; users have direct access only to dev, with acc/prd reached through CI/CD using service principals. (The course example uses one shared workspace but dedicated dev/acc/prd catalogs with limited permissions to avoid unintentional breakage [^src1].)

## Service Principals (SPNs)

A **Service Principal** is "a special, non-human identity used by applications, automation tools, or CI/CD pipelines to authenticate and interact with cloud resources securely" [^src1]. For the CD pipeline to deploy automatically and securely, you must use an SPN rather than personal user credentials [^src1]. Why an SPN over a user account [^src1]:

- **Security** — not tied to an individual, so departures don't risk lost access or exposed credentials.
- **Least privilege** — granted only the permissions needed for deployment, nothing more.
- **Auditability** — all pipeline actions are clearly attributable to the SPN, easing change-tracking and compliance.
- **Automation** — credentials (client ID + secret) can be stored securely in the CI/CD system for hands-off deployment.

Setup: create the SPN in the workspace admin console (User Management → Service Principals), note its Client ID and Client Secret, grant scoped UC/job/workspace privileges (e.g. `CAN_MANAGE`/`CAN_RUN`, scoped to acc/prd only) [^src1]. For serverless endpoint calls, grant the SPN `CAN_QUERY` and obtain an **OAuth token via the client-credentials grant** against `/oidc/v1/token` (`grant_type=client_credentials`, `scope=all-apis`) — a more secure, scalable alternative to the PAT used earlier in the course [^src1].

## Branching & release strategy (Git Flow)

The course uses a version of **Git Flow** [^src1]:

- Feature branches are created from `main`.
- Developers open PRs to `main`, triggering the **CI** pipeline.
- CI runs pre-commit checks, unit tests, and version checks.
- **At least 2 approvals** are required to merge (enforced via **branch protection rules**); direct pushes to `main` are not allowed.
- Once merged, the **CD** pipeline deploys to acceptance and production using environment-scoped secrets and SPNs. Production deployment should be guarded by **deployment protection rules** (deploy only after approval) [^src1].

## CI/CD pipelines (GitHub Actions)

**CI** (`.github/workflows/ci.yml`), triggered on PR/push to `main`/`dev` [^src1]:

- Installs deps with **[[mlops/uv|uv]]** (`uv sync --extra test`).
- Runs pre-commit checks (`uv run pre-commit run --all-files`) and pytest.
- Tags a git version from `version.txt` to enforce **version uniqueness** (prevents accidental duplicate releases) [^src1].

**CD** (`.github/workflows/cd.yml`), triggered after a successful merge to `main` [^src1]:

- Uses a **strategy matrix** `environment: [acc, prd]` so the job runs per environment, with `environment: ${{ matrix.environment }}` selecting **environment-scoped secrets** [^src1].
- Reads `DATABRICKS_HOST` (variable), `DATABRICKS_CLIENT_ID` / `DATABRICKS_CLIENT_SECRET` (secrets) — the SPN credentials, written to `~/.databrickscfg` [^src1].
- Installs the Databricks CLI + uv, then runs **`databricks bundle deploy`** (which builds the wheel and deploys the [[mlops/databricks-asset-bundles|Databricks Asset Bundle]] / Lakeflow job to acc and prd), tagging + pushing the version only on `prd` [^src1].

To wire it up, create GitHub **Environments** `prd` and `acc`, add the SPN's `DATABRICKS_CLIENT_ID`/`DATABRICKS_CLIENT_SECRET` as environment secrets and `DATABRICKS_HOST` as a variable; the CLI picks these up and authenticates as the SPN [^src1].

## Key takeaways

Catalogs, schemas, and workspaces provide clean separation and access control; service principals keep automation secure and scoped; Git Flow + branch protection enforce code quality and review; CI/CD pipelines automate validation and deployment with no manual pushes to production [^src1].

## See also

- [[mlops/databricks-asset-bundles|Databricks Asset Bundles]] — `databricks bundle deploy` is this pipeline's deployment payload
- [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] — the data-infra sibling of this ML CI/CD discipline
- [[mlops/databricks-development|Databricks Development]] — the dev/acc/prd catalog split originates in the local-dev setup
- [[mlops/model-serving|Model Serving]] — the SPN OAuth flow authenticates serverless endpoint calls
- [[data-engineering/databricks|Databricks]] — Unity Catalog and the platform
- [[mlops/README|MLOps hub]]

---

[^src1]: [CI/CD & Deployment Strategies (Marvelous MLOps, Lecture 8)](../../raw/email/email-2025-08-04-ci-cd-deployment-strategies.md)
</content>
