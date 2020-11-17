from django.db import models

class CloakedLink(models.Model):
    page_title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    redirect = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + '; ' + self.page_title + '; ' + self.description + '; ' + str(self.redirect)