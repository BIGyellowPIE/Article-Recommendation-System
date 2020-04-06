# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
 
from Hotpoint.models import Test
 
# 数据库操作
def testdb(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")