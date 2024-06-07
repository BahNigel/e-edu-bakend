# Generated by Django 5.0.4 on 2024-06-06 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_coursematerial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VertualClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100, null=True)),
                ('m_link', models.CharField(max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_vertual_class', to='course.course')),
            ],
        ),
    ]