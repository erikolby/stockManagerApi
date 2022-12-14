# Generated by Django 4.1.3 on 2022-11-29 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfoliomanagerapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockSymbol', models.CharField(max_length=10)),
                ('price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('tradeOperation', models.CharField(max_length=4)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='portfoliomanagerapi.portfolio')),
            ],
        ),
    ]
