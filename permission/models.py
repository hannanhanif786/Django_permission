from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(email, password=password, name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user


#  Custom User Model
class User(AbstractBaseUser):
    role = [
        ("CA", "carrier Admin"),
        ("CM", "carrier manager"),
        ("CD", "carrier Driver"),
        ("BA", "Broker Admin"),
        ("BM", "Broker Manager"),
        ("BP", "Broker Processor"),
        ("FA", "Financer Admin"),
        ("FM", "Financer Manager"),
        ("FP", "Financer Processor"),
    ]

    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_role = models.CharField(max_length=2, choices=role)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    categorydesc = models.CharField(max_length=40)

    def __str__(self):
        return self.categorydesc


class Product(models.Model):
    name = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to="photos")

    def __str__(self):
        return self.name
