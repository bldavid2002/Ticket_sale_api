# Scalable High Currency Ticket Sale API

A scalable distributed backend designed to handle massive sudden traffic spikes. Built to demonstrate advanced DevOps principles such as caching message queuing and automated CI pipelines.

## Documentation

Architecture and System Design documentation is available in the Documentation folder.

## Quick Start

Ensure you have Docker and Docker Compose installed.

1. Clone the repository:
git clone https://github.com/bldavid2002/Ticket_sale_api.git

2. Build and start the services:
docker compose up --build -d

## Tech Stack

* FastAPI for the web framework
* PostgreSQL with declarative list partitioning for data storage
* Redis for caching
* RabbitMQ for message queuing
* GitHub Actions for automated CI and security scanning

## Kubernetes Deployment
To deploy the custom primary-replica database architecture to a local cluster:

- kubectl apply -f k8s/postgres-secret.yml
- kubectl apply -f k8s/postgres-primary.yml
- kubectl apply -f k8s/postgres-replica.yml

## Engineering Decisions and Solutions
- Automated Replication Cloning: The replica uses an initContainer that waits for the primary to become healthy and automatically clones data using pg_basebackup.

- Permission Management: Managed container permission mismatches between root-owned backup files and the non-root PostgreSQL process by integrating explicit chown and strict 0700 directory permissions into the initialization script.

- Network Authentication: Configured explicit replication roles and updated pg_hba.conf rules on the primary node to authorize cluster-internal streaming connections.