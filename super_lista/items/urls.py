from django.urls import path

from super_lista.items.views import ItemSuggestView

urlpatterns = [
    # Autocomplete/suggest
    path('suggest/', ItemSuggestView.as_view(), name='item_suggest'),
]
