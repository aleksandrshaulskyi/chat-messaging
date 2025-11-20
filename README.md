# Chat-messaging.

The messaging microservice for the distributed chat system.

## Brief.

This microservice is intended to do all the heavy lifting tasks which are related to messages.
It consumes messages from RabbitMQ and then validates, enforces authorization policies
(PEP, PIP, PDP are all situated here), stores them into the database and publishes them back
to the RabbitMQ in order to be dispatched to the users later. Aside of that this service also works
with REST providing vital functionality for the whole system.

## Stage.
This service is in the stage of active development. Updates are released multiple times a week.

## Features.
This microservice operates with the two domain entities:

1) Chat
2) Message

It works both via AMQP and REST.

The first one is intended to handle the real-time communication while the second one serves
the data that is needed on request basis.

## Architecture.

This microservice is built using the Clean Architecture approach.
It consists of 4 layers which are:

1) Domain (entities, value objects)
2) Application layer (domain entities orchestration and business logic)
3) Interface adapters (thin transport layer that incapsulates the internal logic)
4) Infrastructure (frameworks, databases, etc.)

## Usage.

1) Clone the repository.
2) Create .env file in the backed directory using the env_example.txt as an example.
3) ```docker-compose up --build``` in the directory where docker-compose.yaml file is located.
4) The application will be available on **http://localhost:8002**

## Recent updates.

None yet released.

## Docs.

Available at the standard FastAPI docs endpoint **http://localhost:8002/docs**

## Back to Index repository of the whole chat system.

https://github.com/aleksandrshaulskyi/chat-index
