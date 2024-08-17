from django.db import models

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.author} - {self.text}"

class users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.TextField(max_length=20)

    def __str__(self):
        return self.username