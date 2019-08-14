# Version 1.0
# 基础镜像
FROM ubuntu:latest

# 维护者
MAINTAINER root@bertramc.cn

#换源
RUN rm -f /etc/apt/sources.list
COPY sources.list /etc/apt/
#安装基础组建
RUN apt -y update && apt install -y python3 && apt install -y nginx && apt install -y python3-pip && apt install -y git

#从git上clone下docs-manager这个项目
RUN cd /root/ && git clone https://gitee.com/berTrAM_chen/docs-manager.git

#安装python3依赖
RUN cd /root/docs-manager/backend && pip3 install -r r.txt

#修复mkdocs自带bug
RUN sed -i "111i \ \ \ \ \ \ \ \ config['site_url'] = ''" /usr/local/lib/python3.6/dist-packages/mkdocs/commands/serve.py

#修改nginx配置
RUN rm -f /etc/nginx/sites-enabled/default
COPY default /etc/nginx/sites-enabled/

#启动nginx服务
RUN service nginx start
RUN rm -f /root/docs-manager/start.sh
COPY start.sh /root/docs-manager/
RUN chmod +x /root/docs-manager/start.sh

#开放端口
EXPOSE 80
EXPOSE 8080

#守护容器
CMD ["/root/docs-manager/start.sh"]
