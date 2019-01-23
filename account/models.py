from django.db import models


# Create your models here.
class account(models.Model):
    timezone = models.CharField(max_length=100)
    language = models.CharField(max_length=10)
    user = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )


class accountdeletion(models.Model):
    email = models.CharField(max_length=254)
    date_requested = models.DateTimeField()
    date_expunged = models.DateTimeField(null=True, default=None)
    user = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        default=None
    )


class emailaddress(models.Model):
    email = models.CharField(max_length=254)
    verified = models.SmallIntegerField()
    primary = models.SmallIntegerField()
    user = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )


class emailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(null=True, default=None)
    key = models.CharField(max_length=64)
    email_address = models.ForeignKey(
        'account.emailaddress',
        on_delete=models.CASCADE,
        null=False
    )


class signupcode(models.Model):
    code = models.CharField(max_length=64)
    max_uses = models.IntegerField()
    expiry = models.DateTimeField(null=True, default=None)
    email = models.CharField(max_length=254)
    notes = models.TextField()
    sent = models.DateTimeField(null=True, default=None)
    created = models.DateTimeField()
    use_count = models.IntegerField()
    inviter = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        default=None
    )


class signupcoderesult(models.Model):
    timestamp = models.DateTimeField()
    signup_code = models.ForeignKey(
        'account.signupcode',
        on_delete=models.CASCADE,
        null=False
    )
    user = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )
