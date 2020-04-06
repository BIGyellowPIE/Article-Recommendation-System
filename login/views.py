from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from . import models
from . import forms
import time
import hashlib
# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def record(request):
    if request.method == "GET":
        newid = request.GET.get('newid')
        if request.session.get('is_login', None):
            newone = models.new.objects.filter(new_id=newid)[0]
            # 将用户的点击新闻信息写入数据库
            uname = request.session['user_name']
            newbtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            models.newbrowse.objects.create(user_name=uname,new_id=newid,new_browse_time=newbtime).save()            
            return HttpResponse(newid)
        else:
            return HttpResponse(newid)

def index(request):
    _cate = request.GET.get("cateid","1")
    total = 0
    _page_id = 1
    if _cate == "1":
        news,news_hot_value = getHotNews()
    # 如果cate 是热度榜，走该部分逻辑
    elif _cate == "2":
        news, news_hot_value = getRecNews(request)
    # 其他正常的请求获取
    else:
        news = models.new.objects.filter(new_cate=_cate).order_by("-new_time")
        total = news.__len__()
        news = news[_page_id * 10:(_page_id+1) * 10]
    result = dict()
    result["code"] = 2
    result["total"] = total
    result["cate_id"] = _cate
    result["news"] = list()
    for one in news:
        result["news"].append({
            "new_id":one.new_id,
            "new_title":str(one.new_title),
            "new_time": one.new_time,
            "new_cate": one.new_cate.cate_name,
            "new_hot_value": news_hot_value[one.new_id] if _cate == "2" or _cate == "1" else 0 ,
            "new_content": str(one.new_content[:100])
        })        
        
        
    hotnews_list = models.Hotnews.objects.all()[:10]
    bdhotnews_list = models.Baidu_Hotnews.objects.all()[:10]
    sghotnews_list = models.Sogo_Hotnews.objects.all()[:10]
    wbhotnews_list = models.Sina_Hotnews.objects.all()[:10]
    articles_list = models.Articles.objects.all()[:20]
    return render(request, 'login/index.html',{"bdhotnews_list":bdhotnews_list,"sghotnews_list":sghotnews_list,"wbhotnews_list":wbhotnews_list,"articles_list":articles_list,"news":result["news"]})



def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
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
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
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
                return redirect('/prefer/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def prefer(request):
    if request.method == "POST":
        check_box_list = request.POST.getlist('check_box_list')
        pre_str=''.join(check_box_list)
        if pre_str.isspace() or len(pre_str)==0:
            pre_str = '123456'
        user_set = models.Settings.objects.get(name=request.session['user_name'])
        user_set.forum = pre_str
        user_set.save()
        return redirect('/channel/')
    return render(request, 'login/prefer.html')
    
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
    all_news = models.newhot.objects.order_by("-new_hot").values("new_id","new_hot")[:20]
    all_news_id = [one["new_id"] for one in all_news]
    all_news_hot_value = { one["new_id"]:one["new_hot"] for one in all_news}
    # 返回 热度榜单数据
    return models.new.objects.filter(new_id__in=all_news_id),all_news_hot_value

# 为你推荐的数据获取逻辑
def getRecNews(request):
    if request.session.get('is_login', None):
        user_set = models.Settings.objects.get(name=request.session['user_name'])
        tags = user_set.channel
        tag_flag = 0 if tags == "" else 1
        tags_list= tags.split(",")
        uname = request.session["user_name"]
        # 走标签召回逻辑
        if tag_flag == 1:
            # 首先判断用户是否有浏览记录
            # 如果有该用户的浏览记录 则从浏览的新闻获取相似的新闻返回
            if models.newbrowse.objects.filter(user_name=uname).exists():
                # 判断用户最近浏览的新闻是否够7个，如果够的话 取 top 7，每个取两个相似
                # 如果不够7个 每个取 14/真实个数 +1 相似
                num = 0
                browse_dict = models.newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id")[:7]
                if browse_dict.__len__() < 7:
                    num = ( 14 / browse_dict.__len__())
                else:
                    num = 2
                news_id_list = list()
                all_news_hot_value = dict()
                # 遍历最近浏览的N篇新闻，每篇新闻取num篇相似新闻
                for browse_one in browse_dict:
                    for one in models.newsim.objects.filter(new_id_base=browse_one["new_id"]).order_by("-new_correlation")[:num]:
                        news_id_list.append(one.new_id_sim)
                        all_news_hot_value[one.new_id_sim] = (models.newhot.objects.filter(new_id=browse_one["new_id"])[0]).new_hot
                num = (20 / len(tags_list)) + 1
                news_id_hot_dict = dict()
                for tag in tags_list:
                    result = models.newtag.objects.filter(new_tag=tag).values("new_id","new_hot")[:num]
                    for one in result:
                        news_id_list.append(one["new_id"])
                        all_news_hot_value[one["new_id"]] = one["new_hot"]                        
                
                return models.new.objects.filter(new_id__in=news_id_list)[:20], all_news_hot_value
            else:
                num = (20 / len(tags_list)) + 1
                news_id_list = list()
                news_id_hot_dict = dict()
                for tag in tags_list:
                    result = models.newtag.objects.filter(new_tag=tag).values("new_id","new_hot")[:num]
                    for one in result:
                        news_id_list.append(one["new_id"])
                        news_id_hot_dict[one["new_id"]] = one["new_hot"]
                return models.new.objects.filter(new_id__in=news_id_list)[:20], news_id_hot_dict
        # 走正常排序逻辑
        else:
            # 首先判断用户是否有浏览记录
            # 如果有该用户的浏览记录 则从浏览的新闻获取相似的新闻返回
            if models.newbrowse.objects.filter(user_name=uname).exists():
                # 判断用户最近浏览的新闻是否够10个，如果够的话 取 top 10，每个取两个相似
                # 如果不够10个 每个取 20/真实个数 +1 相似
                num = 0
                browse_dict = models.newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id")[:10]
                if browse_dict.__len__() < 10:
                    num = ( 20 / browse_dict.__len__()) +1
                else:
                    num = 2
                news_id_list = list()
                all_news_hot_value = dict()
                # 遍历最近浏览的N篇新闻，每篇新闻取num篇相似新闻
                for browse_one in browse_dict:
                    for one in models.newsim.objects.filter(new_id_base=browse_one["new_id"]).order_by("-new_correlation")[:num]:
                        news_id_list.append(one.new_id_sim)
                        all_news_hot_value[one.new_id_sim] = (models.newhot.objects.filter(new_id=browse_one["new_id"])[0]).new_hot
                return models.new.objects.filter(new_id__in=news_id_list)[:20], all_news_hot_value
            # 如果该用户没有浏览记录，即该用户是第一次进入系统且没有选择任何标签 返回热度榜单数据的20-40
            else:
                # 从新闻热度表中取top20 新闻数据
                all_news = models.newhot.objects.order_by("-new_hot").values("new_id", "new_hot")[20:40]
                all_news_id = [one["new_id"] for one in all_news]
                all_news_hot_value = {one["new_id"]: one["new_hot"] for one in all_news}
                # 返回 热度榜单数据
                return models.new.objects.filter(new_id__in=all_news_id), all_news_hot_value 
    else:
        all_news = models.newhot.objects.order_by("-new_hot").values("new_id", "new_hot")[20:40]
        all_news_id = [one["new_id"] for one in all_news]
        all_news_hot_value = {one["new_id"]: one["new_hot"] for one in all_news}
        # 返回 热度榜单数据
        return models.new.objects.filter(new_id__in=all_news_id), all_news_hot_value 
    
def faqs(request):
    return render(request, 'login/faqs.html')
    
def help(request):
    return render(request, 'login/help.html')
