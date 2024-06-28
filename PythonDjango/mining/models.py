from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
import requests
from bs4 import BeautifulSoup


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    advertiser_name = models.CharField(max_length=255)
    advertiser_link = models.URLField()
    publication_date = models.DateField(null=True, blank=True)
    submission_deadline = models.DateField(null=True, blank=True)
    bvpz_code = models.CharField(max_length=50)
    purchase_type = models.CharField(max_length=50)
    advertisement_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()

    def __str__(self):
        return self.email


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Now you can access the HTML of the page with the soup object
    # For example, to print out all the text inside <p> tags:
    for p in soup.find_all("p"):
        print(p.get_text())


scrape_website("http://example.com")
