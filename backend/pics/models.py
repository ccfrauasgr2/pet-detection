from django.db import models


class Pic(models.Model):
    #type = models.CharField(max_length=3)
    #accuracy = models.FloatField(max_length=10)
    picture = models.CharField(max_length=10000000)
    date = models.CharField(max_length=10)  # dd.mm.yyyy
    time = models.CharField(max_length=8)  # 00:00:00

    def __str__(self):
        return self.date + ' ' + self.time


class Pet(models.Model):
    #image = models.CharField(max_length=10000000)
    #date = models.CharField(max_length=10) #01.01.1111
    #time = models.CharField(max_length=5)
    type = models.CharField(max_length=32)
    accuracy = models.FloatField()
    bid = models.IntegerField()
    foreignKey = models.ForeignKey(Pic, on_delete=models.CASCADE)

    # json_data = models.JSONField()

    def __str__(self):
        return self.bid  # + ' ' + self.json_data
