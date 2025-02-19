# Generated by Django 4.2.13 on 2024-12-02 16:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Censo',
            fields=[
                ('numeroDNI', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=128)),
                ('fechaNacimiento', models.CharField(max_length=8)),
                ('anioCenso', models.CharField(max_length=4)),
                ('codigoAutorizacion', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'censo',
            },
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCircunscripcion', models.CharField(max_length=16)),
                ('idMesaElectoral', models.CharField(max_length=16)),
                ('idProcesoElectoral', models.CharField(max_length=16)),
                ('nombreCandidatoVotado', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(1)])),
                ('marcaTiempo', models.DateTimeField(auto_now=True)),
                ('codigoRespuesta', models.CharField(default='000', max_length=3)),
                ('censo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votoAppWSServer.censo')),
            ],
            options={
                'db_table': 'voto',
            },
        ),
        migrations.AddConstraint(
            model_name='voto',
            constraint=models.UniqueConstraint(fields=('censo', 'idProcesoElectoral'), name='unique_blocking_voto'),
        ),
    ]
