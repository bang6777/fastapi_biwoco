# 1. Setup and Enviroment 

## Enviroment
Python 3.12

## Running the Application

To run the application, follow these steps:

1. Navigate to the root directory of your project.

2. Run the following command:
    ```bash
    pip install -r requirements.txt
    python main.py --env local
    ```
3. To run the application using Docker, follow these steps:

    ```bash
    cd docker
    docker-compose build
    docker-compose up -d
    ```

This will build the Docker image and run the FastAPI application in a container. You can access it at `http://127.0.0.1:8000/docs`.

This will start the FastAPI application and you can access it at `http://127.0.0.1:8000/docs`.


# 2. Test 1
Overview again your requirement:
- Use MongoDB as the database
- Define a data schema and access patterns, including index strategies
- Use the FastAPI framework
- Utilize the Dependency Injector library
- A flexible project structure, designed to be easily scalable
- Optionally, integration with AWS services such as S3 for file upload APIs

```
fastapi_biwoco/
├── app/
│   ├── users/                              # User module
│   │   ├── adapter/
│   │   │   ├── router.py                   # User API routes
│   │   │   ├── input/                      # Input validation schemas
|   |   |   |   ├── api/                    # API request schemas
│   │   │   │   │   ├── init.py             # Declare router schemas
│   │   │   │   │   ├── v1/                 # API version 1
│   │   │   │   │   │   ├── request/        # Request schemas
│   │   │   │   │   │   │   ├── init.py     # Declare params request schemas
│   │   │   │   │   │   ├── response/       # Response schemas
│   │   │   │   │   │   │   ├── init.py     # Declare response schemas
│   │   │   │   │   │   ├── user.py         # Define endpoint-specific request/response schemas
│   │   │   ├── output/                     # Output schemas
│   │   │   │   ├── init.py
│   │   │   │   ├── user_repository.py      # User repository for database interaction
│   │   ├── application/
│   │   │   ├── services.py                 # User service for handling business logic
│   │   │   └── dto/                        # Data Transfer Objects
│   │   └── domain/
│   │       ├── entity.py                   # User entity definition (e.g., Pydantic model)
│   ├── server.py                           # FastAPI application setup
│   ├── container.py                        # Dependency injection container setup
├── core/
│   ├── config.py                           # App configurations
│   ├── db/                                 # Database-related utilities
│   │   ├── database.py                     # MongoDB connection setup
│   │   ├── mixins/                         # Mixins for database models
│   │   │   ├── timestamp.py                # Timestamp mixin
│   │   ├── redis/                          # Redis-related utilities
│   │   │   ├── redis_client.py             # Redis connection setup
│   ├── exceptions/                         # Custom exceptions
│   │   ├── init.py
│   │   └── custom_exceptions.py            # Custom exception classes
│   ├── helpers/
│   │   ├── init.py
│   │   ├── caches/
│   │   │   └── redis_backend.py            # Redis cache backend
│   │   |   └── cache_manager.py            # Cache manager
│   │   |   └── cache_tag.py                # Cache tag utility
│   │   |   └── custom_key_marker.py        # Custom key marker
│   │   |   └── base/                       # Base cache class
|   |   |   |   └── init.py
|   |   |   |   └── backend.py              # Base cache backend
|   |   |   |   └── key_marker.py           # Base key marker
│   │   ├── redis.py                        # Redis connection setup
│   │   ├── token.py                        # JWT token utility
│   ├── fastapi/
│   │   ├── dependencies/                   # Dependencies for FastAPI
│   │   │   ├── dependencies.py             # Declare dependencies
│   │   │   └── permission.py               # Permission dependencies
│   │   └── middleware/                     # Middleware
│   │       └── response_middleware.py      # Common response middleware
|   ├── celery_task/                        # Celery task
│   │   ├── init.py                         # Celery setup
|   |   ├── tasks.py                        # Celery tasks
├── main.py                                 # FastAPI entry point
├── .env                                    # Environment variables
```


- A clear and organized source code structure to meet specific requirements.
- Sentry integration for efficient error monitoring and resolution.
- Redis for managing user authentication workflows securely and efficiently.
- Celery for handling both background and recurring tasks, thereby improving application performance and user experience.
- dependency injection has been applied to facilitate easier management and inject of components 


# 3. Test 2
Overview again your requirement:
- This is very similar to the architect that we are using https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/mobile-web-serverless-RA.pdf?did=wp_card&trk=wp_card
- Please take a look, and describe how it works from your understanding, and any improvements or adjustments to make it better, easy to scale, ...

## Answer
``` 
Describe how it works from your understanding
```
## Architecture Overview

This architecture is made up of four main components:

### 1. Authentication and Authorization
Manages user access and permissions, ensuring only authorized users can interact with the system.

### 2. Business Logic
Defines the core functions and workflows, processing requests from users and executing the application’s specific tasks.

### 3. Data Storage and Management
Handles data persistence and retrieval, with different storage solutions for structured data and files.

### 4. CI/CD
Facilitates continuous integration and delivery, enabling efficient testing, deployment, and updates.

## Services in Use:

- **Amazon Cognito**: Manages user authentication, allowing users to log in securely.
- **API Gateway**: Routes incoming requests from the application to the appropriate backend service.
- **AWS Lambda**: Processes each request, executing specific business logic as defined by the application.
- **DynamoDB and S3**: DynamoDB stores structured data, while S3 handles file storage.
- **CloudFront**: Speeds up content delivery to users worldwide by caching content at edge locations.
- **CloudWatch and IAM**: CloudWatch enables monitoring and logging, while IAM (Identity and Access Management) manages security and permissions for resources.



