from django.db import models


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    prefer =  models.CharField(default=None, max_length=256)
    channel =  models.CharField(default=None, max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
        
class Settings(models.Model):
    name = models.CharField(default=None, max_length=128, unique=True)
    forum =  models.CharField(default=None, max_length=256)
    channel =  models.CharField(default=None, max_length=256)

        
class Hotnews(models.Model):

    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256,default='')
    
class Articles(models.Model):

    title = models.CharField(max_length=256)
    profile = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    link = models.CharField(max_length=256,default='')
    piclink = models.CharField(max_length=256,default='')
    authorlink = models.CharField(max_length=256,default='')
    
class Baidu_Hotnews(models.Model):

    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256,default='')
    
class Sina_Hotnews(models.Model):

    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256,default='')

    
class Sogo_Hotnews(models.Model):

    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256,default='')
    
    
class CSDN_Articles(models.Model):

    title = models.CharField(max_length=256)
    profile = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    link = models.CharField(max_length=256,default='')
    piclink = models.CharField(max_length=256,default='')
    authorlink = models.CharField(max_length=256,default='')
    
    
class Jianshu_Articles(models.Model):

    title = models.CharField(max_length=256)
    profile = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    link = models.CharField(max_length=256,default='')
    piclink = models.CharField(max_length=256,default='')
    authorlink = models.CharField(max_length=256,default='')
    
class Weixin_Articles(models.Model):

    title = models.CharField(max_length=256)
    profile = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    link = models.CharField(max_length=256,default='')
    piclink = models.CharField(max_length=256,default='')
    authorlink = models.CharField(max_length=256,default='')
    
    
# 新闻类别表
class cate(models.Model):
    cate_id = models.CharField(blank=False, max_length=64, verbose_name='ID',unique=True)
    cate_name = models.CharField(blank=False, max_length=64, verbose_name='名字')

    def __str__(self):
        return self.cate_name
    class Meta:
        db_table = 'cate'
        verbose_name_plural = "新闻类别表"

# 新闻与新闻相似表
class newsim(models.Model):
    new_id_base = models.CharField(blank=False, max_length=64, verbose_name="ID_base", unique=False)
    new_id_sim = models.CharField(blank=False, max_length=64, verbose_name="ID_sim", unique=False)
    new_correlation = models.FloatField(verbose_name="新闻相关度", blank=False)

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_id_base

    class Meta:
        db_table = 'newsim'
        verbose_name_plural = "新闻相似度表"


# 新闻表
class new(models.Model):
    new_id = models.CharField(blank=False, max_length=64, verbose_name="ID", unique=True)
    new_cate = models.ForeignKey(cate, related_name="类别", on_delete=False)
    new_time = models.DateTimeField(blank=False, verbose_name="发表时间")
    new_seenum = models.IntegerField(verbose_name="浏览次数", blank=False)  # True表示可不填
    new_disnum = models.IntegerField(verbose_name="跟帖次数", blank=False)  # True表示可不填
    # related_name定义主表对象查询子表时使用的方法名称
    new_title = models.CharField(blank=False, max_length=100, verbose_name="标题")
    new_content = models.TextField(blank=False, verbose_name="新闻内容")

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_title

    class Meta:
        db_table = 'new'
        verbose_name_plural = "新闻信息表"

# 新闻热度表
class newhot(models.Model):
    new_id = models.CharField(blank=False, max_length=64, verbose_name="ID", unique=True)
    new_cate = models.ForeignKey(cate, related_name="类别名", on_delete=False)
    new_hot = models.FloatField(verbose_name="热度值", blank=False)

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_id

    class Meta:
        db_table = 'newhot'
        verbose_name_plural = "新闻热度表"


# 新闻标签对应表
class newtag(models.Model):
    new_tag = models.CharField(blank=False, max_length=64, verbose_name="标签", unique=False)
    new_id = models.CharField(blank=False, max_length=64, verbose_name="ID", unique=False)
    new_hot = models.FloatField(verbose_name="热度值", blank=False)

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_tag

    class Meta:
        db_table = 'newtag'
        verbose_name_plural = "新闻标签表"

# 用户点击表
class newbrowse(models.Model):
    user_name = models.CharField(blank=False, max_length=64, verbose_name="用户名", unique=False)
    new_id = models.CharField(blank=False, max_length=64, verbose_name="ID", unique=False)
    new_browse_time = models.DateTimeField(blank=False, verbose_name="浏览时间")
    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'newbrowse'
        verbose_name_plural = "用户点击表"