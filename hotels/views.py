# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.shortcuts import HttpResponse,HttpResponseRedirect
# 操作数据库
from django.db import connection
import sys
import time
import datetime #导入日期时间模块
import random


# 设置页面编码
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

#常见日期设置
timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 本地时间
today = datetime.date.today() #获得今天的日期
tomorrow = today + datetime.timedelta(days=1) #用今天日期加上时间差，参数为1天，获得明天的日期
enter_time=str(today)+" 18:00:00"#入住时间
leave_time=str(tomorrow) +" 12:00:00"#离店时间
random_number=random.randint(150000000000, 190000000000)#生成随机数

#执行sql语句，返回dict
def executeQuery(sql):
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql)
    rawData = cursor.fetchall()
    print rawData
    col_names = [desc[0] for desc in cursor.description]
    print col_names

    result = []
    for row in rawData:
        objDict = {}
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(row):
            print index, col_names[index], value
            objDict[col_names[index]] = value
        result.append(objDict)
    return result

#插入语句
def insertDb(sql):
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    return cursor.execute(sql)

#执行sql语句，如更新或者删除，依据id查询等
def executeSQL(sql):
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    return cursor.execute(sql)

#我的首页
def index_main(request):
    context = {'data': list}
    template = loader.get_template('index_main.html')
    context['data']=executeQuery("select * from hotel_house")
    return HttpResponse(template.render(context))


#我的首页-查询
def index_search(request):
    key_words=''
    flag=False
    if request.method=="POST":
        key_words=request.POST.get('key_words',None)
        if str(key_words).encode("utf8").strip()=='':
            flag=True
    context = {'data': list}
    template = loader.get_template('index_main.html')
    if flag:
        sql="select * from hotel_house"
        context['data'] = executeQuery(sql)
    else:
        sql = "select * from hotel_house where hotel_name like '%%%%%s%%%%'" % key_words
        context['data'] = executeQuery(sql)
    return HttpResponse(template.render(context))




#注册页面
def registry_ui(request):
    return render(request, 'registry_ui.html')

#用户注册
def registry(request):
    username=request.POST.get("username",'');
    password = request.POST.get("password", '');
    real_name = request.POST.get("real_name", '');
    gender = request.POST.get("gender", '');
    address = request.POST.get("address", '');
    phone = request.POST.get("phone", '');
    age = request.POST.get("age", 0);
    head_pic='18143441.jpg'
    registry_time=str(timeNow)
    sql="select id from hotel_user where username='%s'"%(username)
    result=executeSQL(sql)
    if int(result)!=0:
        context = {'error_message': '该用户名已存在'}
        template = loader.get_template('registry_ui.html')
        return HttpResponse(template.render(context))

    sql='insert into hotel_user (username,password,real_name,gender,registry_time,address,phone,head_pic,role_type,age) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%d","%d")' % \
        (str(username).encode("utf8"),password,real_name,str(gender).encode("utf8"),registry_time,str(address).encode("utf8"),phone,head_pic,0,int(str(age).encode("utf8")))
    result=insertDb(sql)
    print "注册结果：",result

    return render(request, 'login_ui.html')

#登陆页面
def login_ui(request):
    return render(request, 'login_ui.html')


#登陆
def login(request):
    username=request.POST.get("username",'');
    password = request.POST.get("password", '');
    role_type=request.POST.get("role_type", -1);
    sql="select id from hotel_user where username='%s'  and password= '%s'"%(username,password)
    cursor=connection.cursor()
    result=cursor.execute(sql)
    if int(result)==1:
        sql="select id from hotel_user where username='%s'  and password= '%s'and role_type = '%d'"%(username,password,int(str(role_type)))
        result = cursor.execute(sql)
        if int(result)==1:#用户名和密码正确，判断类别权限
            request.session['user_id'] = cursor.fetchone()[0] #登陆成功，将用户id放入session中
            sql="select real_name,gender,registry_time,address from hotel_user where username='%s'  and password= '%s'"%(username,password)
            context = {'data': executeQuery(sql)[0]}
            template = loader.get_template('home.html')
            if int(role_type)==1:#根据角色进入管理员页面
                template = loader.get_template('admin_home.html')
            return HttpResponse(template.render(context))
        else:
            context = {'error_message': '权限选择不正确'}
            template = loader.get_template('login_ui.html')
            return HttpResponse(template.render(context))
    else:
        context = {'error_message': '用户名或密码不正确'}
        template = loader.get_template('login_ui.html')
        return HttpResponse(template.render(context))


#注销
def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return render(request, 'login_ui.html')

#个人首页页面
def home(request):
    if request.session:  #登陆后，具有session
        try:
            user_id = request.session['user_id']
            sql = "select real_name,gender,registry_time,address,role_type from hotel_user where id= '%d'"%(user_id)
            context = {'data': executeQuery(sql)[0]}
            role_type=context['data']['role_type']#获取用户角色信息
            template = loader.get_template('home.html')
            if int(role_type)==1:
                template = loader.get_template('admin_home.html')
            return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
        return render(request, 'login_ui.html')

#随心行酒店首页
def  home_main(request):

    context = {'data': list}
    template = loader.get_template('home_main.html')
    context['data'] = executeQuery("select * from hotel_house")
    return HttpResponse(template.render(context))

#我的首页-查询
def home_search(request):
    key_words=''
    flag=False
    if request.method=="POST":
        key_words=request.POST.get('key_words',None)
        if str(key_words).encode("utf8").strip()=='':
            flag=True
    context = {'data': list}
    template = loader.get_template('home_main.html')
    if flag:
        sql="select * from hotel_house"
        context['data'] = executeQuery(sql)
    else:
        sql = "select * from hotel_house where hotel_name like '%%%%%s%%%%'" % key_words
        context['data'] = executeQuery(sql)
    return HttpResponse(template.render(context))

#酒店预定页面
def hotel_order(request):
    context = {}
    template = loader.get_template('hotel_order.html')
    if request.session:  # 登陆后，具有session
        try:
            user_id = request.session['user_id']
            id=request.GET.get('id',1)
            sql="select * from hotel_house where id= "+id
            sql2="SELECT a.`real_name`,a.head_pic,b.comments_score,b.comments_content,b.comments_time from hotel_user a,hotel_comment b where a.id=b.user_id and b.house_id="+id+" ORDER BY b.comments_time desc"
            commentList=executeQuery(sql2)
            context['data'] = executeQuery(sql) #酒店数据
            context['commentList']=commentList  #评论列表数据
            context['commentCount']=len(commentList) #评论总数

            #准备酒店预订信息
            sql3="SELECT a.`real_name`,a.phone,b.hotel_name,b.price\
                  from hotel_user a,hotel_house b\
                  where a.id='%d' and b.id= '%d'"%(int(user_id),int(id))
            context['orderDetails']=executeQuery(sql3)[0]
            context['from']=enter_time
            context['to']=leave_time

            return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
        return render(request, 'login_ui.html')

#酒店下单
def book_hotel(request):
    context = {'data': ''}
    template = loader.get_template('my_order.html')
    if request.session:  # 登陆后，具有session
        try:
            house_id = request.POST.get("house_id", '');
            enter_time = request.POST.get("enter_time", '');
            leave_time = request.POST.get("leave_time", '');
            order_time=str(timeNow)
            user_id = request.session['user_id']
            order_state="已预订"
            order_number=random_number
            sql = "insert into hotel_user_order (user_id,order_time,order_numbers,order_state,leave_time,enter_time,house_id) values ('%d','%s','%s','%s','%s','%s','%d')"%(int(user_id),order_time,order_number,order_state,leave_time,enter_time,int(house_id))
            result = executeSQL(sql)
            if int(result)==1:
                return HttpResponseRedirect('/my_order.action?id='+house_id)#重定向到action
            else:
                context['data']='请重试'
                return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
        return render(request, 'login_ui.html')


#添加评论
def add_comment(request):
    context = {'data': ''}
    template = loader.get_template('hotel_order.html')
    if request.session:  # 登陆后，具有session
        try:
            house_id = request.POST.get("house_id", '');
            comments_content = request.POST.get("comments_content", '');
            comments_score = request.POST.get("comments_score", 1);
            comments_time=str(timeNow)
            user_id = request.session['user_id']
            sql = "insert into hotel_comment (house_id,user_id,comments_time,comments_content,comments_score) values ('%d','%d','%s','%s','%d')"%(int(str(house_id)),int(user_id),comments_time,comments_content,int(comments_score))
            cursor = connection.cursor()
            result = cursor.execute(sql)
            if int(result)==1:
                sql="update hotel_house set comments_num =comments_num +1 where id ='%d'"%(int(house_id))#酒店评价数量更新
                cursor.execute(sql)
                return HttpResponseRedirect('/hotel_order.action?id='+house_id)#重定向到action
            else:
                context['data']='请刷新重试'
                return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
        return render(request, 'login_ui.html')

#我的订单
def my_order(request):
    context = {'data': list}
    template = loader.get_template('my_order.html')
    if request.session:  #登陆后，具有session
        try:
            user_id = request.session['user_id']
            sql="SELECT a.`real_name`,a.head_pic,b.order_time,b.order_numbers,b.order_state,b.enter_time,b.leave_time,c.hotel_pic,c.hotel_name\
            from hotel_user a,hotel_user_order b,hotel_house c\
            where b.user_id=a.id and b.house_id = c.id and b.user_id='%d' ORDER BY b.order_time DESC "%(user_id)
            context['data']=executeQuery(sql)
            return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
         return render(request, 'login_ui.html')

# 管理员查看所有订单
def all_orders(request):
    context = {'data': list}
    template = loader.get_template('admin_all_orders.html')
    if request.session:  # 登陆后，具有session
        try:
            user_id = request.session['user_id']
            sql = "SELECT a.`real_name`,a.head_pic,b.order_time,b.order_numbers,b.order_state,b.enter_time,b.leave_time,c.hotel_pic,c.hotel_name\
            from hotel_user a,hotel_user_order b,hotel_house c\
            where b.user_id=a.id and b.house_id = c.id ORDER BY b.order_time DESC "
            context['data'] = executeQuery(sql)
            return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
        return render(request, 'login_ui.html')

#我的主页---仅仅测试环境
def index(request):
    template = loader.get_template('home_main.html')
    context = {'data': list}

    #操作数据库
    from django.db import connection, transaction
    cursor = connection.cursor()

    # 数据修改操作——提交要求
    cursor.execute("select * from person")
    lists = cursor.fetchall();

    context['data']=lists
    print "sql--->",list

    return HttpResponse(template.render(context))

#修改密码页面
def password_ui(request):
    if request.session:  #登陆后，具有session
        return render(request, 'edit_password_ui.html')
    else:
        return render(request, 'login_ui.html')

#修改密码
def edit_password(request):
    password=request.POST.get("password",'');
    newPassword = request.POST.get("newPassword", '');

    context = {'error_message': ''}
    template = loader.get_template('edit_password_ui.html')
    if request.session:  #登陆后，具有session
        try:
            if len(str(password).strip())==0:
                context['error_message']='原始密码不能为空'
                return HttpResponse(template.render(context))
            elif len(str(newPassword).strip())==0:
                context['error_message']='新密码不能为空'
                return HttpResponse(template.render(context))

            user_id=request.session['user_id']
            sql="SELECT id from hotel_user where password ='%s' and id = '%d'"%(password,user_id)#判断密码是否正确
            cursor = connection.cursor()
            result = cursor.execute(sql)
            print "修改操作：",result
            if int(result)==1:
                sql="update hotel_user set password ='%s' where id ='%d'"%(newPassword,user_id)
                cursor.execute(sql)#修改密码
                return render(request, 'login_ui.html')
            else:
                context['error_message']='原始密码不正确'
                return HttpResponse(template.render(context))
        except Exception,e:
            return render(request, 'login_ui.html')
    else:
         return render(request, 'login_ui.html')