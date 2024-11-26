import pika
import json
import time
import requests  # for callingback updates for task status

from datetime import datetime
from elasticsearch import Elasticsearch

es=Elasticsearch("http://localhost:9200")

def process_task(task):
    """
    SIMULATION OF TASKS HERE!
    """
    start_time=time.time()
    print(f"Processing task: {task['title']} with priority {task['priority']}")
    time.sleep(2)  # Simulate task processing time
    end_time=time.time()

    performance_data={
        "task_id": task["id"],
        "title": task["title"],
        "priority": task["priority"],
        "status": "COMPLETED",
        "processing_time": round(end_time - start_time, 2),
        "timestamp": datetime.now().isoformat()
    }
    es.index(index="task_performance", document=performance_data)



    return True  # response if task is executed successfully

def update_task_status(task_id, status):
    """
    Call the API of the task management service to update the task status
    """
    url = f"http://127.0.0.1:8000/tasks/{task_id}/update/"  # 假设更新状态的 API
    payload = {"status": status}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Task {task_id} status updated to {status}")
        else:
            print(f"Failed to update task {task_id} status: {response.status_code}")
    except Exception as e:
        print(f"Error updating task status: {e}")

def main():
    """
    Main：consume RabbitMQ queue
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks_queue', durable=True)

    def callback(ch, method, properties, body):
        print(f"Received raw body: {body}") 
        task = json.loads(body)
        print(f"Received task: {task}")
        success = process_task(task)
        status = "COMPLETED" if success else "FAILED"
        update_task_status(task["id"], status)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 确认消息已处理

    channel.basic_consume(queue='tasks_queue', on_message_callback=callback)
    print("Worker is waiting for tasks...")
    channel.start_consuming()

if __name__ == "__main__":
    main()