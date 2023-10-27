# Generated by Django 4.2.6 on 2023-10-27 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('text', 'Text'), ('intger', 'Intger'), ('float', 'Float'), ('option', 'Option'), ('multi_option', 'Multi Option')], default='text', max_length=16)),
                ('required', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
            },
        ),
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Option Group',
                'verbose_name_plural': 'Option Groups',
            },
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('track_stock', models.BooleanField(default=True)),
                ('require_shipping', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Product Class',
                'verbose_name_plural': 'Product Class',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('text', 'Text'), ('intger', 'Intger'), ('float', 'Float'), ('option', 'Option'), ('multi_option', 'Multi Option')], default='text', max_length=16)),
                ('required', models.BooleanField(default=False)),
                ('option_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.optiongroup')),
                ('options', models.ManyToManyField(to='catalog.option')),
                ('product_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalog.productclass')),
            ],
            options={
                'verbose_name': 'Product Attribute',
                'verbose_name_plural': 'Product Attributes',
            },
        ),
        migrations.CreateModel(
            name='OptionGroupValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.optiongroup')),
            ],
            options={
                'verbose_name': 'Option Group Value',
                'verbose_name_plural': 'Option Groups Values',
            },
        ),
        migrations.AddField(
            model_name='option',
            name='option_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.optiongroup'),
        ),
    ]
