from flask import Flask, request, render_template
import requests
import pandas as pd
import numpy as np 
import pickle

app = Flask(__name__)
pickle_in = open('model_GB.pkl', 'rb')
model = pickle.load(pickle_in)

@app.route('/', methods =['GET'])
def Home():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def refresh():
    return render_template('index.html')

@app.route('/predict', methods =['POST'])
def predict():
    if request.method == 'POST':

        #Sex
        sex = request.form['sex']
        if (sex == '1'):
            sex = 1.0
        else:
            sex = 0.0

        #Chest Pain
        cp = request.form['cp']
        if (cp == '0'):
            cp = 0.0
        elif (cp=='1'):
            cp = 0.33333
        elif (cp=='2'):
            cp = 0.66667
        else:
            cp = 1.0

        #Exercise Induced Angina
        exeng = request.form['exeng']
        if (exeng == '1'):
            exeng = 1.0
        else:
            exeng = 0.0

        #Maximum Heart Rate
        th = float(request.form['thalachh'])
        thalachh = (th - 71.0) / (202.0 - 71.0)

        #Previous Peak
        old = float(request.form['oldpeak'])
        oldpeak = (old - 0.0) / (6.2 - 0.0)

        #Slope
        slp = request.form['slp']
        if (slp == '0'):
            slp = 0.0
        elif (slp == '1'):
            slp = 0.5
        else:
            slp = 1.0

        #Number of Major Vessels
        caa = request.form['caa']
        if (caa == '0'):
            caa = 0.00
        elif (caa == '1'):
            caa = 0.25
        elif (caa == '2'):
            caa = 0.50
        elif (caa == '3'):
            caa = 0.75
        else:
            caa = 1.00

        #Thalium Stress Test result
        thall = request.form['thall'] 
        if (thall == '0'):
            thall = 0.0
        elif (thall=='1'):
            thall = 0.33333
        elif (thall=='2'):
            thall = 0.66667
        else:
            thall = 1.0


        prediction = model.predict([[sex,cp,thalachh, exeng,oldpeak,slp,caa,thall]])
        prob = model.predict_proba([[sex,cp,thalachh, exeng,oldpeak,slp,caa,thall]])
        prob_out = int(round(prob[0][1]*100,0))
        output=round(prediction[0],2)
        if output==0.0:
            return render_template('index.html',prediction_text="Less Chances of Heart Attack {}%".format(prob_out))
        else:
            return render_template('index.html',prediction_text="High Chances of Heart Attack {}%".format(prob_out))

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)

