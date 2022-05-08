

from flask import Flask,Blueprint,render_template,request,flash,redirect,session,url_for
from . import mysql

auth=Blueprint('auth',__name__)  # further we also need to register the blue print

@auth.route("/login",methods=["GET","POST"])  
def login():
    if request.method=="POST":
        if "email" in request.form and "password" in request.form:
            email=request.form.get("email")
            password=request.form.get("password")
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT * FROM account WHERE EMAIL = % s AND UPASS = % s', (email, password, ))
            account = cursor.fetchone()
            if account: # session is like a dictionary for browser in which several key-value pairs coud be saved
                session['loggedin'] = True        # creating and setting keys for session as loggedin , id , username
                session['id'] = account['UID'] 
                session['EMAIL'] = account['EMAIL']
                flash("Logged inn successfully",category="success")
                return render_template("home.html") # we have just logged inn so directly render the template 
            else:
                flash("Email and password not found -- Register again",category="error")
                return redirect(url_for("auth.sign_up"))
        else:
            flash("Fill all the details",category="error")
                                
    return render_template("login.html")        

@auth.route("/logout")
def logout():
     session.pop('loggedin', None)
     session.pop('id', None)
     session.pop('username', None)
     return redirect(url_for('auth.login'))                    

@auth.route("/sign_up",methods=["GET","POST"])    
 
def sign_up():
    if request.method=="POST":  # so if the method is post then do this
           if ('firstname' in request.form and 'password1' in request.form and 'email' in request.form and "password2" in request.form):

                email=request.form.get("email")
                firstname=request.form.get ("firstname")  # request.form.get is method in python also
                password1=request.form.get("password1")
                password2=request.form.get("password2")   # if we want to search for some random name in url then we can open a form and use get request as it enders fields in url only  
        
                if len(email)<4:
                    flash("Email must be greater than 4 characters",category="error") # flashing the messages on screen
                
                if len(firstname)<3:
                    flash("Name must have more than 3 characters",category="error")
                
                if password1!=password2:
                    flash("Both passwords are not same",category="error")
    
                else:
                     cursor=mysql.connection.cursor()    # make a cursor in this case a dict cursot which fetch  all the rows in  form of a dictionary 
                    
                     cursor.execute("SELECT * FROM account WHERE EMAIL= '{}' ".format(email))  # execute a  query  here account is name of a table 
                     fetched_account=cursor.fetchall()    # fetch first  row of table 
                     if(fetched_account):
                         cursor.close()
                         flash("Account already registered")
                         return redirect(url_for("auth.login"))
                     else:
                    
                         cursor.execute('INSERT INTO account(UNAME,UPASS,EMAIL) VALUES(%s,%s,%s)',(firstname,password1,email)) 
                         mysql.connection.commit()
                         cursor.close()
                         flash('Registration Successfully. Login Here...',category='success')
                         return redirect(url_for("auth.login"))   # redirect similar to .get method of a link
    
           else:
               flash("Fill all the details in the form",category="error")


    return render_template("sign_up.html") # First its rendered then after filling form post method is activated  and above things are done 
     
# By default .route is get method 
# Even if i am rendering different html from same route  we kept remaining on the same route only 
# In get method we can get params of url like subreddit we have done and we cas use those params for our searches in databse 
# Rendering and redirecting are different  rendering is rendering a template and redirecting is like .get to the url
# In post we can get the details from the form 
# learn about url_for for static files and downloading static files
# suppose i am rendering home from login link after logging in even then i will remain on login link only my url is not changing 
