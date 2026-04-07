from django.db import models


class Phase(models.Model):
	code = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=100, blank=True, default="")
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["code"]

	def __str__(self):
		return f"{self.code} - {self.name}" if self.name else self.code
