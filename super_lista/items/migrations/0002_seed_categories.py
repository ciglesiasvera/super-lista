"""Seed initial categories and system data for Superlista."""

from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('items', 'Category')
    categories = [
        ('Abarrotes', 'abarrotes'),
        ('Lácteos', 'lacteos'),
        ('Carnes', 'carnes'),
        ('Congelados', 'congelados'),
        ('Frutas', 'frutas'),
        ('Verduras', 'verduras'),
        ('Limpieza', 'limpieza'),
        ('Higiene Personal', 'higiene-personal'),
        ('Mascotas', 'mascotas'),
        ('Bebidas', 'bebidas'),
        ('Panadería', 'panaderia'),
        ('Condimentos', 'condimentos'),
        ('Enlatados', 'enlatados'),
        ('Otros', 'otros'),
    ]
    for name, slug in categories:
        Category.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'is_system': True,
                'is_active': True,
            },
        )


def reverse_seed(apps, schema_editor):
    Category = apps.get_model('items', 'Category')
    Category.objects.filter(is_system=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed),
    ]
