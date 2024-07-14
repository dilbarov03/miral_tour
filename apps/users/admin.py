from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm

from apps.users.models import User, SavedTour, OrderPerson, Order, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = ('id', 'email', 'full_name', 'phone')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'full_name', 'phone')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(SavedTour)
class SavedTourAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour')
    list_display_links = ('id', 'user')
    search_fields = ('user__full_name', 'tour__title')
    list_per_page = 25


class OrderPersonInlineAdmin(admin.StackedInline):
    model = OrderPerson
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'tarif', 'total_price', 'status', 'currency')
    list_display_links = ('id', 'user')
    search_fields = ('user__full_name', 'tour__title')
    list_per_page = 25
    list_filter = ('status', 'tarif', 'tour')
    inlines = (OrderPersonInlineAdmin,)
    autocomplete_fields = ('user', 'tour', 'tarif')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_id', 'user', 'amount', 'currency', 'payment_status')
    list_display_links = ('id', 'payment_id')
    list_per_page = 25
    list_filter = ('payment_status', 'currency')
    autocomplete_fields = ('order', 'user')