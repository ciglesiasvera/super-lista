from django.conf import settings


def site_config(request):
    return {
        'site_name': 'Superlista',
        'site_description': 'Tu gestor de listas de compras colaborativas',
    }
