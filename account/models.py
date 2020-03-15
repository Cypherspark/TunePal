import hashlib, binascii, os

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    FEMALE = 'Female'
    MALE = 'Male'
    TYPE_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=MALE,
    )
    username = models.CharField( max_length=255,
        help_text=('Required. 255 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'), unique=True)
    first_name = models.CharField( max_length=255, blank=True)
    last_name = models.CharField( max_length=255, blank=True)
    email = models.EmailField( blank=True, unique=True)
    birthdate = models.DateField(null=True)
    password = models.CharField( max_length=255, blank=True)
    
    def hash_password(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password