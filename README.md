# MP3 Converter

MP3 Converter is a web application that allows users to upload video files and convert them to MP3 audio files. The application is built using Python, Docker, and Kubernetes.

## Features

- User authentication and authorization with JWT tokens
- Video file upload and conversion to MP3 format
- Asynchronous file conversion using RabbitMQ message queue
- Persistent storage for video files using MongoDB with GridFS
- Notification service to send email alerts upon conversion completion

## Architecture

The application is designed as a microservices architecture with the following components:

1. **Auth Service**: Handles user authentication and authorization using JWT tokens.
2. **Gateway Service**: Acts as the entry point for user requests, handling file uploads and forwarding conversion tasks to the RabbitMQ queue.
3. **Converter Service**: Consumes conversion tasks from the RabbitMQ queue, converts video files to MP3 format, and stores the output in MongoDB.
4. **Notification Service**: Sends email notifications to users upon successful conversion of their video files.

## Technologies Used

- Python
- Flask
- MySQL (for user authentication)
- JWT (for user authentication)
- Docker
- Kubernetes
- RabbitMQ
- MongoDB with GridFS
- MoviePy (for video to MP3 conversion)

## Setup and Installation

1. Clone the repository
2. Set up Docker and Kubernetes on your local machine
3. Build and push the Docker images for each service to a container registry
4. Apply the Kubernetes manifests to create the necessary resources (Deployments, Services, Ingress, etc.)
5. Configure the required environment variables (e.g., MySQL credentials, RabbitMQ credentials, MongoDB credentials, Gmail credentials for notification service)
6. Access the application through the endpoint
