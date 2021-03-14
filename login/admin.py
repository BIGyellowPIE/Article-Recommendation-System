from django.contrib import admin


from . import models

class newAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.new, newAdmin)

admin.site.register([models.User,models.user_info,models.usersim])
admin.site.register([models.cate,models.newtag,models.newsim,models.newhot])
admin.site.register([models.Lunbo,models.Baidu_Hotnews,models.Sina_Hotnews,models.Sogo_Hotnews])
admin.site.register([models.Word_cloud,models.helpform,models.Answers])