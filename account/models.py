# Create your models here.

from django.contrib.auth.models import User

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



class UserManager(BaseUserManager):
    def create_user(self, userId, productionKey, password=None):
        if not userId:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            userId= userId,
            productionKey=productionKey,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, last_name, first_name, password):
        user = self.create_user(
            userId=userId,
            password=password,
            last_name = last_name,
            first_name = first_name
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(
        verbose_name="User_ID",
        max_length=10,
        unique=True
    )
    productionKey = models.IntegerField(
        verbose_name=_("production_key")
    )
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
    )

    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )

    salt = models.CharField(
        verbose_name=_('Salt'),
        max_length=10,
        blank=True
    )

    loginCount = models.IntegerField(
        default=5
    )
    objects = UserManager()
    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['productionKey', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    # def __str__(self):
    #     return self.nickname
    #
    # def get_full_name(self):
    #     return self.nickname
    #
    # def get_short_name(self):
    #     return self.nickname
    #
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    # get_full_name.short_description = _('Full name')
