from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Profile(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, blank=False)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Category')

    def __str__(self):
        return self.name


class List(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    rid = models.CharField(max_length=10, blank=False)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    ranking = models.IntegerField(default=0, blank=False)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='List')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='List')
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    modified_date = models.DateTimeField(default=datetime.now, blank=True)
    log = models.TextField(blank=True)

    def __str__(self):
        return self.title
