---
type: entity
domain: mlops
status: stub
sources:
  - path: raw/github/github-jpetazzo-ampernetacle.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - jpetazzo/ampernetacle
  - Kubernetes Oracle Cloud free tier
  - OCI Kubernetes Terraform
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Ampernetacle

**TL;DR** — A Terraform configuration that deploys a **4-node ARM Kubernetes cluster on Oracle Cloud Infrastructure (OCI)** within OCI's **free tier** — making it possible to run a multi-node "real" Kubernetes cluster at zero cost for learning and ARM development testing [^src1].

> **Not for production workloads** — explicitly a learning/development tool.

## Key facts

- **Repo**: [github.com/jpetazzo/ampernetacle](https://github.com/jpetazzo/ampernetacle)
- **Author**: jpetazzo (Jérôme Petazzoni, Docker/K8s educator)
- **Stars**: ~2,690
- **Language**: HCL (Terraform)
- **Default cluster**: 4 nodes × 1 OCPU × 6 GB RAM (ARM) — fits OCI free tier

## What it does

Uses `kubeadm` to install Kubernetes on OCI VMs provisioned by Terraform:
1. Creates N virtual machines on Oracle Cloud.
2. Installs Kubernetes control plane on the first machine via `kubeadm`.
3. Joins remaining VMs as worker nodes.
4. Generates a `kubeconfig` file in the project directory.

## Quick start

```bash
# Prerequisites: OCI account, terraform, OCI CLI, kubeadm/kubelet/kubectl
oci session authenticate   # get session token
terraform init
terraform apply

# After apply completes:
export KUBECONFIG=$PWD/kubeconfig
kubectl get nodes
```

## Why it matters for learning

- Multi-node cluster (vs. single-node Minikube/k3s) — exercises real K8s networking, node affinity, and service discovery.
- Free (OCI free tier) — no cloud bill while learning.
- ARM architecture — useful for testing ARM-native container builds.
- Fully Terraform-managed — reinforces IaC workflow alongside Kubernetes [^src1].

## See also

- [Terraform](/mlops/terraform.md) — the IaC tool used to provision the cluster
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) — broader IaC context
- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) — cloud concepts; OCI as a provider
- [MLOps hub](/mlops/README.md)

---

[^src1]: [jpetazzo/ampernetacle (GitHub)](../../raw/github/github-jpetazzo-ampernetacle.md) — README: description, setup steps, use case statement
