from django.shortcuts import render
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
import pika
import json


class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            
            # send tasks to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            print("RabbitMQ connection established!") 
            channel = connection.channel()
            channel.queue_declare(queue='tasks_queue', durable=True)
            message = {
                'id': task.id,
                'title': task.title,
                'priority': task.priority
            }
            print("Sending task to RabbitMQ...")
            channel.basic_publish(
                exchange='',
                routing_key='tasks_queue',
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # 消息持久化
            )
            connection.close()
            print("Task sent successfully!")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            return Response({
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
            })
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

@api_view(['POST'])
def update_task_status(request, task_id):
    """
    API for update task status
    """
    try:
        task = Task.objects.get(id=task_id)
        task.status = request.data.get('status', task.status)
        task.save()
        return Response({"message": "Task status updated successfully"})
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)