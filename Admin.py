import sqlite3  
  
con = sqlite3.connect("employee.db")  
print("Database opened successfully")  
  
# con.execute("create table Employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, roll TEXT UNIQUE NOT NULL, email TEXT NOT NULL, marks_short TEXT NOT NULL, marks_des TEXT NOT NULL)")  
  
print("Table created successfully")  
  
con.close()

from werkzeug.wrappers import Request, Response
from flask import *  
import sqlite3  
  
app = Flask(__name__)  
 
@app.route("/")  
def index():  
    return render_template("A_index.html");  
 
@app.route("/add")  
def add():  
    return render_template("A_add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            name = request.form["name"]  
            email = request.form["email"]  
            address = request.form["address"]  
            with sqlite3.connect("employee.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)",(name,email,address))  
                con.commit()  
                msg = "Employee successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the employee to the list"  
        finally:  
            return render_template("A_success.html",msg = msg)  
            con.close()  
 
@app.route("/view")  
def view():  
    #t=1
    con = sqlite3.connect("employee.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees")
    #cur.execute("select * from Employees where ID = {}".format(t))  
    rows = cur.fetchall()  
    return render_template("A_view.html",rows = rows)  
 
 
@app.route("/delete")  
def delete():  
    return render_template("A_delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("employee.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Employees where id = ?",id)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("A_delete_record.html",msg = msg)  
  
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 3000, app)