# Generated by Django 5.0.2 on 2024-03-09 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0006_refeicao_opcao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcao',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='opcao'),
        ),
    ]
