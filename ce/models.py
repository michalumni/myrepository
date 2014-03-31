from django.db import models

# Create your models here.


class Supplier(models.Model):
    supplierName = models.CharField(max_length=200)
    supplierSlug = models.CharField(max_length=200)
    def __unicode__(self):
        return self.supplierName

    # ...
    #pass


class Review(models.Model):
    supplier = models.ForeignKey(Supplier)
    timeSubmitted = models.DateTimeField('date published')
    rating = models.IntegerField()
    authorName = models.CharField(max_length=1000)
    reviewContent = models.TextField()
    published = models.BooleanField(default=False)
    # ...

