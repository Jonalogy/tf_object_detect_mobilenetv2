#!/usr/bin/env bash

WORK_DIR=$1
MODEL_PATH=$WORK_DIR/model
MODEL_ZIP=ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz

if [ ! -d $MODEL_PATH ]; then
mkdir $MODEL_PATH
fi

curl http://download.tensorflow.org/models/object_detection/tf2/20200711/$MODEL_ZIP \
--output $MODEL_PATH/$MODEL_ZIP

tar -xzvf $MODEL_PATH/$MODEL_ZIP --directory $MODEL_PATH
rm $MODEL_PATH/$MODEL_ZIP