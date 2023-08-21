from django.contrib import admin

from users.models import User, Favorite

# admin.site.register(User)
# admin.site.register(Favorite)


class FavoriteInline(admin.TabularInline):
    model = Favorite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [FavoriteInline,]
