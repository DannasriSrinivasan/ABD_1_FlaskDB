from distutils.log import debug
from flask import Flask, render_template, request
import pyodbc
import hashlib
import time
import pickle

server = 'danna.database.windows.net' 
database = 'datadxs' 
username = 'dxsdb' 
password = 'Happyme@1'

dbConnection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = dbConnection.cursor()


app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/updateComment')
def updateComment():
    return render_template('updateComment.html')

@app.route('/searchAgeRange')
def searchClassRange():
    return render_template('searchAgeRange.html')

@app.route('/addEntity')
def addEntity():
    return render_template('AddEntity.html')

@app.route('/table', methods=['POST','GET'])
def viewEntity():
    cursor.execute("Select * from danna")
    result = cursor.fetchall()
    return render_template("viewEntity.html",values = result)


@app.route('/update', methods=['POST','GET'])
def update():
    sName = request.form['searchName']
    uComment = request.form['comments']
    cursor.execute("UPDATE data set comments = '"+uComment+"' where name = '"+sName+"'")
    cursor.execute("Select * from data where name = '"+sName+"'")
    result = cursor.fetchall()
    return render_template("viewEntity.html",values = result)

@app.route('/searchAge', methods=['POST','GET'])
def searchAge():
    cursor.execute("Select * from danna WHERE age BETWEEN "+request.form['start']+" AND "+request.form['end']+" and age is not null")
    result = cursor.fetchall()
    return render_template("viewEntity.html",values = result)

@app.route('/addEntry', methods=['POST','GET'])
def addEntry():
    cursor.execute("INSERT INTO danna VALUES ('"+request.form['name']+"','"+request.form['age']+"','"+request.form['class']+"','"+request.form['picture']+"','"+request.form['comments']+"')")
    cursor.execute("Select * from danna where name = '"+request.form['name']+"'")
    result = cursor.fetchall()
    return render_template("viewEntity.html",values = result)

if __name__ == '__main__':
    app.run(debug = True)
    