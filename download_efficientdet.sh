#!/usr/bin/env bash

MODEL_ZIP=efficientdet_d0_coco17_tpu-32.tar.gz

curl http://download.tensorflow.org/models/object_detection/tf2/20200711/$MODEL_ZIP \
--output ./models/$MODEL_ZIP

tar -xzvf models/$MODEL_ZIP --directory models
rm models/$MODEL_ZIP