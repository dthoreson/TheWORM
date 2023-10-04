from flask import Flask, render_template, session, request, redirect

from flask_bcrypt import Bcrypt

app = Flask(__name__) 
BCRYPT = Bcrypt(app)

DATABASE = 'the_worm_schema'

app.secret_key = "secretkey" 

