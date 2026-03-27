# Blue-Green Deployment using Ansible (Zero Downtime)

##  Overview

This project implements a **Blue/Green deployment strategy** using **Ansible** on a simulated infrastructure built with **Docker Compose**. The goal is to achieve **zero-downtime deployments** with automated traffic switching, health checks, and rollback protection.

---

## Key Features

* Blue/Green deployment strategy
* Fully automated using Ansible roles
* NGINX reverse proxy for traffic routing
* Health check validation before switching
* Rollback mechanism using Ansible `block/rescue`
* Zero downtime deployment
* Idempotent infrastructure automation

---

## Architecture

```
          ┌──────────────┐
          │   Client     │
          └──────┬───────┘
                 │
          ┌──────▼───────┐
          │ LoadBalancer │ (NGINX)
          └──────┬───────┘
         ┌────────┴────────┐
     BLUE (old)        GREEN (new)
   blue1   blue2     green1  green2
```

---

## Tech Stack

* **Ansible** – Automation & orchestration
* **Docker Compose** – Local infrastructure simulation
* **NGINX** – Load balancer & reverse proxy
* **Flask** – Sample web application
* **Ubuntu Containers** – Target nodes

---

## Project Structure

```
.
├── docker-compose.yml
├── app/
│   ├── app.py
│   └── requirements.txt
├── ansible/
│   ├── inventory.ini
│   ├── deploy.yml
│   ├── roles/
│   │   ├── common/
│   │   ├── app/
│   │   ├── load_balancer/
│   │   ├── health_check/
│   │   └── rollback/
├── .env.example
└── README.md
```

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/<your-username>/blue-green-deployment.git
cd blue-green-deployment
```

---

### Start Infrastructure

```bash
docker-compose up -d
```

Verify:

```bash
docker ps
```

You should see:

* blue1, blue2
* green1, green2
* loadbalancer

---

### Install Dependencies (Host)

```bash
sudo apt install ansible docker-compose -y
```

---

### Verify Ansible Connectivity

```bash
ansible all -i ansible/inventory.ini -m ping
```

---

## Deployment

### Deploy New Version

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -e "app_version=v1.0.0"
```

---

### Test Application

```bash
curl http://localhost:8080
```

Example output:

```
Application Version: v1.0.0
```

---

## Blue-Green Deployment Flow

1. Detect active environment (Blue/Green)
2. Deploy new version to inactive environment
3. Run health checks (`/health`)
4. If successful → switch traffic via NGINX
5. If failure → rollback (no traffic switch)

---

## Health Check

* Endpoint: `/health`
* Expected response: `200 OK`
* Ensures new version is stable before switching traffic

---

## Rollback Mechanism

* Implemented using Ansible `block` and `rescue`
* If deployment or health check fails:

  * Traffic remains on previous stable environment
  * No downtime occurs

---

## Traffic Switching

* NGINX upstreams:

  * Blue → port 5000
  * Green → port 5001

* Switching happens via:

```nginx
proxy_pass http://<active_environment>;
```

* Applied using **graceful reload**:

```bash
nginx -s reload
```

---

## Idempotency

* Re-running the same deployment:

```bash
ansible-playbook deploy.yml -e "app_version=v2.0.0"
```

Produces:

```
changed=0
```

Ensuring:

* No unnecessary changes
* Stable infrastructure

---

## Testing Scenarios

### Successful Deployment

* Deploy new version
* Verify updated response

### Failure Scenario

* Break `/health` endpoint
* Deployment fails
* Traffic remains on old version

---

## Environment Variables

Example `.env.example`:

```
APP_VERSION=v1.0.0
```

---

## Key Learnings

* Blue/Green deployment strategy
* Infrastructure as Code (IaC)
* Ansible role-based automation
* Zero-downtime release techniques
* NGINX traffic routing
* Health-based deployment validation

---

## Future Improvements

* Add CI/CD pipeline (GitHub Actions / Jenkins)
* Add monitoring (Prometheus + Grafana)
* Use Kubernetes for scaling
* Add canary deployments

---

## Author

**Bharghav Sai Marla**

---

## Acknowledgment

This project demonstrates real-world DevOps practices for **reliable, scalable, and zero-downtime application deployments**.
