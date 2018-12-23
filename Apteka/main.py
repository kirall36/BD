from flask import Flask, render_template
import pymysql.connections
import pymysql.cursors

app = Flask(__name__)


@app.route('/')
def indexform():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="apteka"
    )
    with mydb:
        mycursor = mydb.cursor()
        query = "SELECT * FROM drug"
        mycursor.execute(query)
        print("cursor.description: ", mycursor.description)
        for row in mycursor:
            print(row)
    return render_template('./apteka.html')


if __name__ == '__main__':
    app.run(debug=True)
