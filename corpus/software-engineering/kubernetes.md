---
type: entity
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/email/email-2026-06-27-0-years-experience-kubernetes-homelab-devops-job.md
    channel: email
    ingested_at: 2026-07-06
aliases:
  - Kubernetes
  - k8s
  - kubernetes
  - container orchestration
  - kubectl
tags:
  - corpus/software-engineering
  - entity
created: 2026-05-21
updated: 2026-07-06
---

# Kubernetes (k8s)

**TL;DR**: Container orchestration platform that solves managing many containers across many machines at scale — auto-restart, load balancing, zero-downtime deployments, and persistent storage management [^src1].

## Architecture

```
Control Plane (Master):
  - API Server          ← all kubectl commands go here
  - etcd                ← cluster state storage (source of truth)
  - Scheduler           ← assigns pods to nodes
  - Controller Manager  ← watches actual state, converges to desired state

Worker Nodes:
  - kubelet             ← runs pods per API server instructions
  - kube-proxy          ← networking rules
  - Container runtime   ← Docker / containerd
```

## Core components

| Component | Purpose |
|---|---|
| **Pod** | Smallest deployable unit; wraps containers; ephemeral |
| **Deployment** | Manages pod replicas; rolling updates; rollbacks |
| **Service** | Stable network endpoint (pods have dynamic IPs); types: ClusterIP / NodePort / LoadBalancer |
| **ConfigMap** | Non-sensitive config (env vars, config files) |
| **Secret** | Sensitive data — base64 encoded, not encrypted by default |
| **Namespace** | Virtual cluster within cluster; isolate by team/environment |
| **Ingress** | HTTP/HTTPS routing rules; single entry point → multiple services |
| **Helm** | Package manager; Helm Charts = reusable deployment templates |

## Deployment manifest

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    spec:
      containers:
      - name: my-app
        image: my-app:1.0
        ports:
        - containerPort: 8080
```

## Persistent storage

```
PersistentVolume (PV)        ← actual storage resource
PersistentVolumeClaim (PVC)  ← pod's request for storage
StorageClass                 ← dynamic provisioning
```

## StatefulSet (vs Deployment)

Use for stateful workloads (databases) [^src1]:
- Stable pod identities (`pod-0`, `pod-1` — not random)
- Ordered startup and shutdown
- Stable persistent storage per pod

Deployments suit stateless services; StatefulSets suit databases and anything needing stable identity.

## Essential kubectl

```bash
kubectl apply -f manifest.yaml
kubectl get pods / services
kubectl describe pod <name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- /bin/bash
kubectl delete -f manifest.yaml
```

## Relationship to microservices

Kubernetes is the natural runtime platform for [microservices](/software-engineering/microservices.md) architecture [^src1]:
- Services provide stable endpoints despite ephemeral pods — solving the network identity problem in distributed systems
- Namespaces enforce the service isolation that prevents shared-database anti-patterns
- Deployments implement zero-downtime rolling updates — critical when services must evolve independently
- Auto-restart and health checks address partial failure modes discussed in [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md)

## Kubernetes homelab as hiring proof

Interviewers for DevOps/platform roles increasingly weight demonstrated proof over years of experience [^src2]. A homelab cluster enables candidates to speak to:

- How a pod goes from `kubectl apply` to running (Scheduler → kubelet → container runtime)
- How traffic reaches a pod (Service → kube-proxy → pod IP)
- Real incidents created and debugged in a personal lab

The KubeCraft pattern: build real clusters, document everything, surface it via GitHub + LinkedIn. Interviews become "tell me what you built" rather than trivia exams [^src2].

> "Companies don't hire years. They hire proof." [^src2]

## See also

- [Microservices](/software-engineering/microservices.md) — the architectural style Kubernetes operationalizes at runtime
- [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md) — Kubernetes addresses partial failure and network unreliability via auto-restart and load balancing
- [Software Design Principles](/software-engineering/software-design-principles.md) — loose coupling is enforced at infrastructure level via Service objects (stable endpoints over dynamic pods)
- [Software Architecture hub](/software-engineering/README.md)

---

[^src1]: [DevOps - Kubernetes Complete Course for Beginners](/03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md)
[^src2]: [0 years experience. Kubernetes homelab. DevOps job](../../raw/email/email-2026-06-27-0-years-experience-kubernetes-homelab-devops-job.md)
