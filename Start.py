from flask import Flask,abort, redirect, url_for,flash,request,render_template
import os
import requests
import time
import datetime
import pymysql
import xlrd
import xlwt
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
Cookie = ''
Token = ''
url2 = "http://wego.istarshine.com/task/filterTasks?id=&project_id=&site_name=&site_url=&username=&site_type=&domain=&ctime=&receive_flag=&submit_flag=&allocation_flag=&qualified_passed_flag=&status=11&limit=10&page={}"
d2 = {
"Host": "wego.istarshine.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
"Accept": "*/*",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate",
"X-Requested-With": "XMLHttpRequest",
"Connection": "keep-alive",
"Referer": "http://wego.istarshine.com/task/mine?status=11",
"Cookie": "",}
d = {"POST": "/maintain/task_manage_staff HTTP/1.1",
     "Host": "wego.istarshine.com",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
     "Accept": "*/*",
     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
     "Accept-Encoding": "gzip, deflate",
     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
     "X-Requested-With": "XMLHttpRequest",
     "Content-Length": "249",
     "Origin": "http://wego.istarshine.com",
     "Connection": "keep-alive",
     "Referer": "http://wego.istarshine.com/maintain/task_manage_staff?status_id=14",
     "Cookie": "",
     }
data2 = {
    "csrfmiddlewaretoken": "",
    "id": "",
    "project_id": "",
    "site_name": "",
    "site_url": "",
    "domain": "",
    "ctime": "",
    "receive_flag": "",
    "submit_flag:": "",
    "allocation_flag": "",
    "finish_flag": "",
    "lang": "",
    "status_id": "14",
    "manage_type": "task_manage_staff",
    "page": "1",
}
num_protect = 0
ALLinformation = []
DiffenceId = []
fliterStarttime = "2021-9-10 08:00:00"
fliterEndtime = "2021-9-27 08:00:00"
num_Page_protect = 10
num_Page_new = 2
result =[]
def timetrans(timeflag):
    time_local = time.localtime(timeflag)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt
def get_sucess_protect(data2,d,fstime,fetime):
    url = "http://wego.istarshine.com/maintain/task_manage_staff"
    r = requests.post(url, data=data2, headers=d)
    data = r.json()
    taskx = data.get("tableData").get("tasks")
    global num_protect
    global ALLinformation
    for task in taskx:
        information = []
        ctime = task.get("pass_flag")
        if ctime<fstime:
            continue
        if ctime>fetime:
            continue
        id = task.get("id")
        site_name = task.get("site_name")
        Money = 0
        is_modify = task.get("is_modify_code")
        if is_modify:
            Money=8
        else :
            Money=1
        information.append(id)
        information.append(site_name)
        information.append(timetrans(ctime))
        information.append(Money)
        ALLinformation.append(information)
        num_protect +=1
def get_success_newcode(url_x, d,fstime,fetime):
    r = requests.get(url_x, headers=d)
    data = r.json()
    taskx = data.get("tableData").get("tasks")
    global num_protect
    global ALLinformation
    for task in taskx:
        information = []
        ctime = task.get("finish_flag")
        if ctime<fstime:
            continue
        if ctime>fetime:
            continue
        id = task.get("id")
        site_name = task.get("site_name")
        Money = 15
        information.append(id)
        information.append(site_name)
        information.append(timetrans(ctime))
        information.append(Money)
        ALLinformation.append(information)
        num_protect +=1
def get_sum():
    global ALLinformation
    Summoney = 0
    ctime = datetime.datetime.utcnow()
    for infor in ALLinformation:
        Summoney += int(infor[3])
    sumitem = ['66666','总和',str(len(ALLinformation)),Summoney] 
    ALLinformation.append(sumitem)
def get_encode(Cookie):
    Cookie.replace('; ',' ')
    return Cookie
def get_decode(Cookie):
    Cookie.replace(' ','; ')
def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='Dragon', passwd='tianxiu123', db='dragon',charset='utf8')
    return conn
def insert(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    conn.commit()
    cur.close()
    conn.close()
def update(sql,args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql,args)
    conn.commit()
    cur.close()
    conn.close()    
def query(sql,args):
    result = []
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql,args)
    results = cur.fetchall()
    for row in results:
        username = row[0]
        password = row[1]
        Cookie =row[2]
        token = row[3]
        result.append(username)
        result.append(password)
        result.append(Cookie)
        result.append(token)
        pass
    return result
def My_Find(username):
    sql = 'SELECT  * FROM user where username=%s;'
    args = username
    result = query(sql,args)
    if result == []:
        err=True
        return result,err
    else:
        err = False
        return result,err
def My_Update(username,word,value,):
    args = (value,username)
    sql = 'UPDATE user SET '+word+'=%s WHERE username = %s;'
    update(sql, args)
def My_insert(username,password,Cookie,token):
    sql='INSERT INTO user VALUES(%s,%s,%s,%s)'
    insert(sql,(username,password,Cookie,token))
def get_fileinformation(Zhewang_path):
    global ALLinformation
    global DiffenceId
    freadZh = xlrd.open_workbook(Zhewang_path, formatting_info=True)
    Zhget_sheet_name = freadZh.sheet_names()[0]
    # #根据名称获取表页
    Mysheetnrow = len(ALLinformation)
    Zhsheet = freadZh.sheet_by_name(Zhget_sheet_name)
    Zhsheetnrow = Zhsheet.nrows
    for i in range(0, Mysheetnrow):
        for j in range(0, Zhsheetnrow):
            if ALLinformation[i][0] == Zhsheet.row_values(j)[0]:
                if ALLinformation[i][3] != Zhsheet.row_values(j)[3]:
                    DiffenceId.append(ALLinformation[i][0])
@app.route('/',methods=['POST','GET'])
def login():
    global result
    err =0
    islog = request.args.get('register', '')
    if request.method =='GET':
        if islog =="1":
           return redirect(url_for('log'))
    if request.method == 'POST':
            usr = request.form['name']
            pwd = request.form['pwd']
            result,err = My_Find(usr)
            if  err:
                err = 1
                return render_template('login.html',err=err)
            else:
                if result[1] == pwd:
                    return redirect(url_for('index'))
                else:
                    err=2
                    return render_template('login.html',err=err)
    return render_template('login.html',err=err)
@app.route('/index',methods=['POST','GET'])
def index():
            global result
            global num_Page_protect
            global num_Page_new
            global fliterEndtime 
            global fliterStarttime
            global ALLinformation
            global DiffenceId
            Cookie =result[2]
            Token =result[3]
            if request.method == 'POST':
                need_chagneinfor = request.form['inforusr']
                if need_chagneinfor=="1":
                    CurCookie = request.form['Cookie']
                    CurToken = request.form['Token']
                    if CurCookie!="":
                        My_Update(result[0],'Cookie',CurCookie)
                    if CurToken!="":
                        My_Update(result[0],'token',CurToken)
                    result,err = My_Find(result[0])
                elif need_chagneinfor=="2":
                     print("qqqq")
                     f = request.files['money']
                     filename = './' + secure_filename(f.filename)
                     f.save(filename)
                     get_fileinformation(filename)
                     os.remove(filename)
                else:
                    DiffenceId = []
                    ALLinformation= []
                    fliterStart = request.form['starttime']
                    if fliterStart!="":
                        fliterStart = fliterStart +" 08:00:00"
                    else:
                        fliterStart = fliterStarttime
                    fliterEnd = request.form['endtime']
                    if fliterEnd!="":
                        fliterEnd = fliterEnd +" 08:00:00"
                    else :
                        fliterEnd = fliterEndtime
                    Page_new = 2
                    Page_pro = 2
                    if request.form['pagenew']!="":
                            Page_new = int(request.form['pagenew'])
                    else:
                            Page_new = num_Page_protect
                    if request.form['pagepro']!="":
                            Page_pro =  int(request.form['pagepro'])
                    else:
                        Page_pro =num_Page_protect
                    fStime = int(time.mktime(time.strptime(fliterStart, "%Y-%m-%d %H:%M:%S")))
                    fEtime = int(time.mktime(time.strptime(fliterEnd, "%Y-%m-%d %H:%M:%S")))
                    d["Cookie"] = Cookie
                    d2["Cookie"] = Cookie
                    data2["csrfmiddlewaretoken"]=Token
                    for x in range(1,Page_pro+1):
                        data2["page"]=str(x)
                        get_sucess_protect(data2,d,fStime,fEtime)
                    for m in range(1,Page_new+1):
                        url_xm = url2.format(str(m))
                        get_success_newcode(url_xm, d2,fStime,fEtime)
                    get_sum()
            return render_template('index.html',information=ALLinformation,result=result,DiffenceId=DiffenceId)
@app.route('/log',methods=['POST','GET'])
def log():
    if request.method == 'POST':
        usr = request.form['name']
        pwd = request.form['pwd']
        CurCookie = request.form['cookie']
        CurToken = request.form['token']
        My_insert(usr,pwd,CurCookie,CurToken)
        return redirect(url_for('login'))
    return render_template('log.html')