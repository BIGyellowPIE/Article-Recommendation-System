## 运行说明
1.项目的Python版本为3.6，Django版本为2.2.1

2.解压WebSite.rar后，进入WebSite/目录，使用pip install -r req.txt安装Python依赖包。

3.在WebSite目录下，执行python manage.py runserver 8000。

4.浏览器中输入http://127.0.0.1:8000/index/，即可在本地进行访问。

5.若需要在云服务器上运行项目（Centos7.3），使用Nginx与uswgi进行网站部署，那么uwsgi.ini已经设置好内容。在WebSite/tools文件夹下，还存放着文章热度值计算与用户相似度计算的py文件，可以使用crontab -e命令将对应py文件加入定时任务，实现离线计算。