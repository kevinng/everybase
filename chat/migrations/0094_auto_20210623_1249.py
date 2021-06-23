# Generated by Django 3.1.2 on 2021-06-23 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0093_auto_20210622_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedataset',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('MENU', 'MENU'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('QNA', 'QNA'), ('CONNECT', 'CONNECT'), ('CONNECT_QUESTION', 'CONNECT_QUESTION'), ('CONNECT_ANSWER', 'CONNECT_ANSWER')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('MENU', 'MENU'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('QNA', 'QNA'), ('CONNECT', 'CONNECT'), ('CONNECT_QUESTION', 'CONNECT_QUESTION'), ('CONNECT_ANSWER', 'CONNECT_ANSWER')], db_index=True, max_length=200),
        ),
    ]
