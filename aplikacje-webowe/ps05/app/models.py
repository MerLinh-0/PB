from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


class Experiment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    algorithm = models.CharField(max_length=200)
    parameters = models.TextField()
    metric_name = models.CharField(max_length=200)
    metric_value = models.DecimalField(max_digits=12, decimal_places=4)
    run_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"

    def __str__(self):
        return f"{self.name} - {self.algorithm}"
