# Generated by Django 3.2.7 on 2021-10-05 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentFor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('slug', models.SlugField(unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['title'],
            },
        ),
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='shop.category'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='shop.Tag'),
        ),
    ]