from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    director = models.ForeignKey(Director,
                                 on_delete=models.CASCADE,
                                 null=True)

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [i for i in self.tags.all()]

    @property
    def rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        average = 0
        for i in reviews:
            average += i.stars
        return average / reviews.count()

#from statistics import sum
#def rating_average(average, reviews)
#return "If not reviews,so they just forget to write it" if (sum(average) / len(reviews.count))


STAR_CHOICES = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)
class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(default=1)
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return self.text