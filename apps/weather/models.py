from django.db import models


class WeatherCache(models.Model):
    city = models.CharField(max_length=100, db_index=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    temp_c = models.FloatField()
    feels_like_c = models.FloatField()
    condition_main = models.CharField(max_length=50)
    condition_description = models.CharField(max_length=120)
    is_rainy = models.BooleanField(default=False)
    is_snowy = models.BooleanField(default=False)
    wind_speed = models.FloatField(default=0)
    raw_response = models.JSONField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["city", "fetched_at"])]

    def __str__(self):
        return f"{self.city} {self.temp_c}°C @ {self.fetched_at}"
