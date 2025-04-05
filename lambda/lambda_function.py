import json
import pickle
import numpy as np

with open('lr_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    features = [
        body['age'], body['job'], body['marital'], body['education'],
        body['default'], body['housing'], body['loan'],
        body['contact'], body['month'], body['day_of_week'], body['poutcome'],
        body['campaign'], body['pdays'], body['previous'], body['emp.var.rate'],
        body['cons.price.idx'], body['cons.conf.idx'], body['euribor3m'], body['nr.employed']
    ]
    
    features_array = np.array([features], dtype=float)
    features_scaled = scaler.transform(features_array)
    
    prediction = model.predict(features_scaled)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': 'yes' if prediction[0] == 1 else 'no'})
    }