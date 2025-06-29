from django.db import models

class WhoWeAre(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name = "Who We Are"
        verbose_name_plural = "Who We Are"

    def save(self, *args, **kwargs):
        if WhoWeAre.objects.exists() and not self.pk:  # If there's already an instance and it's a new entry
            raise Exception("Only one WhoWeAre instance is allowed!")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to="team_photos/", blank=True, null=True)

    def __str__(self):
        return self.name
