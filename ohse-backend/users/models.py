from email.policy import default
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

# Create your models here.

class Location(models.TextChoices):
    MENARA_SUNWAY = 'menara_sunway', _('Menara Sunway')


class Trainer(models.TextChoices):
    OSH_COORDINATOR = 'osh_coordinator', _('OSH Coordinator') 


class UserRole(models.TextChoices):
    REPORTER = 'reporter', _('Reporter')
    APPROVER = 'approver', _('Approver')
    INVESTIGATOR = 'investigator', _('Investigator')
    GOHSE_TEAM = 'gohse_team', _('GOHSE Team')
    GOHSE_MANAGER = 'gohse_manager', _('GOHSE Manager')
    OBSERVER = 'observer', _('Observer')


# 23 Business Units (BU)
class BusinessUnit(models.TextChoices):
    GROUP_SECURITY = 'group_security', _('Group Security')
    DCMS = 'dcms', _('DCMS')
    GBMC = 'gbmc', _('GBMC')
    GIAD = 'giad', _('GIAD')
    DSI = 'dsi', _('Digital & Strategic Investment (DSI)')
    DECOSTYLE = 'decostyle', _('Decostyle')
    SUNWAY_LEASING_RISK = 'sunway_leasing_risk', _('Sunway Leasing and Risk')
    CREDIT_BUREAU_MALAYSIA_SDN_BHD = 'credit_bureau_malaysia_sdn_bhd', _('Credit Bureau Malaysia Sdn Bhd')
    FINANCE_SHARED_SERVICES_CENTRE_SDN_BHD = 'finance_shared_services_centre_sdn_bhd', _('Finance Shared Services Centre Sdn Bhd')
    SUNWAY_COMPUTER_SERVICES_SDN_BHD = 'sunway_computer_services_sdn_bhd', _('Sunway Computer Services Sdn Bhd')
    SUNWAY_MONEY = 'sunway_money', _('Sunway Money')
    GROUP_SECRETARIAL = 'group_secretarial', _('Group Secretarial')
    GROUP_ACCOUNTS = 'group_accounts', _('Group Accounts')
    GROUP_LEGAL = 'group_legal', _('Group Legal')
    GROUP_CFO = 'group_cfo', _('Group CFO')
    GBMC_18 = 'gbmc_18', _('GBMC 18')
    GROUP_HR = 'group_hr', _('Group HR')
    SUNWAY_TRAVEL = 'sunway_travel', _('Sunway Travel')
    SUNWAY_DESIGN = 'sunway_design', _('Sunway Design')
    DIGITAL_HUB = 'digital_hub', _('Digital Hub')
    HRSSC = 'hrssc', _('HRSSC')
    SUNWAY_PALS = 'sunway_pals', _('Sunway Pals')
    SUNWAY_QUANTUM = 'sunway_quantum', _('Sunway Quantum')



class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid4, 
        editable=False
    )

    is_active = models.BooleanField(default=True)

    name = models.CharField(max_length=255)
    email = models.EmailField(("email address"), max_length=100)

    user_role = models.CharField(
        max_length=50, 
        choices=UserRole.choices,
        null=True,
        blank=True,
        default=None
    )

    business_unit = models.CharField(
        max_length=50, 
        choices=BusinessUnit.choices,
        null=True,
        blank=True,
        default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Check user role
    @property
    def is_reporter(self):
        return self.groups.filter(name=UserRole.REPORTER).exists()

    @property
    def is_approver(self):
        return self.groups.filter(name=UserRole.APPROVER).exists()

    @property
    def is_investigator(self):
        return self.groups.filter(name=UserRole.INVESTIGATOR).exists()

    @property
    def is_gohse_manager(self):
        return self.groups.filter(name=UserRole.GOHSE_MANAGER).exists()
    
    @property
    def is_gohse_team(self):
        return self.groups.filter(name=UserRole.GOHSE_TEAM).exists()
    
    @property
    def is_observer(self):
        return self.groups.filter(name=UserRole.OBSERVER).exists()


    def __str__(self):
        return f'{self.name} - {self.user_role}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user_role:
            group, created = Group.objects.get_or_create(name=self.user_role)
            self.groups.clear()  # optional: remove from other groups
            self.groups.add(group)



# class UserProfile(models.Model):
#     user_role = models.CharField(
#         max_length=50, 
#         choices=UserRole.choices,
#         default=None
#     )

#     email = models.EmailField(max_length=100)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user_role



class OSHCoordinator(models.Model):
    name = models.CharField(max_length=100)

    location = models.CharField(
        max_length=50, 
        choices=Location.choices,
        null=True,
        blank=True,
        default=None
    )

    trainer = models.CharField(
        max_length=50, 
        choices=Trainer.choices,
        null=True,
        blank=True,
        default=None
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
        null=True,
        blank=True,
        default=None
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
        null=True,
        blank=True,
        default=None
    )

    trainer = models.CharField(
        max_length=50, 
        choices=Trainer.choices,
        null=True,
        blank=True,
        default=None
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

