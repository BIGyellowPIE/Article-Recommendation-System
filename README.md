# 基于Django的个性化文章推荐系统

#### 介绍
本作品在研究推荐系统相关理论知识的基础上，综合使用数据库、机器学习、爬虫、网页交互等技术，结合经典推荐算法，搭建基于网络热点的综合个性化推荐系统，旨在为用户提供及时精准的个性化网络信息服务。


#### 安装教程
1. 项目的Python版本为3.6，Django版本为2.2.1
2. 使用pip install -r req.txt安装Python依赖包。

#### 使用说明

1. 在WebSite目录下，执行python manage.py runserver 8000。
2. 修改WebSite/settings.py中的SECRET_KEY为您的Django项目使用的密钥。
3. 浏览器中输入http://127.0.0.1:8000/index/，即可在本地进行访问。
4. 若需要在云服务器上运行项目（Centos7.3），使用Nginx与uswgi进行网站部署，那么uwsgi.ini已经设置好内容。在WebSite/tools文件夹下，还存放着文章热度值计算与用户相似度计算的py文件，可以使用crontab -e命令将对应py文件加入定时任务，实现离线计算。

#### 贡献者

1. BIGyellowPIE
2. MR_PANGHU

#### 更多
由于项目的主体由本人完成，故后续更新不再提交，等有空了回来填坑。如有疑问可以联系我。
