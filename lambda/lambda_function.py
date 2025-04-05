import json
import pickle
import numpy as np
import boto3
from sklearn.preprocessing import LabelEncoder

with open('lr_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

label_encoders = {}
categorical_columns = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome']

categories = {
    'job': ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'],
    'marital': ['divorced', 'married', 'single', 'unknown'],
    'education': ['basic.4y', 'basic.6y', 'basic.9y', 'high.school', 'illiterate', 'professional.course', 'university.degree', 'unknown'],
    'default': ['no', 'yes', 'unknown'],
    'housing': ['no', 'yes', 'unknown'],
    'loan': ['no', 'yes', 'unknown'],
    'contact': ['cellular', 'telephone', 'unknown'],
    'month': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
    'day_of_week': ['mon', 'tue', 'wed', 'thu', 'fri'],
    'poutcome': ['failure', 'nonexistent', 'success', 'unknown']
}

for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    label_encoders[col].fit(categories[col])

def preprocess_features(body):
    """
    Preprocess the input features: encode categorical variables and handle numerical features.
    """
    features = [
        body['age'],
        body['job'],
        body['marital'],
        body['education'],
        body['default'],
        body['housing'],
        body['loan'],
        body['contact'],
        body['month'],
        body['day_of_week'],
        body['poutcome'],
        body['campaign'],
        body['pdays'],
        body['previous'],
        body['emp.var.rate'],
        body['cons.price.idx'],
        body['cons.conf.idx'],
        body['euribor3m'],
        body['nr.employed']
    ]

    encoded_features = []
    for i, feature in enumerate(features):
        if i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            col_name = categorical_columns[i - 1]
            encoded_feature = label_encoders[col_name].transform([feature])[0]
            encoded_features.append(encoded_feature)
        else:
            encoded_features.append(float(feature))

    return encoded_features

def lambda_handler(event, context):
    if 'CodePipeline.job' in event:
        job_id = event['CodePipeline.job']['id']
        codepipeline = boto3.client('codepipeline')

        try:
            print("Lambda function invoked by CodePipeline")
            codepipeline.put_job_success_result(jobId=job_id)
            return {
                'statusCode': 200,
                'body': json.dumps('Successfully processed by CodePipeline')
            }
        except Exception as e:
            codepipeline.put_job_failure_result(
                jobId=job_id,
                failureDetails={
                    'type': 'JobFailed',
                    'message': str(e)
                }
            )
            raise e
    else:
        try:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']

            features = preprocess_features(body)

            features_array = np.array([features], dtype=float)
            features_scaled = scaler.transform(features_array)

            prediction = model.predict(features_scaled)

            return {
                'statusCode': 200,
                'body': json.dumps({'prediction': 'yes' if prediction[0] == 1 else 'no'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }