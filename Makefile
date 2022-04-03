STACK_NAME ?= ffmpeg-python-lambda-layer
STATIC_BUILD_URL ?= https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
AWS_S3_BUCKET ?= aws-sar-ffmpeg-lambda-layer-gyhxw3zp
AWS_REGION ?= us-west-2

clean:
	rm -rf build

build/layer/bin/ffmpeg:
	mkdir -p build/layer/bin
	rm -rf build/ffmpeg*
	cd build && curl $(STATIC_BUILD_URL) | tar x
	mv build/ffmpeg*/ffmpeg build/ffmpeg*/ffprobe build/layer/bin

build/layer/python/ffmpeg:
	mkdir -p build/layer/python
	pip install ffmpeg-python -t build/layer/python

build/output.yaml: template.yaml build/layer/bin/ffmpeg build/layer/python/ffmpeg
	sam package --template-file $< --output-template-file $@ --s3-bucket $(AWS_S3_BUCKET)

publish: build/output.yaml
	sam publish --template $< --region $(AWS_REGION)

deploy: build/output.yaml
	sam deploy --template $< --stack-name $(STACK_NAME)
	aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs --output table
