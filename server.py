from flask import send_file, send_from_directory,  Flask, render_template, flash, request, redirect, url_for, session
import mysql.connector as MySQL
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cert", "key.pem")
CERT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cert", "cert.pem")
LIBRARIES = os.path.join(CURRENT_DIRECTORY, "libraries", "")
app = Flask(__name__)
app.config['SECRET_KEY'] = 's0m3th1ng#g00dz'

# Establish MySQL connection to database server.
def databaseConnection():
    connection = MySQL.connect(host= '203.150.37.154',
                           user = 'libraries',
                           passwd = 'libp@ssw0rd#',
                           port = '10004',
                           db = 'libraries')
    return connection

def createLibraries():
    connection = databaseConnection()
    cursor = connection.cursor()
    executeCommand = ("CREATE TABLE IF NOT EXISTS libraries (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL UNIQUE, filename VARCHAR(100) NOT NULL UNIQUE)")
    cursor.execute(executeCommand)
    connection.commit()
    try:
        connection.close()
    except:
        pass

def addLibrary(modelname, filename):
    filename = filename.replace(".py", "")
    connection = databaseConnection()
    cursor = connection.cursor()
    executeCommand = "INSERT INTO libraries (name, filename) VALUES (%s, %s)"
    cursor.execute(executeCommand, (modelname, filename,))
    connection.commit()

def getLibraries():
    connection = databaseConnection()
    cursor = connection.cursor()
    executeCommand = "SELECT name, filename FROM libraries WHERE filename <> %s"
    cursor.execute(executeCommand, ("none",))
    result = cursor.fetchall()
    try:
        connection.close()
    except:
        pass
    return result

@app.route('/libraries/<string:filename>')
def download(filename):
    return send_from_directory(LIBRARIES , filename=filename, as_attachment=True)

@app.route('/libraries')
def libraries():
    libraries = getLibraries()
    return render_template("libraries.html", libraries=libraries)

@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload_post():
    try:
        file = request.files['file']
        filename = file.filename
        modelname = request.form.get("modelname")
        if filename[-3:] == ".py":
            FILE_PATH = os.path.join(CURRENT_DIRECTORY, "libraries", "" , filename)
            file.save(FILE_PATH) # Save at powermeter folder
            addLibrary(modelname, filename)
            success = True
            flash('"' + modelname + '" uploaded successfully.')
        else:
            success = False
            flash("Failed: Can't upload '" + modelname + '" to database.')
        return redirect('libraries')
    except:
        flash("Failed: Can't upload library to database")
        return redirect('libraries')
    return filename

if __name__ == '__main__':
    createLibraries()
    app.run(debug=True, port=8000, host="0.0.0.0")
    #app.run(port=8000, host="0.0.0.0" , ssl_context=(CERT, KEY))
