from django.contrib import admin
from .models import Movie,Review
from .models import Order


admin.site.register(Movie)  
admin.site.register(Review)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
