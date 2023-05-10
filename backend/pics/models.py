from django.db import models

class Pic(models.Model):
    type = models.CharField(max_length=3)
    accuracy = models.FloatField(max_length=10)
    date = models.CharField(max_length=10) # dd.mm.yyyy
    time = models.CharField(max_length=5)  # 00:00

    def __str__(self):
        return self.type + ' ' + self.accuracy + ' ' + self.date + ' ' + self.time