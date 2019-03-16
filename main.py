import argparse
from scripts.detect_object import detect_object

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", type=str, required=False, default="models/MobileNetSSD_deploy.prototxt.txt",
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", type=str, required=False, default="models/MobileNetSSD_deploy.caffemodel",
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.3, required=False,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

detect_object(args["prototxt"], args["model"], args["confidence"])
