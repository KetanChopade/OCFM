from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/validate_admin', methods=['post'])
def validate_admin():
    uname = request.form.get("t1")
    upass = request.form.get("t2")
    if uname == "ketan" and upass == "chopade":
        return render_template("admin_welcome.html")
    else:
        mess = {"error":"Invalid user"}
        return render_template("admin_login.html",message = mess )

@app.route('/admin_home')
def admin_home():
    return render_template('admin_welcome.html')

@app.route('/new_class')
def new_class():
    return render_template("new_class.html")

@app.route('/save_course', methods=['post'])
def save_course():
    cname = request.form.get("c1")
    fname = request.form.get("c2")
    date = request.form.get("c3")
    time = request.form.get("c4")
    fees = request.form.get("c5")
    dur = request.form.get("c6")
    conn = sql.connect("onlineclasse.sqlite2")
    curs = conn.cursor()
    curs.execute("select max (cno) from course")
    res = curs.fetchone()
    if res[0]:
        cno = res[0]+1
    else:
        cno = 1001
    curs.execute("insert into course values (?,?,?,?,?,?,?)",(cno,cname,fname,date,time,fees,dur))
    conn.commit() #commit is used for saving the record
    conn.close()
    return render_template('new_class.html' , message = "New Course saved")

@app.route('/view_scheduled_class')
def view_scheduled_class():
    conn = sql.connect("onlineclasse.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course")
    result = curs.fetchall()
    conn.close()
    return render_template("view_scheduled_class.html",data = result)

@app.route('/upadte_course')
def upadte_course():
    idno = request.args.get("cno")
    conn = sql.connect("onlineclasse.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course where cno = ?",(idno,))
    res = curs.fetchone()
    return render_template('upadte_course.html', data=res)

@app.route('/save_upadte_course', methods=['post'])
def save_upadte_course():
    cid = request.form.get("c0")
    cname = request.form.get("c1")
    fname = request.form.get("c2")
    date = request.form.get("c3")
    time = request.form.get("c4")
    fees = request.form.get("c5")
    dur = request.form.get("c6")
    conn = sql.connect("onlineclasse.sqlite2")
    curs = conn.cursor()
    curs.execute(" update course set course_name = ?  ,faculty_name = ? ,class_date = ? ,class_time = ? ,fee = ? ,duration = ? where cno = ?",(cname,fname,date,time,fees,dur,cid))
    conn.commit()
    conn.close()
    return view_scheduled_class()

@app.route('/delete')
def delete():
    conn = sql.connect("onlineclasse.sqlite2")
    curs = conn.cursor()
    cno = request.args.get("cno")
    curs.execute(' delete from course where cno = ?',(cno,))
    conn.commit()
    conn.close()
    return view_scheduled_class()

if __name__ == '__main__':
    app.run(debug=True)
