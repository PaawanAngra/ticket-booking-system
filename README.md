# High-Concurrency Ticket Booking System

A distributed backend service designed to handle "Flash Sale" scenarios where thousands of concurrent users attempt to book a limited inventory of tickets simultaneously. This project demonstrates core SDE-2 competencies including distributed locking, ACID transactions, and system observability.



## Key Features
* **Atomic Inventory Management:** Prevents double-booking using Redis Lua scripts for sub-millisecond atomic decrements.
* **Distributed Locking:** Ensures data integrity across multiple API instances.
* **Database Reliability:** Uses PostgreSQL with strict unique constraints and transaction isolation.
* **Performance Benchmarking:** Validated with Locust load-testing to handle 5k+ Requests Per Second (RPS).

## System Architecture
The system employs a multi-layered defense strategy:
1. **FastAPI (Application Layer):** Handles incoming REST requests asynchronously using Python's `async/await`.
2. **Redis (Caching Layer):** Acts as a high-speed buffer. Tickets are first "reserved" in Redis to avoid hitting the database disk for every request.
3. **PostgreSQL (Persistence Layer):** The final source of truth. Once a ticket is reserved in Redis, it is committed to the relational DB within a transaction block.

## Tech Stack
* **Language:** Python (FastAPI)
* **Primary DB:** PostgreSQL
* **In-Memory Store:** Redis
* **Infrastructure:** Docker & Docker Compose
* **ORM:** SQLAlchemy
* **Load Testing:** Locust

## Getting Started

### Prerequisites
* Docker and Docker Compose installed.

### Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ticket-booking-system.git](https://github.com/YOUR_USERNAME/ticket-booking-system.git)
   cd ticket-booking-system