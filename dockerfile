# AWS Lambda Python 3.9 base image එක use කරනවා
FROM public.ecr.aws/lambda/python:3.9

# Dependencies install කරනවා
RUN pip install numpy scipy scikit-learn -t /var/task/

# Lambda function එකයි pickle files ටිකයි copy කරනවා
COPY lambda/lambda_function.py /var/task/
COPY lambda/lr_model.pkl /var/task/
COPY lambda/scaler.pkl /var/task/

# Handler එක set කරනවා
CMD ["lambda_function.lambda_handler"]