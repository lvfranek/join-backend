from django.conf import settings
from django.db import models


class Task(models.Model):

    class Status(models.TextChoices):
        TODO = 'todo', 'To do'
        IN_PROGRESS = 'inProgress', 'In progress'
        AWAIT_FEEDBACK = 'awaitFeedback', 'Await feedback'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        URGENT = 'urgent', 'Urgent'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    due_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, default='Technical Task')
    assignees = models.JSONField(default=list, blank=True)
    subtasks = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title
