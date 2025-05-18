from django.db import models

class ContactInfo(models.Model):
    email = models.EmailField()
    what_three_words = models.CharField(max_length=100)
    what_three_words_link = models.URLField()
    address = models.TextField()
    address_link = models.URLField()
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return self.address
