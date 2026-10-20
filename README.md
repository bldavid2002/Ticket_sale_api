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
