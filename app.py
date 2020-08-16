from flask import Flask, make_response, request, jsonify, render_template, send_file
import io
import csv
import pickle
import numpy as np
from flask_cors import cross_origin
import pandas as pd
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
model = pickle.load(open('batch_.pickle', 'rb'))
model1 =pickle.load(open("zz.pickle", "rb"))


@app.route('/')
def home():
    return render_template('H.html')

@app.route('/d.html', methods = ['GET', 'POST'])
def single():
    return render_template('d.html')


@app.route('/transform', methods=["POST"])
def batch_view():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('File Not Uploaded')
            return render_template('B.html')
        f = request.files['file']
        if f.filename == '':
            print('No File')
            return render_template('B.html')
        else:
            filename = secure_filename(f.filename)
            f.save(filename)
            print('File uploaded successfully')
        input_df = pd.read_csv(f.filename)
        result_df = input_df.copy()
        input_df['MONTH'] = input_df["MONTH"]
        input_df['DAY'] = input_df["DAY"]
        input_df['DAY_OF_WEEK'] = input_df["DAY_OF_WEEK"]
        input_df['AIRLINE'] = input_df["AIRLINE"]
        input_df['SCHEDULED_DEPARTURE'] = input_df["SCHEDULED_DEPARTURE"]
        input_df['DEPARTURE_TIME'] = input_df["DEPARTURE_TIME"]
        input_df['TAXI_OUT'] = input_df["TAXI_OUT"]
        input_df['DISTANCE'] = input_df["DISTANCE"]
        input_df['TAXI_IN'] = input_df["TAXI_IN"]
        input_df['SCHEDULED_ARRIVAL'] = input_df["SCHEDULED_ARRIVAL"]
        input_df['ARRIVAL_DELAY'] = input_df["ARRIVAL_DELAY"]
        input_predict = model.predict(input_df)
        result_df['Result'] = input_predict
        result_df['Result_Description'] = result_df['Result']
        print(result_df)
        print(result_df['AIRLINE'])
        result_df.to_csv('Prediction.csv')
        return redirect('/downloadfile/' + 'Prediction.csv')

    return render_template('B.html')

@app.route('/downloadfile/<filename>', methods =['GET'])
def download_file(filename):
    return render_template('Down.html', value = filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route('/B.html', methods = ['GET','POST'])
def batch():
    return render_template('B.html')

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        MONTH = int(request.form["MONTH"])
        DAY = int(request.form["DAY"])
        DAY_OF_WEEK = int(request.form["DAY_OF_WEEK"])
        AIRLINE = float(request.form["AIRLINE"])
        SCHEDULED_DEPARTURE = float(request.form["SCHEDULED_DEPARTURE"])
        DEPARTURE_TIME = float(request.form["DEPARTURE_TIME"])
        TAXI_OUT = float(request.form["TAXI_OUT"])
        DISTANCE = int(request.form["DISTANCE"])
        TAXI_IN = float(request.form["TAXI_IN"])
        SCHEDULED_ARRIVAL = float(request.form["SCHEDULED_ARRIVAL"])
        ARRIVAL_DELAY = float(request.form["ARRIVAL_DELAY"])

       

        prediction=model.predict([[
            MONTH,
            DAY,
            DAY_OF_WEEK,
            AIRLINE,
            SCHEDULED_DEPARTURE,
            DEPARTURE_TIME,
            TAXI_OUT,
            DISTANCE,
            TAXI_IN,
            SCHEDULED_ARRIVAL,
            ARRIVAL_DELAY
        ]])

        output = round(prediction[0], 2)

        return render_template('d.html', prediction_text="Airline Delay Should Be in min. {}".format(output))

    return render_template('d.html')





if __name__ == "__main__":
    app.run(debug=True)
