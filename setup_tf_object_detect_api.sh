#!/usr/bin/env bash

TF_OD_DIR="$(pwd)/tf_object_detect"

if [ -d $TF_OD_DIR/research/object_detection ]
then
  echo "Tensorflow object detection API already exists"
else
  mkdir $TF_OD_DIR
  echo "Fetching TF Object Detect API"
  git clone --depth 1 https://github.com/tensorflow/models.git $TF_OD_DIR
fi

echo "Changing work directory to ${TF_OD_DIR}/research"
cd $TF_OD_DIR/research
protoc object_detection/protos/*.proto --python_out=. # This next line requires with research dir as the working dir
cp object_detection/packages/tf2/setup.py $TF_OD_DIR/research/setup.py

PATH="$(pwd)/.venv/bin:$PATH"
python -m pip install .

# install OpenCV python package
python -m pip install opencv-python opencv-contrib-python