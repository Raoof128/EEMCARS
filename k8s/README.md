# Kubernetes Deployment for EEMCARS

## Prerequisites

- Azure Kubernetes Service (AKS) cluster
- `kubectl` configured for your cluster
- Azure Container Registry access
- PostgreSQL database (Azure Database for PostgreSQL)
- Redis instance (Azure Cache for Redis)

## Quick Deploy

```bash
# 1. Set context
kubectl config use-context eemcars-production-aks

# 2. Create namespace
kubectl apply -f base/namespace.yaml

# 3. Create secrets (use Azure Key Vault in production)
kubectl create secret generic eemcars-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=secret-key=$SECRET_KEY \
  --namespace=eemcars

# 4. Apply configurations
kubectl apply -f base/configmap.yaml

# 5. Deploy applications
kubectl apply -f base/backend-deployment.yaml
kubectl apply -f base/frontend-deployment.yaml
kubectl apply -f base/celery-worker.yaml

# 6. Apply auto-scaling
kubectl apply -f base/hpa.yaml

# 7. Verify deployment
kubectl get pods -n eemcars
kubectl get svc -n eemcars
```

## Production Deployment with Kustomize

```bash
# Deploy to production
kubectl apply -k overlays/prod

# Deploy to development
kubectl apply -k overlays/dev
```

## Monitoring

```bash
# Check pod status
kubectl get pods -n eemcars -w

# View logs
kubectl logs -f deployment/eemcars-backend -n eemcars
kubectl logs -f deployment/eemcars-frontend -n eemcars

# Check resource usage
kubectl top pods -n eemcars
kubectl top nodes
```

## Scaling

```bash
# Manual scaling
kubectl scale deployment eemcars-backend --replicas=5 -n eemcars

# Check HPA status
kubectl get hpa -n eemcars
```

## Updates

```bash
# Update image
kubectl set image deployment/eemcars-backend \
  eemcars-backend=eemcarsprodacr.azurecr.io/eemcars-backend:v1.1.0 \
  -n eemcars

# Rollout status
kubectl rollout status deployment/eemcars-backend -n eemcars

# Rollback
kubectl rollout undo deployment/eemcars-backend -n eemcars
```

## Troubleshooting

```bash
# Describe pod
kubectl describe pod <pod-name> -n eemcars

# Execute commands in pod
kubectl exec -it <pod-name> -n eemcars -- /bin/bash

# View events
kubectl get events -n eemcars --sort-by='.lastTimestamp'
```

## Clean Up

```bash
# Delete all resources
kubectl delete namespace eemcars
```
