# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from _datetime import datetime


class Amount(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text


class WallUnitBrand(models.Model):
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CompetitorBrand(models.Model):
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Contract(models.Model):
    from_dt = models.DateTimeField(db_column='from', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    to_dt = models.DateTimeField(blank=True, null=True)
    renewable = models.BooleanField(blank=True, null=True)
    amount = models.ForeignKey(Amount, models.PROTECT, db_column='amount', blank=True, null=True)
    payment = models.ForeignKey('PaymentType', models.PROTECT, db_column='payment', blank=True, null=True)
    remark = models.ForeignKey('Remark', models.PROTECT, db_column='remark', blank=True, null=True)
    outlet = models.ForeignKey('Outlet',models.PROTECT)
    
    def __str__(self):
        return "Contract"+self.outlet.name

class EstimatedSales(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text


class Media(models.Model):
    path = models.TextField(blank=True, null=True)



class Outlet(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    size = models.ForeignKey('Size', models.DO_NOTHING, db_column='size', blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    estimated_sales = models.ForeignKey(EstimatedSales, models.DO_NOTHING, db_column='estimated', blank=True, null=True)
    user = models.ForeignKey(User,models.DO_NOTHING,blank=True, null=True)
    is_retail = models.BooleanField(blank=True, null=True)
    medias = models.ManyToManyField(Media,blank=True)
    
    def __str__(self):
        return self.name

class PaymentType(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text


class UserProfile(models.Model):
    mobile = models.IntegerField(null = True, blank=True)
    profile_pic = models.CharField(max_length= 255,null = True, blank=True)
    user = models.OneToOneField(User,models.DO_NOTHING)
    phone = models.CharField(max_length=64, null=True, default=None)
    local_password = models.CharField(max_length=255, null=True, default=None)
    
    def __str__(self):
        return self.user.first_name + " "+self.user.last_name
    
    
#Trigger a userprofile creation upon the creation of a user account
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
    
class Remark(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text

class Size(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text


class TrackUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    location_dt = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.user.first_name +" " +self.user.last_name +",date  "+self.location_dt.strftime("%B %d, %Y")


class WallUnitType(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text


class Wallunit(models.Model):
    outlet = models.ForeignKey(Outlet, models.CASCADE, db_column='outlet', blank=True, null=True)
    brand = models.ForeignKey(WallUnitBrand, models.DO_NOTHING, db_column='brand', blank=True, null=True)
    wall_unit_type = models.ForeignKey(WallUnitType, models.DO_NOTHING, db_column='type', blank=True, null=True)
    medias = models.ManyToManyField(Media,related_name="medias")
    def __str__(self):
        return self.outlet.name