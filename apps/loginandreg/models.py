from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid First Name! - Must be 2 characters long"
        if not (postData['first_name'].isalpha()) == True:
            errors['first_name'] = "Invalid First Name! - Can only contain alphabetic characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid Last Name! - Must be 2 characters long"
        if not (postData['last_name'].isalpha()) == True:
            errors['last_name'] = "Invalid Last Name! - Can only contain alphabetic characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        emailAlreadyExists = User.objects.filter(DBemail = postData['email']).exists()
        if (emailAlreadyExists):
            errors['email'] = "Email already in system"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['pwconfirm']:
            errors['confirmpw'] = "Password and Confirm Password must match"
        return errors
    def login_validator(self, postData):
        errors = {}
        loginemailAlreadyExists = User.objects.filter(DBemail = postData['emailLogin']).exists()
        if not (loginemailAlreadyExists):
            errors['loginemail'] = "Failure to log in"
        user = User.objects.get(DBemail=postData["emailLogin"])
        pw_to_hash = postData["passwordLogin"]
        if not bcrypt.checkpw(pw_to_hash.encode(), user.DBpassword.encode()):
            errors['loginemail'] = "Failure to log in"
        return errors


class User(models.Model):
    DBfirst_name = models.CharField(max_length = 255)
    DBlast_name = models.CharField(max_length = 255)
    DBemail = models.CharField(max_length = 255)
    DBpassword = models.CharField(max_length = 255)
    objects = UserManager()
    def __repr__(self):
        return f"<User object: {self.DBfirst_name} {self.DBlast_name} {self.DBemail} {self.DBpassword} ({self.id})>"
