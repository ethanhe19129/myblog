"""
只处理与主题相关的路由和视图
"""
import json
import os

import math
from sqlalchemy import func

from . import main
from flask import render_template, session, request, redirect

from .. import db
from ..models import *
import datetime

@main.route("/")
@main.route("/index")
def index_views():
    categories = Category.query.all()
    spec_reco = Topic.query.filter_by(recommend_id=3).order_by(Topic.id.desc()).limit(3).all()
    reco = Topic.query.filter_by(recommend_id=2).order_by(Topic.id.desc()).all()
    mostlike = db.session.query(Voke.topic_id).group_by('topic_id').order_by(func.count('user_id').desc()).all()
    liketopics = []
    id = None
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    if id == 1:
        topics = Topic.query.all()
        for ml in mostlike:
            liketop = Topic.query.filter_by(id=ml[0]).first()
            liketopics.append(liketop)
    else:
        topics = Topic.query.filter(Topic.blogtype_id!=1).all()
        for ml in mostlike:
            liketop = db.session.query(Topic).filter(Topic.id==ml[0],Topic.blogtype_id!=1).first()
            if liketop:
                liketopics.append(liketop)
    return render_template("index.html",params = locals())

@main.route("/getSel")
def getSel_views():
    recommends = Recommend.query.filter(Recommend.id > 1).all()
    list = []
    for reco in recommends:
        list.append(reco.to_dic())
    return json.dumps(list)

@main.route("/release",methods=['GET','POST'])
def release_views():
    if request.method == 'GET':

        # 判断session,判断是否有登录用户
        if 'id' in session and 'loginname' in session:
            # 将id从session中获取出来再查询用户
            id = session['id']
            user = User.query.filter_by(ID=id).first()
            clickmax = Topic.query.order_by(Topic.read_num.desc()).limit(5).all()
            if user.is_author:
                # 1.查询Category的所有的信息
                categories = Category.query.all()
                # 2.查询BlogType的所有的信息
                blogTypes = BlogType.query.all();
                recommends = Recommend.query.filter(Recommend.id>1).all()
                return render_template("release.html",params=locals())
        return redirect('/')
    else:
        # 创建Topic的对象
        topic = Topic()
        # 获取标题(author)为Topic.title赋值
        topic.title = request.form['author']
        # 获取文章类型(list)为Topic.blogtype_id赋值
        topic.blogtype_id = request.form['list']
        # 获取内容类型(category)为Topic.category_id赋值
        topic.category_id = request.form['category']
        # 获取内容(content)为Topic.content赋值
        topic.content = request.form['content']
        # 从session中获取id为Topic.user_id赋值
        topic.user_id = session['id']
        # 获取是否推荐(recommend)为Topic.recommend_id赋值
        if not request.form['recommend']:
            topic.recommend_id = 1
        else:
            topic.recommend_id = request.form['recommend']

        # 获取系统时间为Topic.pub_date赋值
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 判断是否有上传图片,处理上传图片,为Topic.images赋值
        if request.files:
            # 获取上传的文件
            f = request.files['picture']
            # 处理文件名:时间.扩展名
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[-1]
            filename=ftime+'.'+ext
            # 将文件名赋值给topic.images
            topic.images = "upload/"+filename
            # 处理上传路径: static/upload
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir,'static/upload',filename)
            # 上传文件
            f.save(upload_path)
        # 将Topic的对象保存进数据库
        db.session.add(topic)
        return redirect('/')

@main.route("/login", methods=['GET', 'POST'])
def login_views():
    if request.method == "GET":
        return render_template('login.html')
    else:
        loginname = request.form.get('username')
        upwd = request.form.get('password')
        user = User.query.filter_by(loginname=loginname, upwd=upwd).first()
        if user:
            session['id'] = user.ID
            session['loginname'] = user.loginname
            return redirect("/")
        else:
            errMsg = "用户名或密码有误"
            return render_template('login.html', errMsg=errMsg)

@main.route("/register", methods=['GET', 'POST'])
def register_views():
    if request.method == "GET":
        return render_template('register.html')
    else:
        user = User()
        user.loginname = request.form.get('loginname')
        user.uname = request.form.get('username')
        user.email = request.form.get('email')
        user.upwd = request.form.get('password')
        if 'url' in request.form:
            user.url = request.form.get('url')
        db.session.add(user)
        db.session.commit()
        session['id'] = user.ID
        session['loginname'] = user.loginname
        return redirect("/")

@main.route("/logout")
def logout_views():
    if 'id' in session or 'loginname' in session:
        del session['id']
        del session['loginname']
        return redirect('/')

@main.route("/info", methods=['GET', 'POST'])
def info_views():
    if request.method == "GET":
        categories = Category.query.all()
        id = request.args.get('id')
        topic = Topic.query.filter_by(id=id).first()
        try:
            replies = Reply.query.filter_by(topic_id=id).order_by(Reply.id.desc()).all()
        except AttributeError:
            replies = None
        mostlike = db.session.query(Voke.topic_id).group_by('topic_id').order_by(func.count('user_id').desc()).all()
        liketopics = []
        #特别推荐博客
        spec_reco = Topic.query.filter_by(recommend_id=3,category_id=topic.category_id).order_by(Topic.id.desc()).all()
        #推荐博客
        reco = Topic.query.filter_by(recommend_id=2,category_id=topic.category_id).order_by(Topic.id.desc()).all()
        #打开页面增加一次阅读量
        topic.read_num += 1
        db.session.add(topic)
        if request.args.get('like'):
            voke = Voke()
            voke.topic_id = id
            voke.user_id = session['id']
            db.session.add(voke)
            db.session.commit()
        voke_num = Voke.query.filter_by(topic_id=id).count()
        # 判断是否登录
        uid = None
        if 'id' in session and 'loginname' in session:
            user = User.query.filter_by(ID=session['id']).first()
            uid = session['id']
        if uid == 1:
            topics = Topic.query.filter_by(category_id=topic.category_id).all()
            for ml in mostlike:
                liketop = Topic.query.filter_by(id=ml[0], category_id=topic.category_id).first()
                if liketop:
                    liketopics.append(liketop)
            prevTopic = Topic.query.filter(Topic.id < id).order_by(Topic.id.desc()).first()
            nextTopic = Topic.query.filter(Topic.id > id).first()
        else:
            topics = Topic.query.filter(Topic.category_id==topic.category_id, Topic.blogtype_id!=1).all()
            for ml in mostlike:
                liketop = Topic.query.filter(Topic.id==ml[0],Topic.category_id==topic.category_id,Topic.blogtype_id!=1).first()
                if liketop:
                    liketopics.append(liketop)
            prevTopic = Topic.query.filter(Topic.id < id, Topic.blogtype_id!=1).order_by(Topic.id.desc()).first()
            nextTopic = Topic.query.filter(Topic.id > id, Topic.blogtype_id!=1).first()
        return render_template("info.html", params=locals())
    else:
        # 增加评论
        reply = Reply()
        reply.user_id = session['id']
        reply.topic_id = request.form.get('topicID')
        reply.content = request.form.get('comment')
        reply.reply_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(reply)
        if request.headers['referer']:
            return redirect(request.headers['referer'])
        return redirect('/')

@main.route("/list")
def list_views():
    categories = Category.query.all()


    mostlike = db.session.query(Voke.topic_id).group_by('topic_id').order_by(func.count('user_id').desc()).all()
    liketopics = []


    id = None
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()

    #如果是分类点击进入则分类别显示
    if request.args.get('id'):
        cate_id = request.args.get('id')
        if id == 1:
            topics = Topic.query.filter_by(category_id=cate_id).all()
            for ml in mostlike:
                liketop = Topic.query.filter_by(id=ml[0], category_id=cate_id).first()
                if liketop:
                    liketopics.append(liketop)
        else:
            topics = db.session.query(Topic).filter(Topic.category_id==cate_id,Topic.blogtype_id!=1).all()
            for ml in mostlike:
                liketop = db.session.query(Topic).filter(Topic.id==ml[0],Topic.category_id==cate_id,Topic.blogtype_id!=1).first()
                if liketop:
                    liketopics.append(liketop)
        spec_reco = Topic.query.filter_by(recommend_id=3,category_id=cate_id).order_by(Topic.id.desc()).limit(3).all()
        reco = Topic.query.filter_by(recommend_id=2,category_id=cate_id).order_by(Topic.id.desc()).all()
    #如果直接文章列表进入则不分类
    else:
        if id == 1:
            topics= Topic.query.all()
            for ml in mostlike:
                liketop = Topic.query.filter_by(id=ml[0]).first()
                liketopics.append(liketop)
        else:
            topics = Topic.query.filter(Topic.blogtype_id != 1).all()
            for ml in mostlike:
                liketop = db.session.query(Topic).filter(Topic.id==ml[0],Topic.blogtype_id!=1).first()
                if liketop:
                    liketopics.append(liketop)
        spec_reco = Topic.query.filter_by(recommend_id=3).order_by(Topic.id.desc()).limit(3).all()
        reco = Topic.query.filter_by(recommend_id=2).order_by(Topic.id.desc()).all()

    return render_template('list.html', params=locals())

@main.route("/time")
def time_views():
    categories = Category.query.all()
    id = None
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    if id == 1:
        topics = Topic.query.order_by(Topic.pub_date.desc()).all()
    else:
        topics = db.session.query(Topic).filter(Topic.blogtype_id!=1).order_by(Topic.pub_date.desc()).all()
    return render_template("time.html", params=locals())

@main.route("/photo")
def photo_views():
    # 读取Category中的所有内容并发送到index.html显示
    categories = Category.query.all()
    # 判断是否有登录的用户(判断session中是否有id和loginname)
    id = None
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    #分页显示
    #一页8张图
    pageSize = 8
    #获取页数默认为1
    page = int(request.args.get('page', 1))
    #偏移量
    ost = (page - 1) * pageSize
    if id == 1:
        topics = db.session.query(Topic).filter(Topic.images!=None).offset(ost).limit(pageSize).all()
    else:
        topics = db.session.query(Topic).filter(Topic.images != None, Topic.blogtype_id!=1).offset(ost).limit(pageSize).all()
    #获取要展示博客总数
    totalCount = db.session.query(Topic).filter(Topic.images!=None).count()
    #获取最后一页的页数
    lastPage = math.ceil(totalCount / pageSize)
    #设置默认前一页是1
    prePage = 1
    if page > 1:
        prePage = page - 1
        # 计算下一页
        # 通过page计算下一页,并保存在变量nextPage中
    nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1
    return render_template('photo.html', params=locals())

@main.route("/gbook", methods=['GET','POST'])
def gbook_views():
    if request.method == "GET":
        categories = Category.query.all()
        mostlike = db.session.query(Voke.topic_id).group_by('topic_id').order_by(func.count('user_id').desc()).limit(5).all()
        liketopics = []
        for ml in mostlike:
            liketop = Topic.query.filter_by(id=ml[0]).first()
            liketopics.append(liketop)

        spec_reco = Topic.query.filter_by(recommend_id=3).order_by(Topic.id.desc()).limit(3).all()
        reco = Topic.query.filter_by(recommend_id=2).order_by(Topic.id.desc()).all()
        mess_num = Message.query.count()
        messages = Message.query.all()
        if 'id' in session and 'loginname' in session:
            id = session['id']
            user = User.query.filter_by(ID=id).first()
        return render_template('gbook.html', params=locals())
    else:
        if request.form.get('messid'):
            repmess = ReplyMessage()
            repmess.message_id = request.form.get('messid')
            repmess.content = request.form.get('repcontent')
            repmess.user_id = session['id']
            repmess.pub_date = datetime.datetime.now()
            db.session.add(repmess)
        else:
            message = Message()
            message.content = request.form.get('messcontent')
            message.pub_date = datetime.datetime.now()
            message.user_id = session['id']
            db.session.add(message)
        return redirect("/gbook")

@main.route("/about")
def about_views():
    categories = Category.query.all()
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    return render_template('about.html', params=locals())

@main.route('/lognametest')
def lognametest():
    loginname = request.args.get('loginname')
    user = User.query.filter_by(loginname=loginname).first()
    dic = {}
    if user:
        dic['status'] = 0
        dic['msg'] = '登录名已存在'
    else:
        dic['status'] = 1
        dic['msg'] = '通过'
    return json.dumps(dic)

@main.route('/unametest')
def unametest():
    username = request.args.get('username')
    user = User.query.filter_by(uname=username).first()
    dic = {}
    if user:
        dic['status'] = 0
        dic['msg'] = '用户名已存在'
    else:
        dic['status'] = 1
        dic['msg'] = '通过'
    return json.dumps(dic)

@main.route('/emailtest')
def emailtest():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    dic = {}
    if user:
        dic['status'] = 0
        dic['msg'] = '邮箱已注册'
    else:
        dic['status'] = 1
        dic['msg'] = '通过'
    return json.dumps(dic)











