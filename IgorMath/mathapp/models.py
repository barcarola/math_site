from django.db import models

class MathStatistics(models.Model):
    session_date = models.DateField("Дата")
    total = models.IntegerField("Всего", null=True)
    count10_correct = models.IntegerField("Сложение до 10 правильных", null=True)
    count10_incorrect = models.IntegerField("Сложение до 10 неправильных", null=True)
    subtr10_correct = models.IntegerField("Вычитание до 10 правильных", null=True)
    subtr10_incorrect = models.IntegerField("Вычитание до 10 неправильных", null=True)
    equation10_correct = models.IntegerField("Уравнение до 10 правильных", null=True)
    equation10_incorrect = models.IntegerField("Уравнение до 10 неправильных", null=True)
    multiplication_correct = models.IntegerField("Умножение правильных", null=True)
    multiplication_incorrect = models.IntegerField("Умножение неправильных", null=True)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

class Index_image(models.Model):
    image = models.ImageField(upload_to='mathapp/static/images')