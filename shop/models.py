from django.db import models


class Worker(models.Model):
    name = models.CharField(verbose_name='Имя сотрудника', max_length=255)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=12, unique=True)

    def __str__(self):
        return self.name


class TradePoint(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    workers = models.ManyToManyField(Worker)

    def __str__(self):
        return self.name


class WorkerVisit(models.Model):
    date = models.DateTimeField(verbose_name='Дата посещения', editable=False)
    trade_point = models.ForeignKey(TradePoint, null=False, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, null=False, on_delete=models.CASCADE)
    longitude = models.CharField(verbose_name='Долгота', max_length=255)
    latitude = models.CharField(verbose_name='Широта', max_length=255)

    def __str__(self):
        return f'{self.worker} - {self.trade_point}'
