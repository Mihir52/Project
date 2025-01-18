from django.db import models

# Create your models here.
class User(models.Model):
    susertype = (
        ('member','Member'),
        ('watchman','Watchman'),
        ('chairman','Chairman')
    )
    usertype = models.CharField(max_length=10,choices=susertype)
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20,default='')
    sname = models.CharField(max_length=20,default='')
    mobile = models.IntegerField(default=0,blank=True)
    address = models.CharField(max_length=100,default='')
    profile = models.ImageField(default="", upload_to='profile/')

    def __str__(self):
        return (self.fname+" "+self.sname)
    
class Event(models.Model):
    eventname = models.CharField(max_length=20)
    eventdescription = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    createeventtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.eventname
    
class Notice(models.Model):
    noticename = models.CharField(max_length=20)
    noticedescription = models.TextField()
    createnoticetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.noticename