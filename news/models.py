from django.db import models

class Lunbo(models.Model):
    lunbo_url = models.CharField('轮播地址',max_length=256,default='')
    img = models.CharField('轮播图片',max_length=256,default='')
    lunbo_title = models.CharField('轮播标题',max_length=256)
    
    def __str__(self):
        return self.lunbo_title
        
    class Meta:
        verbose_name = "轮播"
        verbose_name_plural = "轮播"    
