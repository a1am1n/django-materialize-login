# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.ForeignKey(User)
    
    def __unicode__(self):
        return "%s %s %s" %(self.user.first_name, self.user.last_name, self.user.e_mail)
    
