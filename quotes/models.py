from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.DateField()
    born_location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Quote(models.Model):
    tags = models.ManyToManyField(Tag, related_name='quotes')
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')

    def __str__(self):
        return self.quote
    
    from django.db import models

