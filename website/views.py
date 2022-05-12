# Just like a normal flask application, a blueprint defines a collection of views, templates and static assets.
from flask import Flask, Blueprint, render_template, request, flash, redirect, session, url_for, jsonify
import numpy as np
import datetime
import yfinance as yahooFinance
import tensorflow as tf
import keras
from keras.models import load_model
import joblib
import json
import pandas as pd
model = tf.keras.models.load_model('.\website\saved_model\my_model')
scaler = joblib.load(".\website\scaler.save")
scaler2 = joblib.load(".\website\scaler2.save")

# now register this blue print in crate app
views = Blueprint('views', __name__)

#  making variable as global to pass to another root


# As soon as home is rendered javascript is fetching data and showing it  from the route defined below
@views.route('/')
def home():
    if 'loggedin' in session:

        return render_template("home.html")

    else:
        return redirect(url_for('auth.login'))


@views.route("/values/<currency>")
def values(currency):
    if 'loggedin' in session:
        model = tf.keras.models.load_model('.\website\saved_model\my_model')
        opening_model = tf.keras.models.load_model(
            '.\website\saved_model2\my_model5')
        scaler = joblib.load(".\website\scaler.save")
        scaler2 = joblib.load(".\website\scaler2.save")
        opening_scaler = joblib.load(".\website\openingscaler.save")
        opening_scaler2 = joblib.load(".\website\openingscaler2.save")
        if(currency == "eth"):
            GetInformation = yahooFinance.Ticker("ETH-USD")
            input = GetInformation.history(period="150d")
        else:
            GetInformation = yahooFinance.Ticker("BTC-USD")
            input = GetInformation.history(period="150d")
        last_date = input.index[-1]
        dates = pd.date_range(
            start=last_date+datetime.timedelta(days=1), periods=30)
        dates = np.array(dates)
        dates = np.reshape(dates, (30,))
        dates = np.datetime_as_string(dates)
        result = input.to_json(orient="index", date_format='iso')
        parsed = json.loads(result)           # YA TERA 150 KA JSON HA
        json.dumps(parsed)
        input_new = scaler.transform(input.iloc[:, 0:5].values)
        tomorrow_result = scaler2.inverse_transform(
            model.predict(input_new.reshape(-1, 150, 5))).reshape(1,)
        print(tomorrow_result)

        # upto here i am having daily prediction and add try catch for the case we are having not able to fetch data from api
        input_new_opening = opening_scaler.transform(input.iloc[:, [0]].values)
        prediction_array = []
        predict_for = 30
        for i in range(0, predict_for):
            tomorrow_prediction = opening_model.predict(
                input_new_opening.reshape(-1, 150, 1))
            prediction_array.append(
                (opening_scaler2.inverse_transform(tomorrow_prediction)))

            input_new_opening = np.delete(input_new_opening, 0, axis=0)
            input_new_opening = np.append(
                input_new_opening, tomorrow_prediction, axis=0)

        prediction_array = np.array(prediction_array)
        prediction_array = np.reshape(prediction_array, (30,))
        prediction_array = prediction_array.tolist()
        dictionary = dict(zip(dates, prediction_array))

        #json_prediction =json.dumps(dictionary)
        jsonify(dictionary)
        return({"previous": parsed, "predictions": dictionary})

    else:
        return redirect(url_for('auth.login'))
