# EEMCARS Monitoring and Observability

Comprehensive monitoring stack for the Essential Eight Maturity Assessment platform.

## Components

### 1. Prometheus

**Purpose:** Metrics collection and alerting
**Location:** `prometheus/`

- **ServiceMonitor** (`servicemonitor.yaml`): Automatic service discovery and metric scraping
  - Backend API metrics (request rate, latency, errors)
  - Frontend metrics
  - Celery worker metrics

- **PrometheusRule** (`rules.yaml`): Alert definitions
  - High error rates (>5%)
  - High API latency (>2s at p95)
  - Database connection pool exhaustion
  - Celery queue backlog
  - Pod resource usage
  - Assessment failures
  - Essential Eight maturity degradation

**Deployment:**
```bash
# Install Prometheus Operator (if not already installed)
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml

# Deploy EEMCARS monitoring
kubectl apply -f prometheus/servicemonitor.yaml
kubectl apply -f prometheus/rules.yaml
```

### 2. Grafana

**Purpose:** Visualization and dashboards
**Location:** `grafana/`

**Dashboard:** `eemcars-dashboard.json`

**Panels:**
- Essential Eight maturity levels (gauge visualization)
- Overall compliance score
- Assessment run statistics
- Maturity trends (30-day)
- API request rate and latency
- Error rates
- Celery task queue length
- Database connection pool status
- Pod memory/CPU usage
- Drift events
- Remediation task status
- Evidence collection rate

**Import Dashboard:**
```bash
# Via Grafana UI
1. Navigate to Dashboards > Import
2. Upload eemcars-dashboard.json
3. Select Prometheus data source

# Via ConfigMap
kubectl create configmap grafana-dashboard-eemcars \
  --from-file=eemcars-dashboard.json=grafana/eemcars-dashboard.json \
  -n monitoring
```

### 3. Azure Monitor

**Purpose:** Azure-native monitoring and alerting
**Location:** `azure/`

**Alert Rules** (`alert-rules.json`):
- High CPU usage (>80%)
- High memory usage (>85%)
- Pod not ready state
- Application errors (>10/5min)
- Slow API requests (>2s, >50 requests)

**Deployment:**
```bash
# Deploy with Azure CLI
az deployment group create \
  --resource-group eemcars-production-rg \
  --template-file azure/alert-rules.json \
  --parameters actionGroupId="/subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Insights/actionGroups/{action-group-name}"

# Create Action Group first if needed
az monitor action-group create \
  --name eemcars-alerts \
  --resource-group eemcars-production-rg \
  --short-name eemcars \
  --email-receiver name=admin email=admin@example.com \
  --sms-receiver name=oncall countrycode=61 phonenumber=0400000000
```

### 4. Application Insights

**Purpose:** Distributed tracing and application performance monitoring
**Location:** `application-insights/`

**Features:**
- Request/response tracking
- Exception monitoring
- Dependency tracking (PostgreSQL, Redis, external APIs)
- Performance counters
- Custom telemetry for Essential Eight events
- Distributed transaction tracing

**Configuration:**
```bash
# Apply configuration
kubectl apply -f application-insights/appinsights-config.yaml

# Add secret with connection string
kubectl create secret generic appinsights-connection \
  --from-literal=connection-string="InstrumentationKey=xxx;IngestionEndpoint=https://australiaeast-1.in.applicationinsights.azure.com/" \
  -n eemcars
```

**Backend Integration (Python):**
```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

# Setup in app initialization
tracer = Tracer(
    exporter=AzureExporter(connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')),
    sampler=ProbabilitySampler(1.0)
)
```

### 5. Fluentd

**Purpose:** Log aggregation and forwarding to Azure Log Analytics
**Location:** `fluentd/`

**Features:**
- Container log collection
- Kubernetes metadata enrichment
- JSON parsing for structured logs
- Sensitive data filtering
- Essential Eight context tagging
- Azure Log Analytics integration

**Deployment:**
```bash
# Create secrets for Log Analytics
kubectl create secret generic log-analytics-credentials \
  --from-literal=workspace-id=$WORKSPACE_ID \
  --from-literal=shared-key=$SHARED_KEY \
  -n eemcars

# Deploy Fluentd DaemonSet
kubectl apply -f fluentd/fluentd-config.yaml
```

**Log Query Examples (Azure Log Analytics):**
```kusto
// All EEMCARS logs
EEMCARSLogs_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc

// Error logs only
EEMCARSLogs_CL
| where severity_s == "ERROR"
| where TimeGenerated > ago(24h)

// Assessment failures
EEMCARSLogs_CL
| where message_s contains "assessment" and severity_s == "ERROR"
| summarize count() by pillar_s, bin(TimeGenerated, 1h)

// Compliance events
EEMCARSLogs_CL
| where message_s contains "maturity_level_changed"
| project TimeGenerated, pillar_s, old_level_d, new_level_d
```

## Metrics Reference

### Essential Eight Metrics

```promql
# Current maturity levels
essential_eight_maturity_level{pillar="application_control"}

# Maturity change rate
rate(essential_eight_maturity_level[1h])

# Average compliance score
avg(essential_eight_maturity_level) / 3 * 100

# Maturity degradation (24h comparison)
essential_eight_maturity_level - essential_eight_maturity_level offset 24h
```

### Application Metrics

```promql
# Request rate
rate(http_requests_total{job="eemcars-backend"}[5m])

# Error rate
rate(http_requests_total{job="eemcars-backend",status=~"5.."}[5m])
/
rate(http_requests_total{job="eemcars-backend"}[5m])

# P95 latency
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket{job="eemcars-backend"}[5m])
)

# Active database connections
sqlalchemy_pool_connections{state="in_use"}

# Celery queue length
celery_queue_length{queue="default"}
```

### Infrastructure Metrics

```promql
# Pod CPU usage
rate(container_cpu_usage_seconds_total{namespace="eemcars"}[5m])

# Pod memory usage
container_memory_working_set_bytes{namespace="eemcars"} / 1024 / 1024

# Pod restart count
kube_pod_container_status_restarts_total{namespace="eemcars"}
```

## Alert Response Procedures

### Critical Alerts

**MaturityLevelDegradation:**
1. Check recent drift events: `kubectl logs -l component=backend -n eemcars | grep drift`
2. Review failed assessments in UI
3. Validate evidence collection is functioning
4. Run manual assessment to verify

**DatabaseConnectionPoolExhausted:**
1. Check active queries: Query Azure Database for PostgreSQL metrics
2. Scale backend pods: `kubectl scale deployment eemcars-backend --replicas=5 -n eemcars`
3. Review slow query logs
4. Consider increasing pool size in configuration

**PodNotReady:**
1. Describe pod: `kubectl describe pod <pod-name> -n eemcars`
2. Check logs: `kubectl logs <pod-name> -n eemcars`
3. Verify secrets/config: `kubectl get secrets,configmaps -n eemcars`
4. Check resource quotas

### Warning Alerts

**HighErrorRate:**
1. Check Application Insights for exception details
2. Review recent deployments: `kubectl rollout history deployment/eemcars-backend -n eemcars`
3. Analyze error patterns in logs
4. Rollback if necessary: `kubectl rollout undo deployment/eemcars-backend -n eemcars`

**HighAPILatency:**
1. Check database performance metrics
2. Review Redis cache hit rate
3. Analyze slow queries
4. Consider horizontal scaling

**CeleryQueueBacklog:**
1. Check worker status: `kubectl logs -l component=celery-worker -n eemcars`
2. Scale workers: `kubectl scale deployment eemcars-celery-worker --replicas=4 -n eemcars`
3. Review task failure rate
4. Check Redis availability

## Dashboard Access

**Grafana:** https://grafana.eemcars.io
**Prometheus:** https://prometheus.eemcars.io
**Azure Portal:** https://portal.azure.com → Log Analytics → EEMCARSLogs
**Application Insights:** https://portal.azure.com → Application Insights → eemcars-appinsights

## Retention Policies

- **Prometheus:** 15 days (in-cluster)
- **Azure Log Analytics:** 90 days (configurable)
- **Application Insights:** 90 days (default)
- **Grafana Dashboard History:** 30 days

## Custom Metrics

Add custom metrics in backend code:

```python
from prometheus_client import Counter, Histogram, Gauge

# Assessment metrics
assessment_runs = Counter(
    'assessment_runs_total',
    'Total assessment runs',
    ['status', 'pillar']
)

# Maturity level gauge
maturity_level = Gauge(
    'essential_eight_maturity_level',
    'Current maturity level per pillar',
    ['pillar']
)

# Evidence collection
evidence_collected = Counter(
    'evidence_collected_total',
    'Total evidence items collected',
    ['source', 'type']
)

# Usage
assessment_runs.labels(status='completed', pillar='application_control').inc()
maturity_level.labels(pillar='patch_applications').set(2)
evidence_collected.labels(source='defender', type='vulnerability_scan').inc()
```

## Troubleshooting

**Prometheus not scraping metrics:**
```bash
# Check ServiceMonitor
kubectl get servicemonitor -n eemcars
kubectl describe servicemonitor eemcars-backend-monitor -n eemcars

# Verify Prometheus target
kubectl port-forward svc/prometheus-operated 9090:9090 -n monitoring
# Navigate to http://localhost:9090/targets
```

**Fluentd not forwarding logs:**
```bash
# Check DaemonSet status
kubectl get daemonset fluentd -n eemcars
kubectl logs -l app=fluentd -n eemcars --tail=100

# Verify Log Analytics credentials
kubectl get secret log-analytics-credentials -n eemcars -o yaml
```

**Application Insights no data:**
```bash
# Check connection string
kubectl get configmap appinsights-config -n eemcars -o yaml

# Verify backend logs for telemetry initialization
kubectl logs -l component=backend -n eemcars | grep -i "application insights"
```

## Maintenance

### Weekly Tasks
- Review alert thresholds and tune as needed
- Check dashboard accuracy
- Validate retention policies
- Review high-cardinality metrics

### Monthly Tasks
- Analyze long-term trends
- Update alert runbooks
- Review and archive old dashboards
- Capacity planning based on metrics

### Quarterly Tasks
- Full monitoring stack review
- Disaster recovery testing
- Update metric retention policies
- Audit log access and compliance
