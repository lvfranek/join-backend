from rest_framework import serializers

from tasks_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    dueDate = serializers.DateField(source='due_date', required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'dueDate',
            'category',
            'assignees',
            'subtasks',
        ]

    def validate_subtasks(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Subtasks must be a list.')
        for subtask in value:
            if not isinstance(subtask, str):
                raise serializers.ValidationError('Each subtask must be a text.')
        return value

    def validate_assignees(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Assignees must be a list.')
        required_keys = {'id', 'name', 'initials', 'color'}
        for assignee in value:
            if not isinstance(assignee, dict) or not required_keys.issubset(assignee):
                raise serializers.ValidationError(
                    'Each assignee needs id, name, initials and color.'
                )
        return value
