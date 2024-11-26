from django.urls import path
from .views import TaskCreateView, update_task_status, TaskDetailView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:task_id>/update/', update_task_status, name='task-update'),
    path('<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),

]