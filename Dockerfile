FROM public.ecr.aws/lambda/python:3.10

# Copy requirements.txt file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy src dir to LAMBDA_TASK_ROOT
COPY src ${LAMBDA_TASK_ROOT}/src

# Install the requirements
RUN pip install -r requirements.txt

ENV EMAIL_SENDER=contacto.tenderi@gmail.com
ENV EMAIL_PASSWORD=yidnjehemtzjqkdk

# Set the CMD to the handler 
CMD [ "src.handler.send_verification_email" ]
