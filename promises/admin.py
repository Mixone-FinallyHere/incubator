from django.contrib import admin

from promises.models import Promise, Slot


@admin.register(Promise)
class PromiseAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'stop', 'is_sure')


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('start', 'stop', 'is_weekly_recurrent')
