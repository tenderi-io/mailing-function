docker-login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 681839224497.dkr.ecr.us-east-1.amazonaws.com

docker-image:
	pipenv run pip freeze > requirements.txt && docker build -t mailing-service:test . && rm requirements.txt

docker-clean:
	docker stop mailing  && docker rm mailing

docker-run:
	docker run -d -p 9000:8080 --name mailing mailing-service:test

docker-all:
	make docker-image && make docker-clean && make docker-run

test:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"Records":[{"messageId":"059f36b4-87a3-44ab-83d2-661975830a7d","receiptHandle":"AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...","body":{"receiver_email":"info.hazblon@gmail.com","email_type":"VERIFY_ACCOUNT","action_url":"google.com","replacements":{"user_name":"Dulce"}},"attributes":{"ApproximateReceiveCount":"1","SentTimestamp":"1545082649183","SenderId":"AIDAIENQZJOLO23YVJ4VO","ApproximateFirstReceiveTimestamp":"1545082649185"},"messageAttributes":{},"md5OfBody":"098f6bcd4621d373cade4e832627b4f6","eventSource":"aws:sqs","eventSourceARN":"arn:aws:sqs:us-east-1:111122223333:my-queue","awsRegion":"us-east-1"}]}'

invoke: 
	aws lambda invoke --function-name mailing-service --log-type Tail --payload file://request-sapmle.json outputfile.txt --output text --cli-binary-format raw-in-base64-out

deploy: 
	docker tag mailing-service:test 681839224497.dkr.ecr.us-east-1.amazonaws.com/tenderi-services:latest && docker push 681839224497.dkr.ecr.us-east-1.amazonaws.com/tenderi-services:latest  

lambda-update:
	aws lambda update-function-code --function-name mailing-service --image-uri 681839224497.dkr.ecr.us-east-1.amazonaws.com/tenderi-services:latest
