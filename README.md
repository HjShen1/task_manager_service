# Django Task Management System

This project is a task management system built with Django. It allows users to create, manage, and monitor tasks. The system also integrates with RabbitMQ for task queuing and Elasticsearch for performance monitoring, with Grafana providing visualized metrics.

## Features

	•	Submit tasks with priority levels.
	•	Manage task statuses (e.g., Pending, Completed, Failed).
	•	Real-time task processing using RabbitMQ.
	•	Performance monitoring via Elasticsearch and Grafana.
	•	Scalable architecture suitable for distributed systems.

## Tech Stack

	•	Backend: Django, Django REST Framework
	•	Message Queue: RabbitMQ
	•	Database: SQLite (default), PostgreSQL (optional)
	•	Monitoring: Elasticsearch, Grafana
	•	Frontend: React (optional)

## Requirements

	•	Python 3.8+
	•	RabbitMQ
	•	Elasticsearch 7.x
	•	Grafana
	•	Docker (optional, for containerized setup)

## Setup Instructions

1. Clone the repository

git clone https://github.com/your-username/your-repo.git
cd your-repo

2. Set up the virtual environment

python3 -m venv env
source env/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Start RabbitMQ and Elasticsearch

If you are using Docker:

docker-compose up -d

Otherwise, start RabbitMQ and Elasticsearch manually.

5. Run the Django server

	1.	Apply migrations:

        python manage.py makemigrations
        python manage.py migrate


	2.	Start the development server:

        python manage.py runserver

## How to Use

	1.	Submit a task:
	•	Use the endpoint: POST /tasks/create/ with JSON data:

{
  "title": "Test Task",
  "description": "Description of the task",
  "priority": 1
}


	2.	Monitor tasks:
	•	Navigate to Grafana dashboards to view metrics such as task throughput and latency.


## License

This project is licensed under the MIT License.


