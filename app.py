from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('gradient_boosting_regressor_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])

        Brand = request.form['Brand']
        arr_brand = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dict_brand = {'Ashok':0, 'Audi':1, 'BMW':2, 'Chevrolet':3, 'Daewoo':4, 'Datsun':5, 'Fiat':6, 'Force':7, 'Ford':8, 'Honda':9, 'Hyundai':10,
       'Isuzu':11, 'Jaguar':12, 'Jeep':13, 'Kia':14, 'Land':15, 'MG':16, 'Mahindra':17, 'Maruti':18, 'Mercedes-Benz':19,
       'Mitsubishi':20, 'Nissan':21, 'Opel':22, 'Renault':23, 'Skoda':24, 'Tata':25, 'Toyota':26, 'Volkswagen':27, 'Volvo':28}
        arr_brand[dict_brand[Brand]] = 1

        Present_Price=float(request.form['Present_Price'])

        Kms_Driven=int(request.form['Kms_Driven'])

        Owner=int(request.form['Owner'])

        Mileage=float(request.form['Mileage'])

        Engine=int(request.form['Engine'])

        Max_Power=float(request.form['Max_Power'])
        Max_Power1 = np.log(Max_Power)

        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
        else:
            Fuel_Type_Petrol=0

        Year=2021-Year
        Year1 = np.log(Year)

        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trustmark_Dealer=0
        else:
            Seller_Type_Individual=0
            Seller_Type_Trustmark_Dealer=1

        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0

        Seats = request.form['Seats']
        arr_seat = [0,0,0,0,0,0,0]
        dict_seat = {'14':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6}
        arr_seat[dict_seat[Seats]] = 1
        
        scaler = StandardScaler()
        Kms_Driven = scaler.fit_transform([[Kms_Driven]])
        Mileage = scaler.fit_transform([[Mileage]])
        Engine = scaler.fit_transform([[Engine]])
        Max_Power1 = scaler.fit_transform([[Max_Power1]])
        Year1 = scaler.fit_transform([[Year1]])

        temp = [Kms_Driven,Owner,Mileage,Engine,Max_Power1,Year1,Fuel_Type_Petrol,Seller_Type_Individual,
        Seller_Type_Trustmark_Dealer,Transmission_Manual]
        temp.extend(arr_seat)
        temp.extend(arr_brand)

        prediction=model.predict([temp])

        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)