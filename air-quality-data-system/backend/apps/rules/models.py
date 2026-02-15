from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ProtectionRule(models.Model):
    class PopulationType(models.TextChoices):
        GENERAL = "GENERAL", "GENERAL"
        CHILDREN = "CHILDREN", "CHILDREN"
        ELDERLY = "ELDERLY", "ELDERLY"
        PATIENTS = "PATIENTS", "PATIENTS"
        SENSITIVE = "SENSITIVE", "SENSITIVE"

    rule_name = models.CharField(max_length=100)
    min_aqi = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(500)]
    )
    max_aqi = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(500)]
    )
    population_type = models.CharField(max_length=20, choices=PopulationType.choices)
    advice = models.TextField()
    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["population_type", "min_aqi", "max_aqi"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(min_aqi__lte=models.F("max_aqi")),
                name="ck_rule_min_le_max",
            )
        ]

    def __str__(self):
        return f"{self.rule_name} [{self.population_type}] {self.min_aqi}-{self.max_aqi}"

    def clean(self):
        super().clean()

        if self.min_aqi is None or self.max_aqi is None:
            return
        if self.min_aqi > self.max_aqi:
            raise ValidationError({"min_aqi": "min_aqi must be <= max_aqi."})

        # Interval overlap check within the same population type (inclusive ranges).
        qs = ProtectionRule.objects.filter(population_type=self.population_type)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        qs = qs.filter(min_aqi__lte=self.max_aqi, max_aqi__gte=self.min_aqi)
        if qs.exists():
            raise ValidationError(
                "AQI ranges must not overlap within the same population_type."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
