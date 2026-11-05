from django.contrib import admin

from .models import Experiment, Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "date")
    search_fields = ("name",)


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "algorithm", "metric_name", "metric_value", "run_date")
    search_fields = ("name", "algorithm")
    list_filter = ("project", "algorithm")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Experiment, ExperimentAdmin)
