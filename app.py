from flask import Flask,redirect,render_template,url_for,request,session,flash
from flask_mysqldb import MySQL


app=Flask(__name__)
  
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="CRUd"
app.config['MYSQL_CHARSET'] = "latin1"
mysql=MySQL(app)
  
app.secret_key="host452456246246"


@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM  employees")
    data=cur.fetchall()
    return render_template("index.html",data=data)

@app.route('/index')
def rain():
    return render_template("new.html")


@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=='POST':
        user_id=request.form['id']
        username=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO employees(name,email,phone) VALUES(%s,%s,%s)",(username,email,phone))
        mysql.connection.commit()
        cur.close()
        flash("Employee added successfully","success")
        return redirect(url_for('index'))
    return render_template("add.html")


@app.route('/update/<id>',methods=['POST','GET'])
def update(id):
    
    if request.method=='POST':
        user_id=request.form['id']
        username=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE employees SET name=%s,email=%s,phone=%s WHERE id=%s",(username,email,phone,id,))
        mysql.connection.commit()
        cur.close()
        flash("Data updated successfully","success")
        return redirect(url_for('index'))
    
    cur=mysql.connection.cursor()
    cur.execute("SELECT *  FROM employees WHERE id=%s",(id,))
    data=cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return render_template("update.html",update=data)

@app.route('/delete/<id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s",(id,))
    flash("Data deleted successfully","danger")
    return redirect(url_for('index'))

if __name__ =='__main__':
    app.run(debug=True)
    