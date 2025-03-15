# Generated by Django 5.0.4 on 2025-03-15 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIverseTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('leader_name', models.CharField(max_length=100)),
                ('leader_email', models.EmailField(max_length=254)),
                ('leader_phone', models.CharField(max_length=15)),
                ('college', models.CharField(max_length=200)),
                ('amount_paid', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DreambrushTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('leader_name', models.CharField(max_length=100)),
                ('leader_email', models.EmailField(max_length=254)),
                ('leader_phone', models.CharField(max_length=15)),
                ('college', models.CharField(max_length=200)),
                ('amount_paid', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AIverseMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='Registration.aiverseteam')),
            ],
        ),
        migrations.CreateModel(
            name='DreambrushMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='Registration.dreambrushteam')),
            ],
        ),
    ]
