FROM public.ecr.aws/lambda/python:3.9

RUN pip install numpy scipy scikit-learn -t /var/task/

COPY lambda/lambda_function.py /var/task/
COPY lambda/lr_model.pkl /var/task/
COPY lambda/scaler.pkl /var/task/

CMD ["lambda_function.lambda_handler"]