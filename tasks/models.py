from django.db import models

class Task(models.Model):
    TASK_STATUSES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=1)  # 1 = High, 2 = Medium, 3 = Low
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title