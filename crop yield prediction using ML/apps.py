from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':

        Crop_Year=int(request.form['Crop_Year'])
        Area=int(request.form['Area'])
        Temperature=int(request.form['Temperature'])
        Precipitaion=int(request.form['Precipitaion'])
        Humidity=int(request.form['Humidity'])

        Soil_type=request.form['Soil_type']
        s_type=['chalky','clay','loamy','peaty','sandy','silt','silty']
        s_type_num=[]
        for i in s_type:
            if(i==Soil_type):
                s_type_num.append(1)
            else:
                s_type_num.append(0)
        
        District=request.form['District']

        d_type=['ADILABAD','WARANGAL','KARIMNAGAR','KHAMMAM','MEDAK','MAHABOOBNAGAR','RANGAREDDY','NALGONDA','NIZAMABAD','HYDERABAD']
        d_type_num=[]
        for i in d_type:
            if(i==District):
                d_type_num.append(1)
            else:
                d_type_num.append(0)
        
        Crop=request.form['Crop']
        c_type=['Cotton','Jowar','Wheat']
        c_type_num=[]
        for i in c_type:
            if(i==Crop):
                c_type_num.append(1)
            else:
                c_type_num.append(0)

        Season=request.form['Season']
        se_type=['Kharif','Rabi']
        se_type_num=[]
        for i in se_type:
            if(i==Season):
                se_type_num.append(1)
            else:
                se_type_num.append(0)
        
        

        vishnu=[Crop_Year,Area,Temperature,Precipitaion,Humidity]
        for i in s_type_num:
            vishnu.append(i)
        for i in d_type_num:
            vishnu.append(i)
        for i in c_type_num:
            vishnu.append(i)
        for i in se_type_num:
            vishnu.append(i)
        

        prediction=model.predict([vishnu])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="No proper Yeild")
        else:
            return render_template('index.html',prediction_text="Yield {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
