from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("gpt-RF.pkl", "rb"))

models = {
    "gpt-CatBoost": pickle.load(open("gpt-CatBoost.pkl", "rb")),
    "gpt-XGB": pickle.load(open("gpt-XGB.pkl", "rb")),
    "gpt-DT": pickle.load(open("gpt-DT.pkl", "rb")),
    "gpt-Lasso": pickle.load(open("gpt-Lasso.pkl", "rb")),
    "gpt-Ridge": pickle.load(open("gpt-Ridge.pkl", "rb")),
    "gpt-LR": pickle.load(open("gpt-LR.pkl", "rb")),
    "gpt-RF": pickle.load(open("gpt-RF.pkl", "rb")),
}

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == 'POST':
        ## time of departure 
        if request.form["departure_time"] == "Morning":
            d_Morning = 1
            d_Early_Morning = 0
            d_Afternoon = 0
            d_Evening = 0
            d_Night = 0
            d_Late_Night = 0
        elif request.form["departure_time"] == "Early_Morning":
            d_Early_Morning = 1
            d_Morning = 0
            d_Afternoon = 0
            d_Evening = 0
            d_Night = 0
            d_Late_Night = 0
            
        elif request.form["departure_time"] == "Afternoon":
            d_Afternoon = 1
            d_Morning = 0
            d_Early_Morning = 0
            d_Evening = 0
            d_Night = 0
            d_Late_Night = 0
            
        elif request.form["departure_time"] == "Evening":
            d_Evening = 1
            d_Morning = 0
            d_Early_Morning = 0
            d_Afternoon = 0
            d_Night = 0
            d_Late_Night = 0
            
        elif request.form["departure_time"] == "Night":
            d_Night = 1
            d_Morning = 0
            d_Early_Morning = 0
            d_Afternoon = 0
            d_Evening = 0
            d_Late_Night = 0
            
        else:
            d_Late_Night = 1
            d_Morning = 0
            d_Early_Morning = 0
            d_Afternoon = 0
            d_Evening = 0
            d_Night = 0
            
        ## arrival time
        
        if request.form["arrival_time"] == "Morning":
            a_Morning = 1
            a_Early_Morning = 0
            a_Afternoon = 0
            a_Evening = 0
            a_Night = 0
            a_Late_Night = 0
        elif request.form["arrival_time"] == "Early_Morning":
            a_Early_Morning = 1
            a_Morning = 0
            a_Afternoon = 0
            a_Evening = 0
            a_Night = 0
            a_Late_Night = 0
        elif request.form["arrival_time"] == "Afternoon":
            a_Afternoon = 1
            a_Morning = 0
            a_Early_Morning = 0
            a_Evening = 0
            a_Night = 0
            a_Late_Night = 0
        elif request.form["arrival_time"] == "Evening":
            a_Evening = 1
            a_Morning = 0
            a_Early_Morning = 0
            a_Afternoon = 0
            a_Night = 0
            a_Late_Night = 0
        elif request.form["arrival_time"] == "Night":
            a_Night = 1
            a_Morning = 0
            a_Early_Morning = 0
            a_Afternoon = 0
            a_Evening = 0
            a_Late_Night = 0
        else:
            a_Late_Night = 1
            a_Morning = 0
            a_Early_Morning = 0
            a_Afternoon = 0
            a_Evening = 0
            a_Night = 0
            
            
            
               
        
        ## stops
        stops = request.form["stops"]
        
        ## stops are in the range of 0 to 2
        if int(stops) <= 2:
            stops = int(stops)
        else:
            stops = 2
            
        
        ## duration
        duration = request.form["duration"]  
        duration = float(duration)
        
        
        ## flight class
        if request.form["flight_class"] == "Economy":
            flight_class = 1
        else:
            flight_class = 0
        
        ## airline
        
        if request.form["airline"] == "Air_India":
            Air_India = 1
            Vistara = 0
            Indigo = 0
            AirAsia = 0
            SpiceJet = 0
            GO_FIRST = 0
            
        elif request.form["airline"] == "Vistara":
            Vistara = 1
            Air_India = 0
            Indigo = 0
            AirAsia = 0
            SpiceJet = 0
            GO_FIRST = 0
            
        elif request.form["airline"] == "Indigo":
            Indigo = 1
            Air_India = 0
            Vistara = 0
            AirAsia = 0
            SpiceJet = 0
            GO_FIRST = 0
            
        elif request.form["airline"] == "AirAsia":
            AirAsia = 1
            Air_India = 0
            Vistara = 0
            Indigo = 0
            SpiceJet = 0
            GO_FIRST = 0
            
        elif request.form["airline"] == "SpiceJet":
            SpiceJet = 1
            Air_India = 0
            Vistara = 0
            Indigo = 0
            AirAsia = 0
            GO_FIRST = 0
            
        else:
            GO_FIRST = 1
            Air_India = 0
            Vistara = 0
            Indigo = 0
            AirAsia = 0
            SpiceJet = 0
            
            
        ## source 
        
        if request.form["source"] == "Delhi":
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Bangalore = 0
            s_Hyderabad = 0
            
        elif request.form["source"] == "Kolkata":
            s_Kolkata = 1
            s_Delhi = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Bangalore = 0
            s_Hyderabad = 0
            
        elif request.form["source"] == "Mumbai":
            s_Mumbai = 1
            s_Delhi = 0
            s_Kolkata = 0
            s_Chennai = 0
            s_Bangalore = 0
            s_Hyderabad = 0
            
        elif request.form["source"] == "Chennai":
            s_Chennai = 1
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Bangalore = 0
            s_Hyderabad = 0
            
        elif request.form["source"] == "Bangalore":
            s_Bangalore = 1
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Hyderabad = 0
            
        else:
            s_Hyderabad = 1
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Bangalore = 0
            
        ## destination
           
        if request.form["destination"] == "Delhi":
            d_Delhi = 1
            d_Kolkata = 0
            d_Mumbai = 0
            d_Chennai = 0
            d_Bangalore = 0
            d_Hyderabad = 0
            
        elif request.form["destination"] == "Kolkata":
            d_Kolkata = 1
            d_Delhi = 0
            d_Mumbai = 0
            d_Chennai = 0
            d_Bangalore = 0
            d_Hyderabad = 0
            
        elif request.form["destination"] == "Mumbai":
            d_Mumbai = 1
            d_Delhi = 0
            d_Kolkata = 0
            d_Chennai = 0
            d_Bangalore = 0
            d_Hyderabad = 0
            
        elif request.form["destination"] == "Chennai":
            d_Chennai = 1
            d_Delhi = 0
            d_Kolkata = 0
            d_Mumbai = 0
            d_Bangalore = 0
            d_Hyderabad = 0
            
        elif request.form["destination"] == "Bangalore":
            d_Bangalore = 1
            d_Delhi = 0
            d_Kolkata = 0
            d_Mumbai = 0
            d_Chennai = 0
            d_Hyderabad = 0
            
        else:
            d_Hyderabad = 1
            d_Delhi = 0
            d_Kolkata = 0
            d_Mumbai = 0
            d_Chennai = 0
            d_Bangalore = 0
       
            
        ## days_left
        
        days_left = request.form["days_left"]
        
        ## in the dataset in the column "days_left" the values are in the range of 0 to 49
        
        if int(days_left) <= 49:
            days_left = int(days_left)
        else:
            days_left = 49
        
            
        prediction=model.predict([[d_Morning, d_Early_Morning, d_Afternoon, d_Evening, d_Night, d_Late_Night,
                                   a_Morning, a_Early_Morning, a_Afternoon, a_Evening, a_Night, a_Late_Night,
                                   stops, duration, flight_class, Air_India, Vistara, Indigo, AirAsia, SpiceJet, GO_FIRST,
                                   s_Delhi, s_Kolkata, s_Mumbai, s_Chennai, s_Bangalore, s_Hyderabad,
                                   d_Delhi, d_Kolkata, d_Mumbai, d_Chennai, d_Bangalore, d_Hyderabad, days_left]])
        
        output=round(prediction[0],2)
        
        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))
    
    return render_template("home.html")        

if __name__ == "__main__":
    app.run(debug=True)
    
    
        
        