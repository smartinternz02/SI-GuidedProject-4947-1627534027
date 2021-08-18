import requests
import json
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "paD8u8ActrqO6ixYNvsWML16VmmgefugiTnEFc5-m1JB"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    float_features = [float(x) for x in request.form.values()]
    final_features = [np.array(float_features)]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [["layer_height","wall_thickness","infill_density","infill_pattern","nozzle_temperature","bed_temperature","print_speed",
    "fan_speed","roughness","tension_strenght","elongation"]], "values": [final_features]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2a9c6f3b-571c-4d27-89a6-affc5668f967/predictions?version=2021-08-12', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    pred=predictions['predictions'][0]['values'][0][0]
    print(pred)

    return render_template('index.html', prediction_text='Material: {}'.format(pred))

if __name__=="__main__":
    #port = int(os.getenv('PORT', 8080))
    #app.run(host='0.0.0.0', port=port, debug=False)
    app.run(debug=False)