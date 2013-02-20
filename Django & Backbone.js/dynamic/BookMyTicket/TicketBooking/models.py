from django.db import models 

class Language(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Movie(models.Model):
    language = models.ForeignKey(Language)
    movie = models.CharField(max_length=500)
    #def __unicode__(self):
    #    return self.movie