from flask import Flask,render_template,request
import psycopg2
app = Flask(__name__)
# @app.route('/')
# def main():
#     #name = input("Enter the name of student : ")
#     list1 = list()
#     list1 = ['avinash','raut','from','kedgaon','dhumalicha','mala','ravi','avi','savi','kavi']
#     return render_template('index.html',mylist = list1)


# we can make global dictionary so need to pass data from one page to another page

#mydict = {}    #and we can store that data here and we can use in any html page instead of passing from this to this page.
#one more imp thing here that you are passing value from A to B then B to C then data of A is not coming in C so need to do <input type="hidden" name="name" value={{name}}
# if data is hidden then it pass directly there else not..Another option is make global dictionary there so we can use there directly
#use global keyword when we change gloabal varibale inside the local area.



HOST_NAME = 'localhost'
DATABASE_NAME = 'ness'
PORT = 5432
PASSWORD = 'avi123'
DATABASE_USER = 'postgres'

conn = None
cur = None

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_info
        (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            qualification TEXT,
            board TEXT,
            passing_year TEXT,
            percentage TEXT
        )
    """)
    conn.commit()   # <-- Important: commit the transaction
    cur.close()     # <-- Clean up
    conn.close()


def get_connection():
    return psycopg2.connect(host = HOST_NAME,dbname = DATABASE_NAME,port = PORT,password = PASSWORD,user = DATABASE_USER)


def insert_student(name,email,phone,qualification,board,passing_year,percentage):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                insert into student_info
                (
                   name,email,phone,qualification,board,passing_year,percentage
                )
                values(%s,%s,%s,%s,%s,%s,%s)
                """,(name,email,phone,qualification,board,passing_year,percentage))
    conn.commit()
    cur.close()
    conn.close()



@app.route('/')
def personal():
    return render_template('personal.html')

@app.route('/educational',methods=['post'])
def educational():                                        #function name is not used anywhere still now.
    name = request.form['name']                           #this name is coming from value of name attribute from form.
    email = request.form['email']                         #this email is coming from the value of name #i mean i want to say value is imp there in form for name.
    phone = request.form['phone']
    return render_template('educational.html',name = name,email=email,phone=phone)

@app.route('/submited_data',methods = ['POST'])
def mydata():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    qualification = request.form['qualification']
    brd = request.form['board']
    passing_year = request.form['year']
    percentage = request.form['score']

    insert_student(name,email,phone,qualification,brd,passing_year,percentage)

    return render_template('submited_data.html',qualification = qualification,board = brd,p_year = passing_year,percentage = percentage,name = name,email=email,phone = phone)


@app.route('/thankyou',methods = ['POST'])
def last():
    return render_template('thankyou.html')

if __name__=="__main__":
    create_table()
    app.run(debug=True)