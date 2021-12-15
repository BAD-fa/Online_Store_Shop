from django.db import models
from User.models import Profile, Customer


# abstract
class Image(models.Model):
    pass


class Video(models.Model):
    pass


class Comment(models.Model):
    pass


class Address(models.Model):
    pass
