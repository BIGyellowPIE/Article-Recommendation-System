from django.contrib import admin


from . import models

admin.site.site_header = '看荐管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'



admin.site.register([models.User,models.user_info,models.usersim])
admin.site.register([models.new,models.cate,models.newtag,models.newsim,models.newhot])
admin.site.register([models.Lunbo,models.Baidu_Hotnews,models.Sina_Hotnews,models.Sogo_Hotnews])
admin.site.register([models.Word_cloud,models.helpform,models.Answers])
