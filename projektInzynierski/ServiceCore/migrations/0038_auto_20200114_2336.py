# Generated by Django 2.1.4 on 2020-01-14 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ServiceCore', '0037_auto_20200114_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionexercise',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solution_exercise', to='ServiceCore.Solution'),
        ),
        migrations.AlterField(
            model_name='solutiontest',
            name='solution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='solution_test', to='ServiceCore.Solution'),
        ),
    ]