from django.db import models
from rest_framework import serializers

# Create your models here.
class task(models.Model):
    name = models.CharField(max_length=50)
    is_completed = models.BooleanField(default=False)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class taskSerializer(serializers.Serializer):
    class Meta:
        model = task
        fields = '__all__'
        