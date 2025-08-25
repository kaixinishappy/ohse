from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Location(models.TextChoices):
    MENARA_SUNWAY = 'menara_sunway', _('Menara Sunway')


class Trainer(models.TextChoices):
    JOHN_DOE = 'john_doe', _('John Doe')


class UserRole(models.TextChoices):
    REPORTER = 'reporter', _('Reporter')
    APPROVER = 'approver', _('Approver')
    INVESTIGATOR = 'investigator', _('Investigator')
    GOHSE_TEAM = 'gohse_team', _('GOHSE Team')
    GOHSE_MANAGER = 'gohse_manager', _('GOHSE Manager')
    OBSERVER = 'observer', _('Observer')

# USER_ROLE = [
#     ('reporter', 'Reporter'), # 50
#     ('approver', 'Approver'), # 50
#     ('investigator', 'Investigator'), # 5
#     ('gohse_team', 'GOHSE Team'), # 3
#     ('gohse_manager', 'GOHSE Manager'), # 2
#     ('observer', 'Observer'), # 5
# ]


class UserProfile(models.Model):
    user_role = models.CharField(
        max_length=50, 
        choices=UserRole.choices,
        default=None
    )

    email = models.EmailField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_role



class OSHCoordinator(models.Model):
    name = models.CharField(max_length=100)

    location = models.CharField(
        max_length=50, 
        choices=Location.choices,
        default=Location.MENARA_SUNWAY
    )

    trainer = models.CharField(
        max_length=50, 
        choices=Trainer.choices,
        default=Trainer.JOHN_DOE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class FloorMarshall(models.Model):
    name = models.CharField(max_length=100)

    location = models.CharField(
        max_length=50, 
        choices=Location.choices,
        default=Location.MENARA_SUNWAY
    )

    trainer = models.CharField(
        max_length=50, 
        choices=Trainer.choices,
        default=Trainer.JOHN_DOE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class FirstAider(models.Model):
    name = models.CharField(max_length=100)

    location = models.CharField(
        max_length=50, 
        choices=Location.choices,
        default=Location.MENARA_SUNWAY
    )

    trainer = models.CharField(
        max_length=50, 
        choices=Trainer.choices,
        default=Trainer.JOHN_DOE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class News(models.Model):
    title = models.CharField(max_length=200)
    attachment = models.ImageField(upload_to="news/attachments/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"News: {self.title} - Created at: {self.created_at}"



class FAQ(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.title



class UserGuide(models.Model):
    user_role = models.CharField(
        max_length=50, 
        choices=UserRole.choices,
        default=None
    )

    attachment = models.ImageField(upload_to="user_guide/attachments/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_role

