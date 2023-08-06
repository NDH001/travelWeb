from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.utils.text import slugify
from unidecode import unidecode
from uuid import uuid4

def set_link(length=500,allow_null=True,allow_blank=False):
    return models.CharField(max_length=length,null=allow_null,blank=allow_blank)

def set_score(digit=3,decimal=1,allow_null=True,allow_blank=False):
    return models.DecimalField(max_digits=digit,decimal_places=decimal,null=allow_null,blank=allow_blank)

# an abstract img class
class ImgExtend(models.Model):
    img = set_link()
    img_local = set_link()

    class Meta:
        abstract =True

# an abstract base class that contains the base info
class BaseExtend(models.Model):
    id = models.UUIDField(primary_key=True) 
    city = models.ForeignKey('Cities',on_delete=models.CASCADE)
    name = models.CharField(max_length=50) 
    address = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        abstract=True

# an abstract class that has both the base and img and link attributes
class BaseLinkImgExtend(ImgExtend,BaseExtend):
    link = set_link(allow_null=False)

    class Meta:
        abstract = True

class BaseSlugExtend(BaseExtend):

    slug = models.SlugField(max_length= 500, null=True,allow_unicode=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
            print(self.slug)
        super().save(*args,**kwargs)

    class Meta:
        abstract = True
# ------------------------------------------------------------------- #
class Cities(ImgExtend):
    city = models.CharField(max_length=50,unique=True,null=False,blank=False,primary_key=True)
    link = models.CharField(max_length=500,null=False)
    slug = models.SlugField(null=True,blank=True,allow_unicode=True)

    def __str__(self):
        return str(self.city) 
    
    class Meta:
        db_table = '"traveldata"."cities"'

class Shops(BaseLinkImgExtend,BaseSlugExtend):
    rank = models.IntegerField(default=0)
    score = set_score()

    class Meta:
        ordering = ['-rank','-score']
        db_table = '"traveldata"."shops"'
    
    
class Foods(BaseLinkImgExtend,BaseSlugExtend):
    desc = models.CharField(max_length=500,null=True)
    address_link=models.CharField(max_length=500,null=True)

    class Meta:
        db_table = '"traveldata"."foods"'

class Sights(BaseLinkImgExtend,BaseSlugExtend):
    popularity = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    score = set_score()
    
    class Meta:
        ordering = ['-popularity','-score']
        db_table = '"traveldata"."sights"'

class Sights_texts(BaseExtend):
    time = models.CharField(max_length=200,null=True)
    tele = models.CharField(max_length=500,null=True)
    title = models.CharField(max_length=200,null=True)
    desc = models.CharField(max_length=10000,null=True)

    class Meta:
        db_table = '"traveldata"."sights_texts"'

class Sights_imgs(ImgExtend):
    id = models.BigAutoField(primary_key=True)
    sights = models.ForeignKey(Sights,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        db_table = '"traveldata"."sights_imgs"'


 




    
 







