# Microservice Application Documentation

## Overview

This microservice application consists of three separate services:

* **user-service**
* **post-service**
* **analyst-service**

Each service is designed to perform specific tasks and communicate with each other using RabbitMQ and Redis.

## Services

### User-Service

* **CRUD Routers:** Create, Read, Update, and Delete users  
* **RabbitMQ Integration:** Send email notifications to users using RabbitMQ and SMTP server  
* **Postgres Database:** Store user data in a separate Postgres database  

### Post-Service

* **CRUD Routers:** Create, Read, Update, and Delete posts  
* **Postgres Database:** Store post data in a separate Postgres database  

### Analyst-Service

* **Scheduled Tasks:** Run every 10 minutes to fetch data from user-service and post-service using GET requests  
* **Matching Algorithm:** Match users with posts and calculate the number of posts for each user  
* **Redis Storage:** Store analytics data in Redis with `user_id` as the key and analytics data as the value  

## Requirements

* **Database:** Postgres  
* **Message Broker:** RabbitMQ  
* **Cache:** Redis  
* **Programming Language:** Python  
* **Web Framework:** FastAPI  

## Deployment

Each service has its own Dockerfile and docker-compose file. To deploy and run each service separately, follow these steps:




## Installation and Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/DmytroDD2/microservices_project.git
    ```

### User-Service

1. **Navigate to the `user_service` directory:**
   ```bash
   cd user_service
   ```

2. **Create a `.env` file** with the following content:

    ```env
     SMTP_USER='your_email@gmail.com'
     SMTP_PASS='your_secure_password_here'
    ```

3. **Run using Docker:**
    ```bash
    docker-compose build
    docker network create microservices-network
    docker-compose up 
    ```

### Post-Service

1. **Navigate to the `post_service` directory:**
   ```bash
   cd post_service

2. **Run using Docker:**
    ```bash
    docker-compose up --build
    ```


### Analyst-Service

1. **Navigate to the `analyst_service` directory:**
   ```bash
   cd analyst_service
   ```
2. **Run using Docker:**
    ```bash
    docker-compose up --build
    ```

## Documentation

* **User Service:** http://localhost:8001/docs#/
* **Post Service:** http://localhost:8002/docs#/
* **Analyst Service:** http://localhost:8003/docs#/