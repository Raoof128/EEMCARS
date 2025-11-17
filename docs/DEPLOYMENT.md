# EEMCARS Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Azure Production Deployment](#azure-production-deployment)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

- **Azure CLI** ≥ 2.50.0
- **Terraform** ≥ 1.5.0
- **kubectl** ≥ 1.28
- **Docker** ≥ 24.0
- **Python** ≥ 3.11 (for local development)
- **Node.js** ≥ 18 (for frontend development)

### Azure Requirements

- Azure subscription with Owner or Contributor role
- Resource Provider registrations:
  - Microsoft.ContainerService
  - Microsoft.ContainerRegistry
  - Microsoft.DBforPostgreSQL
  - Microsoft.KeyVault
  - Microsoft.Storage
  - Microsoft.Network

### Register Resource Providers

```bash
az provider register --namespace Microsoft.ContainerService
az provider register --namespace Microsoft.DBforPostgreSQL
az provider register --namespace Microsoft.KeyVault
