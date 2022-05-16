from django.contrib import admin

from shop.models import TradePoint, Worker, WorkerVisit


class TradePointAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class WorkerAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class WorkerVisitAdmin(admin.ModelAdmin):
    fields = ('date', 'worker', 'trade_point', 'longitude', 'latitude')
    readonly_fields = ('date', )
    search_fields = ('worker__name', 'trade_point__name')


admin.site.register(TradePoint, TradePointAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(WorkerVisit, WorkerVisitAdmin)
