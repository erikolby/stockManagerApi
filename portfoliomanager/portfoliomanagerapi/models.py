from django.db import models

class Stock(models.Model):
    symbol = models.CharField(null=False, unique=True, max_length=10)
    name = models.CharField(null=False, max_length=100)

    @classmethod
    def create(cls, **kwargs):
        stock = cls.objects.create(
            symbol=kwargs['symbol'],
            name=kwargs['name']
        )
        return stock

class Portfolio(models.Model):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(null=False)
    initialAccountBalance = models.IntegerField(null=False)
    accountBalance = models.IntegerField(null=False)

class Trade(models.Model):
    stockSymbol = models.CharField(null=False, max_length=10)
    price = models.IntegerField(null=False)
    volume = models.IntegerField(null=False)
    portfolio = models.ForeignKey(Portfolio, related_name='trades', on_delete=models.CASCADE)
    tradeOperation = models.CharField(null=False, max_length=4)