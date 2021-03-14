from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from . import models
from . import forms
from random import shuffle
import time
import random
import hashlib
from django.core.paginator import Paginator,InvalidPage,EmptyPage 
import json
import re
import xlsxwriter
import os
import numpy as np
from PIL import Image
import ast
from wordcloud import WordCloud
from django.utils import timezone
from datetime import timedelta
# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def record(request):
    if request.method == "GET":
        newid = request.GET.get('newid')
        uname = request.session['user_name']
        if request.session.get('is_login', None):
            newone = models.newbrowse.objects.filter(new_id=newid,user_name=uname)[:1]
            # 将用户的点击新闻信息写入数据库
            if newone.__len__() < 1:
                user_info = models.user_info.objects.filter(user_name=uname)
                newbtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                if user_info.__len__() < 1:
                    models.user_info.objects.create(user_name=uname,last_log_time=now_time,active=1,read=1).save()
                else:
                    user_info[0].read += 1
                    last_time = str(user_info[0].last_log_time)
                    if now_time != last_time:
                        user_info[0].last_log_time = now_time
                        user_info[0].active += 1
                    user_info[0].save()
                models.newbrowse.objects.create(user_name=uname,new_id=newid,new_browse_time=newbtime).save()
            else:
                newone[0].new_browse_time=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                newone[0].save() 
            return HttpResponse(newid)
        else:
            return HttpResponse(newid)

def index(request):
    cate = request.GET.get("cateid","1")
    total = 0
    _page_id = request.GET.get("_page_id","0")
    if cate == "1":
        news,news_hot_value = getHotNews()
        news = news[:20]
    # 如果cate 是热度榜，走该部分逻辑
    elif cate == "2":
        news = getRecNews(request)
    # 其他正常的请求获取
    else:
        news = models.new.objects.filter(new_cate=cate).order_by("-new_time")[:200]
        news = list(news)
        shuffle(news)
        total = news.__len__()
        news = news[_page_id * 10:(_page_id+1) * 10]
    result = dict()
    result["code"] = 2
    result["total"] = total
    result["cate_id"] = cate
    result["news"] = list()
    for one in news:
        result["news"].append({
            "new_id":one.new_id,
            "new_title":str(one.new_title),
            "new_time": one.new_time,
            "author": one.author,
            "authorlink": one.authorlink,
            "url": one.url,
            "piclink": one.piclink,    
            "new_content": str(one.new_content[:100])+".."
        })        
       
    lunbos = models.Lunbo.objects.all()[:10]
    lunbo_list = list()
    l_range = range(0,lunbos.__len__())
    l_list = random.sample(l_range,4)
    for i in l_list:
        lunbo_list.append(lunbos[i])
  
    shuffle(result["news"])  
    bdhotnews_list = models.Baidu_Hotnews.objects.all()[:10]
    sghotnews_list = models.Sogo_Hotnews.objects.all()[:10]
    wbhotnews_list = models.Sina_Hotnews.objects.all()[:10]
    return render(request, 'login/index.html',{"bdhotnews_list":bdhotnews_list,"sghotnews_list":sghotnews_list,"wbhotnews_list":wbhotnews_list,"lunbo_list":lunbo_list,"news":result["news"]})


def changetab(request):
    cate = request.GET.get("cateid","1")
    total = 0
    posts_list = list()
    if cate == "1":
        news_list,news_hot_value = getHotNews()
    # 如果cate 是热度榜，走该部分逻辑
    elif cate == "2":
        news_list = getRecNews(request)
    # 其他正常的请求获取
    else:
        news_list = models.new.objects.filter(new_cate=cate).order_by("-new_time")[:200]
    for one in news_list:
        posts_list.append({
            "new_id":one.new_id,
            "new_title":str(one.new_title),
            "new_time": one.new_time,
            "author": one.author,
            "authorlink": one.authorlink,
            "url": one.url,
            "piclink": one.piclink,  
            "new_content": str(one.new_content[:100])+".."
        }) 
    shuffle(posts_list) 
    paginator = Paginator(posts_list,20)
    page = int(request.GET.get('page','1')) 
    posts = paginator.page(page)          
    template = 'text_container.html'    
    return render(request, template,locals())

def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        message1 = ""
        message2 = ""
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message1 = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message2 = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())



    
def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        message1 = ""
        message2 = ""
        message3 = ""
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            if password1 != password2:
                message2 = '两次输入的密码不同'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message1 = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message3 = '该邮箱已经被注册'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.nickname = username
                new_user.save()
                user_setting = models.Settings()
                user_setting.name = username
                
                user_setting.save()
                try:
                    user = models.User.objects.get(name=username)
                except :
                    message = '注册失败！'                
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/channel/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())
    
def channel(request):
    if request.method == "POST":
        check_box_list = request.POST.getlist('check_box_list')
        channel_str=','.join(check_box_list)
        if channel_str.isspace() or len(channel_str)==0:
            channel_str = ''
        user_set = models.Settings.objects.get(name=request.session['user_name'])
        user_set.channel=channel_str
        user_set.save()    
        return redirect('/index/')
    return render(request, 'login/channel.html')

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/index/")
    
def getHotNews():
    # 从新闻热度表中取top 20新闻数据
    all_news = models.newhot.objects.order_by("-new_hot").values("new_id","new_hot")[:400]
    all_news_id = [one["new_id"] for one in all_news]
    all_news_hot_value = { one["new_id"]:one["new_hot"] for one in all_news}
    # 返回 热度榜单数据
    newlist = models.new.objects.filter(new_id__in=all_news_id)
    newlist = list(newlist)
    shuffle(newlist)
    return newlist,all_news_hot_value

# 为你推荐的数据获取逻辑
def getRecNews(request):
    if request.session.get('is_login', None):
        user_set = models.Settings.objects.get(name=request.session['user_name'])
        tags = user_set.channel
        tag_flag = 0 if tags == "" else 1
        tags_list= tags.split(",")
        uname = request.session["user_name"]
        simuser = models.usersim.objects.filter(user_id_base=uname).order_by("-user_correlation")[:20]
        if simuser.__len__() > 1:
            user_id_list = list()
            for one in simuser:
                user_id_list.append(one.user_id_sim)
            news_list = list()
            for one in user_id_list:
                browse_dict = models.newbrowse.objects.filter(user_name=one).order_by("-new_browse_time").values("new_id")[:10]
                if browse_dict.__len__() > 1:
                    for art in browse_dict:
                        news_list.append(art["new_id"])
            newlist = models.new.objects.filter(new_id__in=news_list)
            newlist = list(newlist)
            shuffle(newlist)
            return newlist[:100]
        # 走标签召回逻辑
        if tag_flag == 1:
            # 首先判断用户是否有浏览记录
            # 如果有该用户的浏览记录 则从浏览的新闻获取相似的新闻返回
            if models.newbrowse.objects.filter(user_name=uname).exists():
                # 判断用户最近浏览的新闻是否够20个，如果够的话 取 top 20，每个取三个相似
                # 如果不够20个 每个取 60/真实个数 +1 相似
                num = 0
                browse_dict = models.newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id")[:7]
                if browse_dict.__len__() < 10:
                    num = 6
                elif browse_dict.__len__() < 20:
                    num = ( 60 / browse_dict.__len__())
                else:
                    num = 3
                news_id_list = list()
                all_news_hot_value = dict()
                # 遍历最近浏览的N篇新闻，每篇新闻取num篇相似新闻
                for browse_one in browse_dict:
                    for one in models.newsim.objects.filter(new_id_base=browse_one["new_id"]).order_by("-new_correlation")[:num]:
                        news_id_list.append(one.new_id_sim)
                        all_news_hot_value[one.new_id_sim] = (models.newhot.objects.filter(new_id=browse_one["new_id"])[0]).new_hot
                num = (40 / len(tags_list)) + 1
                news_id_hot_dict = dict()
                for tag in tags_list:
                    result = models.newtag.objects.filter(new_tag=tag).values("new_id","new_hot")[:num]
                    for one in result:
                        news_id_list.append(one["new_id"])
                        all_news_hot_value[one["new_id"]] = one["new_hot"]                        
                newlist = models.new.objects.filter(new_id__in=news_id_list)
                newlist = list(newlist)
                shuffle(newlist)
                return newlist[:100]
            else:
                num = (100 / len(tags_list)) + 1
                news_id_list = list()
                news_id_hot_dict = dict()
                for tag in tags_list:
                    result = models.newtag.objects.filter(new_tag=tag).values("new_id","new_hot")[:num]
                    for one in result:
                        news_id_list.append(one["new_id"])
                        news_id_hot_dict[one["new_id"]] = one["new_hot"]
                newlist = models.new.objects.filter(new_id__in=news_id_list)
                newlist = list(newlist)
                shuffle(newlist)
                return newlist[:100]
        # 走正常排序逻辑
        else:
            # 首先判断用户是否有浏览记录
            # 如果有该用户的浏览记录 则从浏览的新闻获取相似的新闻返回
            if models.newbrowse.objects.filter(user_name=uname).exists():
                # 判断用户最近浏览的新闻是否够10个，如果够的话 取 top 10，每个取两个相似
                # 如果不够10个 每个取 20/真实个数 +1 相似
                num = 0
                browse_dict = models.newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id")[:10]
                if browse_dict.__len__() < 20:
                    num = ( 100 / browse_dict.__len__())
                else:
                    num = 5
                news_id_list = list()
                all_news_hot_value = dict()
                # 遍历最近浏览的N篇新闻，每篇新闻取num篇相似新闻
                for browse_one in browse_dict:
                    for one in models.newsim.objects.filter(new_id_base=browse_one["new_id"]).order_by("-new_correlation")[:num]:
                        news_id_list.append(one.new_id_sim)
                        all_news_hot_value[one.new_id_sim] = (models.newhot.objects.filter(new_id=browse_one["new_id"])[0]).new_hot
                newlist = models.new.objects.filter(new_id__in=news_id_list)
                newlist = list(newlist)
                shuffle(newlist)
                return newlist[:100]
            # 如果该用户没有浏览记录，即该用户是第一次进入系统且没有选择任何标签 返回热度榜单数据的20-40
            else:
                # 从新闻热度表中取top100 新闻数据
                all_news = models.newhot.objects.order_by("-new_hot").values("new_id", "new_hot")[:100]
                all_news_id = [one["new_id"] for one in all_news]
                all_news_hot_value = {one["new_id"]: one["new_hot"] for one in all_news}
                # 返回 热度榜单数据
                return models.new.objects.filter(new_id__in=all_news_id)
    else:
        all_news = models.newhot.objects.order_by("-new_hot").values("new_id", "new_hot")[:100]
        all_news_id = [one["new_id"] for one in all_news]
        all_news_hot_value = {one["new_id"]: one["new_hot"] for one in all_news}
        # 返回 热度榜单数据
        return models.new.objects.filter(new_id__in=all_news_id)
      
def home(request):
    if request.session.get('is_login', None):
        uname = request.session["user_name"]
        browse_dict = models.newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id","new_browse_time").distinct()[:20]
        user_info = models.user_info.objects.filter(user_name=uname)
        user = models.User.objects.get(name=uname)
        now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if user_info.__len__() < 1:
            models.user_info.objects.create(user_name=uname,last_log_time=now_time,active=1,read=0)
        else:
            now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            last_time = str(user_info[0].last_log_time)
            user_info = user_info.first()
            if now_time != last_time:
                user_info.last_log_time = now_time
                user_info.active += 1
            user_info.save()    
        
        news = list()
        user_info = models.user_info.objects.filter(user_name=uname)
        for one in browse_dict:
            a_new = models.new.objects.filter(new_id=one["new_id"])[0]
            news.append({
                "new_id":one["new_id"],
                "new_title":str(a_new.new_title),
                "new_time": one["new_browse_time"],
                "author": a_new.author,
                "authorlink": a_new.authorlink,
                "url": a_new.url,
                "piclink": a_new.piclink,  
                "new_content": str(a_new.new_content[:80])+".."
            })
        return render(request, 'login/home.html',{"news":news,"user_info":user_info[0],"nickname":user.nickname})
    else:
        return redirect('/index/')

   
def wordcloud(request):
    if request.session.get('is_login', None):
        template = 'cloud_container.html'
        read_num = request.POST.get('read_num')
        #   词云模式判断，1为查看，2为用户修改，先1
        uname = request.session['user_name']
        user_info = models.user_info.objects.get(user_name=uname)
        user_set = models.Settings.objects.get(name=uname)
        now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        now = timezone.now()
        word_cloud = models.Word_cloud.objects.filter(user_name=uname).order_by("-cloud_time")
        tags = user_set.channel
        tag_flag = 0 if tags == "" else 1
        tags_list= tags.split(",")
            
        if word_cloud.__len__() < 1: #如果没有词云
            #先不做判断浏览条数
            #取出最近浏览的所有新闻，构建count_dict，可以设置默认，根据每个新闻的tag，对应相加
            #取出用户设置的初始喜欢关键词，每个+5
            #构建dict，产生词云，并将词云url和dict返回，将dict内容保存，保存词云记录时间，路径
            if int(read_num) < 1:
                return render(request, template,{"error_img":"/static/login/image/error_img.png"})
            browse_dict = models.newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id","new_browse_time").distinct()
            word = ["财经","彩票","房产","股票","军事","政治","计算机","科技","社会","家居","星座","时尚","体育","娱乐","游戏","教育","历史","文化","艺术"]
            word_list=list(set(word))
            value_list=[0 for name in word_list]
            count_dict=dict(zip(word_list,value_list))
            for news in browse_dict:
                tag_list = models.newtag.objects.filter(new_id=news["new_id"]).values("new_tag")
                for one in tag_list:
                    count_dict[one["new_tag"]] += 1
                    
            if tag_flag == 1:
                for tag in tags_list:
                    count_dict[tag] += 5
            result_dict = count_dict.copy()
            for one in list(result_dict.keys()):
                if result_dict[one] == 0:
                    del result_dict[one]
            title = uname + " " + now_time
            shape = "login/static/login/image/heart.png"
            savepath = "login/static/login/cloudimg"
            fullpath = "/static/login/cloudimg/" + title + ".png"
            dict_sql = str(json.dumps(count_dict, ensure_ascii=False))
            drawWordCloud(result_dict, title, shape, savepath)
            models.Word_cloud.objects.create(user_name=uname,cloud_time=now_time,cloud_img=fullpath,cloud_dict=dict_sql,change_time=now).save()
            user_info.cloud_dict=dict_sql
            user_info.save()
            return render(request, template,{"dicts":count_dict,"cloud_img":fullpath})
        else:
            #有词云，看今天日期和保存词云时间是否相等，相等则再看这段时间有没有浏览，没有则返回最近词云的url和dict，有则更新
            #不相等，则看昨天记录时间到今天有无浏览，没有浏览，使用昨天词云url和dict，复制一份返回
            #有浏览，则昨天dict内容每个*0.7，加上这段时间浏览文章的tag，构建dict和url进行返回
            last_time = str(word_cloud[0].cloud_time)
            if now_time != last_time:
                start = word_cloud[0].change_time
                today_news = models.newbrowse.objects.filter(new_browse_time__gt=start,user_name=uname).values("new_id","new_browse_time").distinct()        
                if today_news.__len__() < 1:
                    models.Word_cloud.objects.create(user_name=uname,cloud_time=now_time,cloud_img=word_cloud[0].cloud_img,cloud_dict=word_cloud[0].cloud_dict,change_time=now).save()
                    count_dict = ast.literal_eval(word_cloud[0].cloud_dict)
                    for sub in count_dict:
                       count_dict[sub] = int(count_dict[sub])
                    return render(request, template,{"dicts":count_dict,"cloud_img":word_cloud[0].cloud_img})
                else:
                    count_dict = ast.literal_eval(word_cloud[0].cloud_dict)
                    for sub in count_dict:
                       count_dict[sub] = int(int(count_dict[sub])*0.7)
                    for news in today_news:
                        tag_list = models.newtag.objects.filter(new_id=news["new_id"]).values("new_tag")
                        for one in tag_list:
                            count_dict[one["new_tag"]] += 1
                            
                    result_dict = count_dict.copy()
                    for one in list(result_dict.keys()):
                        if result_dict[one] == 0:
                            del result_dict[one]
                    title = uname + " " + now_time
                    shape = "login/static/login/image/heart.png"
                    savepath = "login/static/login/cloudimg"
                    fullpath = "/static/login/cloudimg/" + title + ".png"
                    dict_sql = str(json.dumps(count_dict, ensure_ascii=False))
                    drawWordCloud(result_dict, title, shape, savepath)
                    models.Word_cloud.objects.create(user_name=uname,cloud_time=now_time,cloud_img=fullpath,cloud_dict=dict_sql,change_time=now).save()
                    user_info.cloud_dict=dict_sql
                    user_info.save()
                    return render(request, template,{"dicts":count_dict,"cloud_img":fullpath})                    
            else:
                start = word_cloud[0].change_time
                today_news = models.newbrowse.objects.filter(new_browse_time__gt=start,user_name=uname).values("new_id","new_browse_time").distinct()             
                if today_news.__len__() < 1:
                    count_dict = ast.literal_eval(word_cloud[0].cloud_dict)
                    for sub in count_dict:
                       count_dict[sub] = int(count_dict[sub])
                    return render(request, template,{"dicts":count_dict,"cloud_img":word_cloud[0].cloud_img})
                else:   
                    count_dict = ast.literal_eval(word_cloud[0].cloud_dict)
                    for sub in count_dict:
                       count_dict[sub] = int(count_dict[sub])
                    for news in today_news:
                        tag_list = models.newtag.objects.filter(new_id=news["new_id"]).values("new_tag")
                        for one in tag_list:
                            count_dict[one["new_tag"]] += 1
                            
                    result_dict = count_dict.copy()
                    for one in list(result_dict.keys()):
                        if result_dict[one] == 0:
                            del result_dict[one]
                    title = uname + " " + now_time
                    shape = "login/static/login/image/heart.png"
                    savepath = "login/static/login/cloudimg"
                    fullpath = "/static/login/cloudimg/" + title + ".png"
                    dict_sql = str(json.dumps(count_dict, ensure_ascii=False))
                    drawWordCloud(result_dict, title, shape, savepath)
                    new_cloud = word_cloud.first()
                    new_cloud.cloud_img=fullpath
                    new_cloud.cloud_dict=dict_sql
                    new_cloud.change_time=now
                    new_cloud.save()
                    user_info.cloud_dict=dict_sql
                    user_info.save()
                    return render(request, template,{"dicts":count_dict,"cloud_img":fullpath})   
    else:
        return render(request, 'login/index.html')

def changeCloud(request):
    if request.method == "POST":
        num_origin = request.POST.get('num_list')
        shape_type = request.POST.get('shape_type',"1")         
        cloud_mode = request.POST.get('cloudMode',"1")
        num_list= num_origin.split(",")     
        now = timezone.now()
        uname = request.session['user_name']
        word_cloud = models.Word_cloud.objects.filter(user_name=uname).order_by("-cloud_time").first()
        raw_dict = ast.literal_eval(word_cloud.cloud_dict)
        word_list=[i for i in raw_dict.keys()]
        for sub in num_list:
           sub = int(sub)        
        count_dict=dict(zip(word_list,num_list))
        for sub in count_dict:
           count_dict[sub] = int(count_dict[sub])  
        result_dict = count_dict.copy()
        for one in list(result_dict.keys()):
            if result_dict[one] == 0:
                del result_dict[one]
        shape_dict = {"1":"rectangle","2":"star","3":"circle","4":"triangle"}
        title = "temp"
        shape = "login/static/login/image/"+ str(shape_dict[shape_type]) +".png"
        savepath = "login/static/login/cloudimg"
        if cloud_mode == "2":
            now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            title = uname + " " + now_time
            dict_sql = str(json.dumps(count_dict, ensure_ascii=False))  
            word_cloud.cloud_dict = dict_sql
            user_info = models.user_info.objects.get(user_name=uname)
            user_info.cloud_dict=dict_sql
            user_info.save()
            word_cloud.cloud_img = "/static/login/cloudimg/"+title+".png"
            word_cloud.change_time = now
            word_cloud.save()
        drawWordCloud(result_dict, title, shape, savepath)
        fullpath = "/static/login/cloudimg/"+title+".png"+"?"+str(random.random())
        template = 'cloud_container.html'
        return render(request, template,{"dicts":count_dict,"cloud_img":fullpath})

def recoverCloud(request):
    if request.method == "POST":
        uname = request.session['user_name']
        word_cloud = models.Word_cloud.objects.filter(user_name=uname).order_by("-cloud_time") 
        raw_dict = ast.literal_eval(word_cloud[0].cloud_dict)
        for sub in raw_dict:
           raw_dict[sub] = int(raw_dict[sub])
        template = 'cloud_container.html'
        return render(request, template,{"dicts":raw_dict,"cloud_img":word_cloud[0].cloud_img+"?"+str(random.random())})    

def drawWordCloud(words, title, shape, savepath):
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    img_array = np.array(Image.open(shape))
    wc = WordCloud(font_path="login/static/login/image/simkai.ttf", background_color='white', mask=img_array, max_words=2000, width=1920, height=1080, margin=5)
    wc.generate_from_frequencies(words)
    wc.to_file(os.path.join(savepath, title+'.png'))

def viewcloud(request):
    if request.method == "POST":
        uname = request.session['user_name']
        cloudTime = request.POST.get('cloudtime')
        template = 'cloud_img.html'
        word_cloud = models.Word_cloud.objects.filter(user_name=uname,cloud_time=cloudTime)
        if word_cloud.__len__() < 1:
            pic_url = "/static/login/image/no_cloud.png"
            return render(request, template,{"cloud_img":pic_url})
        else:    
            return render(request, template,{"cloud_img":word_cloud[0].cloud_img+"?"+str(random.random())}) 


def setbase(request):
    if request.method == 'POST':   
        user_name = request.POST.get('user_name')
        user = models.User.objects.get(name=user_name)
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')

        f = request.FILES.get('pic')
        if f is not None:
            # 文件保存路径
            fname = 'login/static/login/avatar/%s.jpg' % (user_name)
            with open(fname, 'wb') as pic:
                for c in f.chunks():
                    pic.write(c)
            user.user_img = "/static/login/avatar/%s.jpg" % (user_name)
        if user.nickname is not None:
            user.nickname = nickname
        if user.email is not None:    
            user.email = email
        user.save()
            
    return HttpResponse('保存成功！')

def helpform(request):
    if request.method == 'POST': 
        contact = request.POST.get('contact')
        content = request.POST.get('content')
        models.helpform.objects.create(contact=contact,content=content)
        return HttpResponse('反馈成功！')
    
def setdetail(request):
    if request.method == 'POST':   
        user_name = request.POST.get('user_name')
        user = models.User.objects.get(name=user_name)
        truename = request.POST.get('truename')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        company = request.POST.get('company')
        brief = request.POST.get('brief')
        user.truename = truename
        user.sex = sex
        user.age = age
        user.company = company
        user.brief = brief
        
        user.save()
            
    return HttpResponse('保存成功！')
    
def setkey(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user = models.User.objects.get(name=user_name)
        oldkey = request.POST.get('oldkey')
        newkey0 = request.POST.get('newkey0')
        newkey1 = request.POST.get('newkey1')
        if user.password == hash_code(oldkey):
            if newkey0 == newkey1:
                user.password = hash_code(newkey0)
                user.save()
                return HttpResponse('密码修改成功！') 
            else:
                return HttpResponse('两次输入的密码不同！') 
        else:
            return HttpResponse('密码不正确！') 
            
def delete(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        models.User.objects.filter(name=user_name).delete()
        models.Settings.objects.filter(name=user_name).delete()
        models.Word_cloud.objects.filter(user_name=user_name).delete()
        models.newbrowse.objects.filter(user_name=user_name).delete()
        models.user_info.objects.filter(user_name=user_name).delete()
        request.session.flush()
        return HttpResponse('账号注销成功！')
    
 
def faqs(request):
    return render(request, 'login/faqs.html')

def answers(request):
    answer_id = request.GET.get("answer_id")
    answer = models.Answers.objects.get(answer_id=answer_id)
    return render(request, 'login/answers.html',{"name":answer.answer_name,"content":answer.detail}) 


 
def settings(request):
    if request.session.get('is_login', None):
        user_info = models.User.objects.filter(name=request.session['user_name'])
        return render(request, 'login/settings.html',{"user_info":user_info[0]})
    else:
        return redirect('/index/')
    
def contact(request):
    return render(request, 'login/contact.html')
    
def help(request):
    return render(request, 'login/help.html')    


