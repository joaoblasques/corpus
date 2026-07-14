---
type: entity
domain: mlops
status: draft
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
updated: 2026-07-14
---

# Ampernetacle

**TL;DR** — A Terraform configuration that deploys a **4-node ARM Kubernetes cluster on Oracle Cloud Infrastructure (OCI)** within OCI's **free tier** — making it possible to run a multi-node "real" Kubernetes cluster at zero cost for learning and ARM development testing [^src1].

> **Not for production workloads** — explicitly a learning/development tool.

## Key facts

- **Repo**: github.com/jpetazzo/ampernetacle
- **Author**: jpetazzo (Jérôme Petazzoni, Docker/K8s educator)
- **Stars**: ~2,690
- **Language**: HCL (Terraform)
- **Default cluster**: 4 nodes × 1 OCPU × 6 GB RAM (ARM) — fits OCI free tier
- **Name origin**: portmanteau of Ampere, Kubernetes, and Oracle [^src1]

## What it does

Uses `kubeadm` to install Kubernetes on OCI VMs provisioned by Terraform. Full internal pipeline [^src1]:

1. Generates an OpenSSH keypair and a kubeadm token.
2. Deploys VMs using Ubuntu 20.04.
3. Uses **cloud-init** to install and configure Docker and Kubernetes packages.
4. Runs `kubeadm init` on the first VM (control plane).
5. Runs `kubeadm join` on remaining VMs (worker nodes).
6. Installs the **Weave CNI plugin** for pod networking.
7. Transfers the `kubeconfig` file and patches it to use the VM's public IP.

At the end of `terraform apply`, nodes are named `node1` to `node4` and reachable via SSH using a command printed in the Terraform output [^src1].

## Quick start

```bash
# Prerequisites: OCI account, terraform, OCI CLI, kubeadm/kubelet/kubectl
oci session authenticate   # get session token (valid 1 hour by default)
terraform init
terraform apply

# After apply completes:
export KUBECONFIG=$PWD/kubeconfig
kubectl get nodes
# Expected: 4 nodes named node1–node4
```

Windows (PowerShell 5.1+) is also supported; may require setting execution policy to unrestricted [^src1].

## Customization

`variables.tf` exposes tweakable parameters [^src1]:

- Number of nodes (default: 4).
- Node size (default: 1 OCPU / 6 GB RAM).
- CPU architecture — switch to Intel/AMD instances, but **free tier only applies to ARM** [^src1].
- Availability domain — useful to work around capacity errors (see Caveats).

Tear down with `terraform destroy`.

## Caveats and known limitations

These are explicit gaps in the current implementation [^src1]:

| Missing capability | Consequence |
|---|---|
| No OCI cloud controller manager | `LoadBalancer`-type services stay `<pending>` indefinitely; use `NodePort` instead |
| No ingress controller | No HTTP routing layer out of the box |
| No storage class | Persistent volumes not available by default |

The OCI cloud controller manager can be installed manually from its GitHub repository [^src1].

Oracle Cloud also offers a managed Kubernetes service (**OKE — Container Engine for Kubernetes**) that does not have these limitations, but OKE is not part of the free tier [^src1].

## Common errors

### Authentication failure (401-NotAuthenticated)

Session tokens obtained via `oci session authenticate` expire after **1 hour** by default. Re-authenticate with `oci session authenticate` or refresh with `oci session refresh --profile DEFAULT` [^src1].

### Capacity error (500-InternalError: Out of host capacity)

OCI may have insufficient ARM capacity in a given availability domain. Switch to a different availability domain via `variables.tf` [^src1].

## Why it matters for learning

- Multi-node cluster (vs. single-node Minikube/k3s) — exercises real K8s networking, node affinity, and service discovery [^src1].
- Free (OCI free tier) — no cloud bill while learning.
- ARM architecture — useful for testing ARM-native container builds.
- Fully Terraform-managed — reinforces IaC workflow alongside Kubernetes [^src1].

## See also

- [Terraform](/mlops/terraform.md) — the IaC tool used to provision the cluster
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) — broader IaC context
- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) — cloud concepts; OCI as a provider
- [MLOps hub](/mlops/README.md)

---

[^src1]: [jpetazzo/ampernetacle (GitHub)](../../raw/github/github-jpetazzo-ampernetacle.md)
