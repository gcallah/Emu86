from django.db import models
from django.utils.text import slugify

HEADER_LEN = 128


class SingleNameModel(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class UrlModel(models.Model):
    url = models.CharField(max_length=256, default="",
                           blank=True, null=True)

    class Meta:
        abstract = True


class DescrModel(models.Model):
    descr = models.CharField(max_length=512, default="",
                             blank=True, null=True)

    class Meta:
        abstract = True


class AdminEmail(models.Model):
    email_addr = models.CharField(max_length=80, default="",
                                  blank=True, null=True)

    def __str__(self):
        return self.email_addr


# this model captures site specific info
class Site(SingleNameModel, UrlModel, DescrModel):
    header = models.CharField(max_length=HEADER_LEN, default="")

class Site(models.Model):
    name = models.CharField(max_length=128)
    header = models.CharField(max_length=128, default="")
    slug = models.SlugField(max_length=150, unique=True, editable=False, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:140] or "site"
            slug = base
            i = 2
            while Site.objects.filter(slug=slug).exists():
                suffix = f"-{i}"
                slug = f"{base[:140-len(suffix)]}{suffix}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)