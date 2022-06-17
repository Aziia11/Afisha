from django.db import models


# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    director = models.ForeignKey(Director,
                                 on_delete=models.CASCADE,
                                 null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.text