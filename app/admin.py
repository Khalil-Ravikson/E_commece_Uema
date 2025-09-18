from django.contrib import admin

# Register your models here.
from .models import Product # Importa o modelo Product que você criou

# A linha mágica que torna seus produtos gerenciáveis no admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)