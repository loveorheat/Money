import pymysql
def get_encode(Cookie):
    Cookie.replace('; ',' ')
    return Cookie
def get_decode(Cookie):
    Cookie.replace(' ','; ')
def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='dragon',charset='utf8')
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
    print(result)
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
        print(row)
        username = row[0]
        password = row[1]
        Cookie = row[2]
        token = row[3]
        result.append(username)
        result.append(password)
        result.append(Cookie)
        result.append(token)
        pass
    return result
def My_Find(username):
    sql = 'SELECT  * FROM User where username=%s;'
    args = username
    result = query(sql,args)
    print(result)
    if result == []:
        err=True
        return result,err
    else:
        err = False
        return result,err   
def My_Update(username,word,value,):
    args = (value,username)
    sql = 'UPDATE User SET '+word+'=%s WHERE username = %s;'
    update(sql, args)
def My_insert(username,password,Cookie,token):
    sql='INSERT INTO User VALUES(%s,%s,%s,%s)'
    insert(sql,(username,password,Cookie,token))
value1 = "csrftoken=JDyF6MUNJfdGz6SnT2batV1ct5YIF6QA1MFtBsgeOSYpBqxjNmXV7Par9wY5lYgQ; sessionid=d81xwb9zbd5u89qxo5efdeb5gxjtcilu; aliyungf_tc=3d401d6ecf4932a6afb4eea2db6e09a14329e6c1830d22eb6b91a56c5c65105f"
#My_Update('dragon','Cookie',value1)
#result,err = My_Find('dragon')
My_insert('test','123',value1,'13')
result,err = My_Find('test')
print(result[2])
print('\n')
