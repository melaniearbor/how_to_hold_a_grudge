from django.contrib import admin

from grudge_cabinet.models import Grudge, Story


class GrudgeAdmin(admin.ModelAdmin):
    class Meta:
        model = Grudge
        fields = "__all__"

    readonly_fields = ["carat"]


admin.site.register(Grudge, GrudgeAdmin)
admin.site.register(Story)
