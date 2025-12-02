# Chat-messaging.

##Message persistence, validation, authorization & event publishing##

This microservice performs all core operations related to message lifecycle in the distributed chat system — from ingestion to persistence to event publishing. It is the backbone of message flow.

## 🚀 Overview

```chat-messaging``` is responsible for all heavy-duty backend tasks related to chat messages.
It consumes events from RabbitMQ, applies strict validation and authorization logic, stores messages in a dedicated database, and publishes resulting events back to RabbitMQ for further delivery to users via the transportation layer.

In addition to event-driven flows, this service exposes a REST API used by the frontend and other services for fetching chats, messages and providing essential data for the system.

## 🧩 Features

- Consume messages from RabbitMQ
- Validate payload
- Enforce authorization policies (PEP / PIP / PDP live inside this service)
- Get-or-create chat records when needed
- Persist messages to MongoDB
- Assign per-chat sequence numbers
- Publish MessageCreated events back to RabbitMQ (transactional outbox)
- Provide REST endpoints for chats and messages retrieval

This service performs the main business logic of the entire chat system.

## 🧠 Domain Model

This microservice manages two domain entities:

- **Chat**
- **Message**

AMQP is used for real-time message flow, while REST serves on-demand operations (fetch history, chat info, etc.).

## 🏛️ Architecture

This service is built using Clean Architecture with clear boundaries between layers:

- Domain  
Entities, value objects, domain rules

- Application Layer  
Use-cases, orchestration, business logic

- Interface Adapters  
Controllers, DTO mappers

- Infrastructure  
Databases, framework integrations, message brokers

This separation keeps the core logic framework-agnostic and fully testable.

## ⚙️ Usage

1) Clone the repository
2) Create a .env file inside the backend directory using env_example.txt
3) The example contains no sensitive values — you may copy it as-is
4) Run the service: ```docker-compose up --build```

After startup, the service is available at:

👉 http://localhost:8002

REST documentation (FastAPI Swagger UI):

👉 http://localhost:8002/docs

## 🔗 Back to the Main Index Repository

https://github.com/aleksandrshaulskyi/chat-index
