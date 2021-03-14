from django.db import models


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
        ('none', "保密"),
    )

    name = models.CharField('用户名',max_length=128, unique=True)
    password = models.CharField('密码', max_length=256)
    email = models.EmailField('邮箱', unique=True)
    sex = models.CharField('性别', max_length=32, choices=gender, default="保密")
    c_time = models.DateTimeField(auto_now_add=True)
    prefer =  models.CharField(blank=True, default='', max_length=256, editable=False)
    channel =  models.CharField('喜好',blank=True, default='', max_length=256)
    user_img = models.CharField(blank=True, max_length=64, verbose_name="用户头像图片" ,default="/static/login/image/user.png")
    nickname = models.CharField('昵称',blank=True, max_length=256)
    truename = models.CharField('真实姓名', blank=True, max_length=256)
    age = models.CharField('年龄', blank=True, max_length=256)
    company = models.CharField('公司/学校', blank=True, max_length=256)
    brief = models.CharField('个人简介',blank=True, max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
        
class Settings(models.Model):
    name = models.CharField(default=None, max_length=128, unique=True)
    channel =  models.CharField(blank=True, default='', max_length=256)
    def __str__(self):
        return self.name
        

class Lunbo(models.Model):
    lunbo_url = models.CharField('轮播地址',max_length=256,default='')
    img = models.CharField('轮播图片',max_length=256,default='')
    lunbo_title = models.CharField('轮播标题',max_length=256)
    
    def __str__(self):
        return self.lunbo_title
        
    class Meta:
        verbose_name = "轮播"
        verbose_name_plural = "轮播"    

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

    title = models.CharField('标题',max_length=256)
    link = models.CharField('链接',max_length=256,default='')
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "百度热点"
        verbose_name_plural = "百度热点"   
    
class Sina_Hotnews(models.Model):

    title = models.CharField('标题',max_length=256)
    link = models.CharField('链接',max_length=256,default='')
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "新浪热点"
        verbose_name_plural = "新浪热点"   

    
class Sogo_Hotnews(models.Model):

    title = models.CharField('标题',max_length=256)
    link = models.CharField('链接',max_length=256,default='')
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "搜狗热点"
        verbose_name_plural = "搜狗热点"   
    
    
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
    cate_name = models.CharField(blank=False, max_length=64, verbose_name='类别')

    def __str__(self):
        return self.cate_name
    class Meta:
        db_table = 'cate'
        verbose_name = "文章类别表"
        verbose_name_plural = "文章类别表"

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
        verbose_name_plural = "文章相似度表"
        verbose_name = "文章相似度表"

class usersim(models.Model):
    user_id_base = models.CharField(blank=False, max_length=64, verbose_name="User_base", unique=False)
    user_id_sim = models.CharField(blank=False, max_length=64, verbose_name="User_sim", unique=False)
    user_correlation = models.FloatField(verbose_name="用户相关度", blank=False)

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.user_id_base

    class Meta:
        db_table = 'usersim'
        verbose_name = "用户相似度表"
        verbose_name_plural = "用户相似度表"
        
# 新闻表
class new(models.Model):
    new_id = models.CharField(blank=False, max_length=64, verbose_name="文章ID", unique=True)
    new_cate = models.ForeignKey(cate, related_name="类别", on_delete=False)
    new_time = models.DateTimeField(blank=True, verbose_name="发表时间")
    comment = models.IntegerField(verbose_name="评论次数", default='')  # True表示可不填
    likes = models.IntegerField(verbose_name="喜欢次数", default='')  # True表示可不填
    # related_name定义主表对象查询子表时使用的方法名称
    new_title = models.CharField(blank=False, max_length=100, verbose_name="标题")
    new_content = models.TextField(blank=False, verbose_name="文章简述")
    author = models.CharField(default='', max_length=100, verbose_name="作者")
    authorlink = models.CharField('作者链接',max_length=256,default='')
    url = models.CharField('文章链接',max_length=256,default='')
    piclink = models.CharField('图片链接',max_length=256,default='')
    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_title

    class Meta:
        db_table = 'new'
        verbose_name = "文章信息表"
        verbose_name_plural = "文章信息表"

# 新闻热度表
class newhot(models.Model):
    new_id = models.CharField(blank=False, max_length=64, verbose_name="文章ID", unique=True)
    new_cate = models.ForeignKey(cate, related_name="类别名", on_delete=False)
    new_hot = models.FloatField(verbose_name="热度值", blank=False)

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_id

    class Meta:
        db_table = 'newhot'
        verbose_name = "文章热度表"
        verbose_name_plural = "文章热度表"


# 新闻标签对应表
class newtag(models.Model):
    new_tag = models.CharField(blank=False, max_length=64, verbose_name="标签", unique=False)
    new_id = models.CharField(blank=False, max_length=64, verbose_name="文章ID", unique=False)
    new_hot = models.FloatField(verbose_name="热度值", blank=False)

    # python 2.7中使用的是__unicode__
    def __str__(self):
        return self.new_tag

    class Meta:
        db_table = 'newtag'
        verbose_name = "文章标签表"
        verbose_name_plural = "文章标签表"

class Answers(models.Model):
    answer_id = models.CharField(blank=False, max_length=64, verbose_name='帮助问题ID',unique=True)
    answer_name = models.CharField(blank=False, max_length=64, verbose_name='帮助标题')
    detail = models.CharField(blank=True, max_length=256, verbose_name="解答内容")

    def __str__(self):
        return self.answer_id
    class Meta:
        db_table = 'answer'
        verbose_name = "帮助问题表"  
        verbose_name_plural = "帮助问题表"    

class Word_cloud(models.Model):
    user_name = models.CharField(blank=False, max_length=64, verbose_name="用户名", unique=False)
    cloud_time = models.DateField(blank=False, verbose_name="词云记录时间")
    cloud_img = models.CharField(blank=False, max_length=64, verbose_name="词云图片")
    cloud_dict = models.CharField(blank=True, max_length=256, verbose_name="词云字典")
    change_time = models.DateTimeField(blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.user_name
    class Meta:
        verbose_name = "词云表"
        verbose_name_plural = "词云表" 
    
class user_info(models.Model):
    user_name = models.CharField(blank=False, max_length=64, verbose_name="用户名", unique=True)
    last_log_time = models.DateField(blank=False, verbose_name="最近登录时间")
    active = models.IntegerField(verbose_name="活跃", blank=False)
    read = models.IntegerField(verbose_name="阅读", blank=False)
    cloud_dict = models.CharField(blank=True, max_length=256, verbose_name="词云字典", default=" ")

    def __str__(self):
        return self.user_name
    class Meta:
        verbose_name = "用户登录信息"
        verbose_name_plural = "用户登录信息" 

class helpform(models.Model):
    contact = models.CharField(blank=False, max_length=64, verbose_name="联系方式", unique=False)
    content = models.CharField(blank=False, max_length=256, verbose_name="反馈内容", unique=False)
    def __str__(self):
        return self.contact
    class Meta:
        verbose_name = "用户反馈表"
        verbose_name_plural = "用户反馈表" 
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