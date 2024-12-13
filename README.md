# SushiShop with LLM-Based Neuro-Consultant

SushiShop is an innovative web application designed for a seamless sushi delivery experience. Powered by cutting-edge language models (LLM), it features a neuro-consultant to enhance user interaction and provide tailored recommendations.

## Key Features

1. AI Neuro-Consultant:
   * Uses state-of-the-art LLMs for personalized customer support and recommendations.
   * Can answer customer queries, suggest menu items, and assist with navigating the store.
2. Dynamic Sushi Menu:
   * A regularly updated menu featuring seasonal novelties.
   * Includes detailed descriptions and high-quality images for every dish.
3. User-Friendly Design:
   * Responsive interface for smooth interaction on both desktop and mobile.
   * Intuitive navigation for exploring the menu, viewing promotions, and completing orders.
4. Efficient Order Processing:
   * Streamlined checkout experience.
   * Integration with payment gateways for secure transactions.
5. Custom Knowledge Base:
   * A proprietary knowledge base is used by the neuro-consultant to provide context-aware answers.

## Technologies Used

* Backend: Python (FastAPI/Django)
* Frontend: HTML/CSS/JavaScript
* AI Integration: OpenAI API, custom LLM training
* Database: PostgreSQL
* Deployment: Docker, Uvicorn
* DevOps: GitHub Actions for CI/CD

## Installation and Setup

## Pre-requisites

* Python 3.12 or higher
* Docker (optional for containerized deployment)
* API keys for the OpenAI service

## Running the Project on a Remote Server in Debug Mode

To deploy and run SushiShop on a remote server for development purposes (debug mode), follow these steps:

1. Update ALLOWED_HOSTS in Django settings
* Navigate to the settings file:

app/sushi_delivery_shop/settings.py

* Add the server’s IP address or domain name to the ALLOWED_HOSTS variable:

```
ALLOWED_HOSTS = ['your-server-ip', 'localhost', '127.0.0.1']
```

2. Configure API URLs in Django settings
* In the same settings file, update the following variables:

```
BASE_URL = "http://your-server-ip:8000"
CONSULTANT_API_URL = "http://your-server-ip:5000/api/get_answer"
```

Replace your-server-ip with the external IP address of your server (or 127.0.0.1 for local testing).

3. Export the Knowledge Base
* Navigate to the project folder and run the following command to generate an updated knowledge base for the neuro-consultant:

```
cd app
python manage.py chunks_export
```

4. Start the Django Web Application
* In the same directory, launch the web application, ensuring it listens on all network interfaces:

```
python manage.py runserver 0.0.0.0:8000
```

5. Start the Neuro-Consultant API
* Open another terminal, navigate to the api folder, and start the neuro-consultant:

```
cd path_to_api
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Notes:

* 0.0.0.0: Ensures the application is accessible from external devices (not just localhost).
* This setup runs both the Django application and the neuro-consultant in debug mode, which is not recommended for production environments.

Accessing the Application

* Open a web browser and navigate to:

`http://your-server-ip:8000`

* The neuro-consultant API will be available at:

`http://your-server-ip:5000/api/get_answer`

### Deployment in Production

For production deployment, consider using:

* Gunicorn or uWSGI with Nginx for Django.
* A managed environment or orchestrator for API services.

Feel free to customize further if needed!
