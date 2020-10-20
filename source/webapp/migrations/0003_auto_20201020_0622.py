# Generated by Django 2.2 on 2020-10-20 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20201020_0504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'verbose_name': 'Товар в заказе', 'verbose_name_plural': 'Товары в заказе'},
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='amount',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='qty',
            field=models.IntegerField(default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
    ]
