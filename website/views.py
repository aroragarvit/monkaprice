from flask import Flask,Blueprint,render_template,request,flash,redirect,session,url_for   # Just like a normal flask application, a blueprint defines a collection of views, templates and static assets.
import numpy as np
import yfinance as yahooFinance
import tensorflow as tf
import keras
from keras.models import load_model
import joblib 
model = tf.keras.models.load_model('.\website\saved_model\my_model')
scaler=joblib.load(".\website\scaler.save")
scaler2=joblib.load(".\website\scaler2.save")           

views=Blueprint('views',__name__)  # now register this blue print in crate app 

@views.route('/')
def home():
     if 'loggedin' in session:
        model = tf.keras.models.load_model('.\website\saved_model\my_model')
        opening_model= tf.keras.models.load_model('.\website\saved_model2\my_model5')
        
        scaler=joblib.load(".\website\scaler.save")
        scaler2=joblib.load(".\website\scaler2.save")
        
       
        opening_scaler=joblib.load(".\website\openingscaler.save")
        opening_scaler2=joblib.load(".\website\openingscaler2.save")

        GetBitcoinInformation = yahooFinance.Ticker("BTC-USD")
        input=GetBitcoinInformation.history(period="150d")
        input_new=scaler.transform(input.iloc[:,0:5].values)
        tomorrow_result = scaler2.inverse_transform(model.predict(input_new.reshape(-1,150,5))).reshape(1,)
        print(tomorrow_result)
        ##### upto here i am having daily prediction and add try catch for the case we are having not able to fetch data from api
        input_new_opening=opening_scaler.transform(input.iloc[:,[0]].values)
        prediction_array=[]
        predict_for=30
        for i in range(0,predict_for):
            tomorrow_prediction=opening_model.predict(input_new_opening.reshape(-1,150,1))
            prediction_array.append((opening_scaler2.inverse_transform(tomorrow_prediction)).reshape(1,))
            
            
            input_new_opening=np.delete(input_new_opening,0,axis=0)
            input_new_opening=np.append(input_new_opening,tomorrow_prediction,axis=0)
            
            print(prediction_array)


         
        return render_template("home.html",value=tomorrow_result)

     else:
        return redirect(url_for('auth.login'))