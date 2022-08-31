import hashlib
from django.urls import reverse
import this
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .validators import validar_gt_0, validar_lt_10
import rsa
from django.template.defaultfilters import slugify
import hashlib
from django.core.exceptions import ValidationError


class Member(User):

    publicKey = models.TextField(null=True, max_length=600)
    privateKey = models.TextField(null=True, max_length=600)
    #permission

    #subjects

    def save(self, *args, **kwargs):

        if not self.publicKey or not self.privateKey:

            p_key, pr_key = rsa.newkeys(512)
            self.publicKey = str(p_key)
            self.privateKey = str(pr_key)

            print(self.publicKey)

        super(Member, self).save(*args, **kwargs)



class Block(models.Model):

    previousHash = models.CharField(max_length=256, null=True)

    index = models.IntegerField(default=0, null=True)

    validation = models.BooleanField(default=False)

    #-------------------------
    emiter = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, related_name="emited")

    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, related_name="received")

    text = models.TextField(null=True)

    description = models.TextField(null=True)#only teachers

    score = models.IntegerField(
        default=0, validators=[validar_gt_0, validar_lt_10]
    ) #only teachers
    #-------------------------

    date =models.DateTimeField()

    hash = models.CharField(max_length=256, null=True)

    slug = models.SlugField(unique=True, null=True)

    def max_index(self):
        index2 = 0
        while(1):
            try:
                b = Block.objects.get(index=index2+1)
                index2 = index2 + 1
                
            except BaseException:
                return index2
        

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        self.slug = slugify(
                (self.index, self.date.strftime("%d-%b-%Y-%H-%M-%S"), self.emiter)
            )

        if not self.index or not self.previousHash:
            self.index = self.max_index()
            self.index = self.index + 1
            self.previousHash = "-1"

            if self.receiver == self.emiter:
                    raise ValidationError("Emiter and receiver can't be the same")

            try:

                previousBlock = Block.objects.get(index = (self.index - 1))
                self.previousHash = hashlib.sha256(previousBlock.__str__().encode('utf-8')).hexdigest()
            except BaseException:
                pass
            self.hash = hashlib.sha256(self.__str__().encode('utf-8')).hexdigest()

        
        super(Block, self).save(*args, **kwargs)

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s|%s|%s|%s|%s|%s|%s|%s|%s' % (
                self.index,
                self.previousHash,
                self.validation,
                self.emiter.username,
                self.receiver.username,
                self.text,
                self.description,
                self.score,
                self.date
            )
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('detail', kwargs={'slug': self.slug})

