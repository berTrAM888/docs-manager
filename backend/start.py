# -*- coding:utf-8 -*-
# Author:berTrAM

import sys
import os

import json
import hashlib
import yaml
import re
import string
import random
import zipfile
import urllib
from flask import Flask,render_template,g,url_for,request,jsonify,session,redirect,send_from_directory
from functools import wraps

template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

web = Flask(__name__,static_folder=static_folder,template_folder=template_folder)
web.config['SECRET_KEY'] = "no_one_can_gue5s_my_key"
website_path = os.path.abspath(os.path.dirname(os.getcwd()))
website_config_path = os.path.join(website_path,"mkdocs.yml")
website_doc_path = os.path.join(website_path,"docs/")

#########################
#    System Functions
#########################

#获取站点配置
def Website_config_get():
	f = open(website_config_path,'r',encoding='utf-8')
	config = f.read()
	f.close()
	config = yaml.load(config)
	return config

#修改站点配置
def Website_config_mod(config):
	prev_config = Website_config_get()
	f = open(website_config_path,'w+',encoding='utf-8')
	#print(prev_config)
	prev_config["site_name"] = config["site_name"]
	prev_config["site_description"] = config["site_description"]
	prev_config["site_author"] = config["site_author"]
	prev_config["site_url"] = config["site_url"]
	prev_config["copyright"] = config["copyright"]
	try:
		new_config = yaml.dump(prev_config)
		f.write(new_config)
		f.close()
		return True
	except:
		return False

#获取管理员配置信息
def Admin_init():
	configfile = open('config.inc','r')
	admin_configs = configfile.read()
	admin_configs = json.loads(admin_configs)
	configfile.close()
	return admin_configs

#查询单个管理员
def Admin_select(username):
	for admin in Admin_init():
		if admin["username"] == username:
			return admin
	return None

#修改管理员配置信息
def Admin_modify(admin_configs):
	configfile = open('config.inc','w+')
	admin_configs = json.dumps(admin_configs)
	try:
		configfile.write(admin_configs)
		configfile.close()
		return True
	except:
		return False

#修改管理员密码
def Admin_pwd_modify(prev_pwd,new_pwd,repeat_new_pwd):
	if new_pwd == repeat_new_pwd:
		if hashlib.md5(prev_pwd.encode('utf-8')).hexdigest() == g.current_user["password"]:
			admins = Admin_init()
			for admin in admins:
				if g.current_user["username"] == admin["username"]:
					admin["password"] = hashlib.md5(new_pwd.encode('utf-8')).hexdigest()
					if Admin_modify(admins):
						return jsonify(code=200,msg=u"密码修改成功")
					else:
						return jsonify(code=500,msg=u"密码修改失败")
		else:
			return jsonify(code=500,msg=u"请确认原密码是否正确")
	else:
		return jsonify(code=500,msg=u"请确认两次输入的密码一致")

#删除管理员
def Admin_delete(username):
	admins = Admin_init()
	i = 0
	for admin in admins:
		if username == admin["username"]:
			admins.pop(i)
			if Admin_modify(admins):
				return True
		i = i + 1
	return False

#创建管理员
def Admin_add(admin):
	admins = Admin_init()
	try:
		new_admin = {"username":admin["username"],"password":hashlib.md5(admin["password"].encode('utf-8')).hexdigest()}
		admins.append(new_admin)
		if Admin_modify(admins):
			return True
	except:
		return False

#登录判断
def Admin_verify(username,password):
	for admin in Admin_init():
		if admin["username"] == username:
			if admin["password"] == hashlib.md5(password.encode('utf-8')).hexdigest():
				session["username"]=admin["username"]
				return True
	return False

#创建随机字符串
def gen_random_string():
	return "".join(random.sample(string.ascii_letters + string.digits, 16))

'''
#获取所有页面
def Page_get():
	config = Website_config_get()
	pages_key=[]
	pages = config['nav']
	for p in pages:
		pages_key.append(list(p.keys())[0])
	return pages_key

#查询单个页面
def Page_select(page):
	pages = Page_get()
	page_key = 0
	for p in pages:
		if page == p:
			return True
		page_key = page_key + 1
	return False

#删除单个页面
def Page_delete(page):
	config = Website_config_get()
	pages = config['nav']
	i = 0
	for p in pages:
		#print(i)
		if list(p.keys())[0] == page:
			pages.pop(i)
			config['nav'] = pages
			f = open(website_config_path,'w+',encoding='utf-8')
			f.write(yaml.dump(config))
			f.close()
			return True
		i = i + 1
	return False

#创建页面
def Page_add(page):
	config = Website_config_get()
	pages = config['nav']
	file = gen_random_string()+".md"
	f = open(website_doc_path+file,'w+',encoding='utf-8')
	f.close()
	new_page = { page:[{"简介":file}]}
	pages.append(new_page)
	config['nav'] = pages
	try:
		f = open(website_config_path,'w+',encoding='utf-8')
		f.write(yaml.dump(config))
		f.close()
		return True
	except:
		return False
	return False

#获取所有子页面(包含与父页面关系)
def Childpage_get():
	config = Website_config_get()
	pages = config['nav']
	return pages

#删除子页面
def Childpage_delete(parent,child):
	config =Website_config_get()
	pages = config['nav']
	for page in pages:
		#print(page.keys())
		if list(page.keys())[0]==parent:
			i = 0
			for childs in page[parent]:
				if list(childs.keys())[0]==child:
					return True
	return True
'''

#获取页面配置
def All_page_get():
	content = yaml.dump(Website_config_get()['nav'])
	print(content)
	return content

#修改页面配置
def All_page_mod(content):
	config = Website_config_get()
	nav = yaml.load(content)
	config['nav'] = nav
	try:
		f = open(website_config_path,'w+',encoding='utf-8')
		f.write(yaml.dump(config))
		f.close()
		return True
	except:
		return False

#获取上线文章
def Article_online_get():
	config = All_page_get()
	pattern=r"[\u4e00-\u9fff\w\-\_]+.md"
	regex = re.compile(pattern,flags=re.M)
	articles = regex.findall(config.encode('utf-8').decode('unicode_escape'))
	return articles

#获取未上线文章
def Article_offline_get():
	all_files = os.listdir(website_doc_path)
	online_files = Article_online_get()
	return list(set(all_files)-set(online_files))

#删除所有下线文章
def Article_delete_all():
	offline_files = Article_offline_get()
	for offline_file in offline_files:
		if os.path.exists(website_doc_path+offline_file):
			os.remove(website_doc_path+offline_file)
		else:
			return False
	return True

def Article_delete_one(article_id):
	offline_files = Article_offline_get()
	offline_file = offline_files[int(article_id)]
	if os.path.exists(website_doc_path+offline_file):
		os.remove(website_doc_path+offline_file)
	else:
		return False
	return True

#保存markdown文件
def Save_markdown(filename,content):
	try:
		f = open(website_doc_path+filename,'w+')
		f.write(content)
		f.close()
		return True
	except:
		return False

#获取markdown文件RAW
def Get_markdown(filename):
	try:
		f = open(website_doc_path+filename+'.md','r')
		article = f.read()
		f.close()
		return article
	except:
		return False

#将markdown原始格式js多行化,并UNICODE化
def JS_markdown(content):
	return content.replace('\n','\\n\\\n')


#############################
#          内核函数
#############################
#登录检查
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("username")==None:
			return redirect(url_for('login_tpl'))
		return f(*args, **kwargs)
	return decorated_function



#设置全局变量g
@web.before_request
def before_request():
	if "username" in session:
		g.current_user = Admin_select(session["username"])
	else:
		g.current_user = None


##########################
#        Templates
##########################

#主页route
@web.route('/admin/',methods=['GET'])
@web.route('/admin/index.html',methods=['GET'])
@login_required
def index():
	return render_template('index.html',admin=g.current_user,config=Website_config_get(),admin_count=len(Admin_init()),article_count=len(Article_online_get()))

#登录页route
@web.route('/admin/login.html',methods=['GET'])
def login_tpl():
	return render_template('login.html',methods=['GET'])

#网站信息修改route
@web.route('/admin/manager.html',methods=['GET'])
@login_required
def manager_tpl():
	return render_template('manager.html',admin=g.current_user,config=Website_config_get())

#修改密码页面route
@web.route('/admin/changepwd.html',methods=['GET'])
@login_required
def changepwd_tpl():
	return render_template('changepwd.html',admin=g.current_user,config=Website_config_get())

#用户管理route
@web.route('/admin/user_manager.html',methods=['GET'])
@login_required
def user_manager_tpl():
	return render_template('user_manager.html',admin=g.current_user,config=Website_config_get(),admins=Admin_init())
'''
#页面管理route
@web.route('/admin/page_manager.html',methods=['GET'])
@login_required
def page_manager_tpl():
	return render_template('page_manager.html',admin=g.current_user,config=Website_config_get(),pages=Page_get())

#子页面管理route
@web.route('/admin/childpage_manager.html',methods=['GET'])
@login_required
def childpage_manager_tpl():
	return render_template('childpage_manager.html',admin=g.current_user,config=Website_config_get(),pages=Childpage_get())

'''

#页面管理route
@web.route('/admin/page_managers.html',methods=['GET'])
@login_required
def page_manager_tpl():
	#print(All_page_get())
	return render_template('page_managers.html',admin=g.current_user,config=Website_config_get(),content=All_page_get().encode('utf-8').decode("unicode_escape"))

#写文章页面route
@web.route('/admin/article_post.html',methods=['GET'])
@login_required
def article_post_tpl():
	return render_template('article_post.html',admin=g.current_user,config=Website_config_get())

#修改文章页面route
@web.route('/admin/article_modify/<filename>',methods=['GET'])
@login_required
def article_modify_tpl(filename):
	filename = filename[:-3]
	if re.match(r'\.',filename):
		return redirect('/admin/article_manager.html')
	else:
		article = Get_markdown(filename)
		#print(article)
		if article != False:
			article = JS_markdown(article)
			return render_template('article_modify.html',admin=g.current_user,config=Website_config_get(),article_content = article)


#文档route
@web.route('/admin/document.html',methods=['GET'])
@login_required
def document_tpl():
	return redirect('http://note.youdao.com/noteshare?id=a75d6982884020a1438ea476a228876c')

#文章管理route
@web.route('/admin/article_manager.html',methods=['GET'])
@login_required
def article_manager_tpl():
	return render_template('article_manager.html',admin=g.current_user,config=Website_config_get(),online_files=Article_online_get(),offline_files=Article_offline_get())


##########################
#          API
##########################


#登录API
@web.route('/admin/API/login',methods=['POST'])
def login():
	if request.get_json():
		login = request.get_json()
	else:
		return jsonify(code=500,msg=u"请输入登录信息")
	username = login["username"]
	password = login["password"]
	if Admin_verify(username,password):
		return jsonify(code=200,msg=u"登录成功")
	return jsonify(code=500,msg=u"登录失败")

#修改网站信息API
@web.route('/admin/API/manager',methods=['POST'])
@login_required
def manager():
	if request.get_json():
		config = request.get_json()
	else:
		return jsonify(code=500,msg=u"请输入信息")
	if Website_config_mod(config):
		return jsonify(code=200,msg=u"修改成功")
	else:
		return jsonify(code=500,msg=u"修改失败")

#修改管理员密码API
@web.route('/admin/API/changepwd',methods=['POST'])
@login_required
def changepwd():
	if request.get_json():
		passwords = request.get_json()
	else:
		return jsonify(code=500,msg=u"请输入密码")
	return Admin_pwd_modify(passwords["prev_pwd"],passwords["new_pwd"],passwords["repeat_new_pwd"])

#登出API
@web.route('/admin/API/logout',methods=['GET'])
@login_required
def logout():
	session.pop("username",None)
	return jsonify(code=200,msg=u"登出成功")

#删除管理员API
@web.route('/admin/API/user/delete',methods=['POST'])
@login_required
def user_delete():
	if request.get_json():
		username = request.get_json()["username"]
		if Admin_delete(username):
			return jsonify(code=200,msg=u"删除成功")
		else:
			return jsonify(code=500,msg=u"删除失败")
	else:
		return jsonify(code=500,msg=u"请输入删除的管理员名")

#创建管理员API
@web.route('/admin/API/user/add',methods=['POST'])
@login_required
def user_add():
	if request.get_json():
		user = request.get_json()
		if Admin_select(user["username"]):
			return jsonify(code=500,msg=u"用户已存在")
		if Admin_add(user):
			return jsonify(code=200,msg=u"创建成功")
		else:
			return jsonify(code=500,msg=u"创建失败")
	else:
		return jsonify(code=500,msg=u"请输入新建信息")

#修改页面信息API
@web.route('/admin/API/page/modify',methods=['POST'])
@login_required
def page_modify():
	if request.get_json():
		nav = request.get_json()['content']
		print(nav)
		if All_page_mod(nav):
			return jsonify(code=200,msg=u"修改成功")
		else:
			return jsonify(code=500,msg=u"修改失败")
	else:
		return jsonify(code=500,msg=u"请输入页面信息")

#上传文章
@web.route('/admin/API/article/post',methods=['POST'])
@login_required
def article_post():
	if request.get_json():
		content = request.get_json()['markdown_content']
		filename = request.get_json()['filename']
		#print(filename)
		if re.match(r'\.',filename):
			return jsonify(code=500,msg=u"文件名错误")
		filename = filename+".md"
		if Save_markdown(filename,content):
			return jsonify(code=200,msg=u"上传成功",path=filename)
		else:
			return jsonify(code=500,msg=u"上传失败")
	else:
		return jsonify(code=500,msg=u"请输入内容")

#修改文章
@web.route('/admin/API/article/modify',methods=['POST'])
@login_required
def article_modify():
	if request.get_json():
		content = request.get_json()['markdown_content']
		filename = request.get_json()['filename']
		if re.match(r'\.',filename):
			return jsonify(code=500,msg=u"文件名错误")
		filename = request.get_json()['filename']+".md"
		#print(filename)
		if Save_markdown(filename,content):
			return jsonify(code=200,msg=u"修改成功",path=filename)
		else:
			return jsonify(code=500,msg=u"修改失败")
	else:
		return jsonify(code=500,msg=u"请输入内容")

#删除所有下线文章
@web.route('/admin/API/article/delete_all',methods=['GET'])
@login_required
def article_delete_all():
	if Article_delete_all():
		return jsonify(code=200,msg=u"清除成功")
	else:
		return jsonify(code=500,msg=u"清除失败")

#删除某个文章
@web.route('/admin/API/article/delete',methods=['POST'])
def article_delete_one():
	if request.get_json():
		file_id = request.get_json()['article_id']
		if Article_delete_one(file_id):
			return jsonify(code=200,msg=u"删除成功")
		else:
			return jsonify(code=200,msg=u"删除失败")
	else:
		return jsonify(code=500,msg=u"请输入文章id")

#备份所有文章
@web.route('/admin/API/article/backup',methods=['GET'])
def article_backup():
	filename = gen_random_string()+".zip"
	z = zipfile.ZipFile(website_path+"/backups/"+filename,"w")
	if os.path.isdir(os.path.join(website_path,"docs/")):
		for d in os.listdir(os.path.join(website_path,"docs/")):
			z.write(os.path.join(website_path,"docs/")+d)
		z.close()
	return send_from_directory(website_path+"/backups/",filename,as_attachment=True)

'''
#删除页面
@web.route('/admin/API/page/delete',methods=['POST'])
@login_required
def page_delete():
	if request.get_json():
		page = request.get_json()
		if Page_delete(page["page"]):
			return jsonify(code=200,msg=u"删除成功")
		else:
			return jsonify(code=500,msg=u"删除失败")
	else:
		return jsonify(code=500,msg=u"请输入删除的页面")

#创建页面
@web.route('/admin/API/page/add',methods=['POST'])
@login_required
def page_add():
	if request.get_json():
		page = request.get_json()["page"]
		if Page_select(page):
			return jsonify(code=500,msg=u"页面已存在")
		else:
			if Page_add(page):
				return jsonify(code=200,msg=u"创建页面成功")
			else:
				return jsonify(code=500,msg=u"创建页面失败")
	else:
		return jsonify(code=500,msg=u"请输入创建的页面名")

#删除子页面
@web.route('/admin/API/childpage/delete',methods=['POST'])
#@login_required
def childpage_delete():
	if request.get_json():
		parentpage = request.get_json()["parent"]
		childpage = request.get_json()["child"]
		Childpage_delete(parentpage,childpage)
		return jsonify(code=200,msg=u"删除成功")
	else:
		return jsonify(code=500,msg=u"请输入删除的页面")
'''

if __name__ == '__main__':
	web.run(host='0.0.0.0',port=8080,debug=True)
