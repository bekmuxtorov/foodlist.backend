from django.db import models


class UserManager(models.Manager):
    def get_managers(self):
        return self.filter(type='manager')

    def get_customers(self):
        return self.filter(type='customer')
