---
type: entity
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md
    channel: notes
    ingested_at: 2026-05-21
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
updated: 2026-05-21
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

Kubernetes is the natural runtime platform for [[software-engineering/microservices|microservices]] architecture [^src1]:
- Services provide stable endpoints despite ephemeral pods — solving the network identity problem in distributed systems
- Namespaces enforce the service isolation that prevents shared-database anti-patterns
- Deployments implement zero-downtime rolling updates — critical when services must evolve independently
- Auto-restart and health checks address partial failure modes discussed in [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]]

## See also

- [[software-engineering/microservices|Microservices]] — the architectural style Kubernetes operationalizes at runtime
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — Kubernetes addresses partial failure and network unreliability via auto-restart and load balancing
- [[software-engineering/software-design-principles|Software Design Principles]] — loose coupling is enforced at infrastructure level via Service objects (stable endpoints over dynamic pods)
- [[software-engineering/README|Software Architecture hub]]

---

[^src1]: [[03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners|DevOps - Kubernetes Complete Course for Beginners]]
