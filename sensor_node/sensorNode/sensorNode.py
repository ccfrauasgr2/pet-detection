import os
import cv2
import argparse
import time
from itertools import count
from datetime import datetime

from camera import Camera
from detection import Detection, NoBoundingBoxDetected
from network import Network
from package import Package
from compress import Compress


def execute(args, camera, detection, network, item):
    image = camera.take_image()
    #results = detection.make_prediction("input/cats-dogs-portrait-2-63f366aae3884c8ca21c890cf0b89754.jpg")
    results = detection.make_prediction(image)
    package = Package(image=results[0].orig_img, date=datetime.today().strftime('%Y-%m-%d'), time=datetime.today().strftime('%H:%M:%S'), detections=results)
    json = package.toJson()
    network.sendPost(Compress.compress_zip(json), args.debug)
    
    
    if args.debug:
        cv2.imwrite(f"output/{item}.JPG",package.image)
    

def main(args):
    if not os.path.isfile(args.model):
        print(f"No Model in {args.model}")
        return 
    camera = Camera()
    detection = Detection(args.model, args.conf)
    network = Network(queue_lenght=args.queue, url=args.url)
    
    for item in count():        
        start = time.time()
        try:
            execute(args, camera, detection, network, item)
            print(f"Run: {item}")
            
        except NoBoundingBoxDetected:
            print(f"On Image: {item} could no animal be detected")
        except ValueError as e:
            print(f"ValueError: {e}")
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Application will be stopped")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
        end = time.time()
        print(f"Lap time: {end - start}")
        if args.single:
            break
            
    camera.stop_camera()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='SensorNode',
                                     description='Detect Cats and Dogs')
    parser.add_argument('--model',default='model/best.pt', help="Path To Model",type=str)
    parser.add_argument('--url',default='http://192.168.178.201/mongo/input', help="URL to server",type=str )
    parser.add_argument('--conf', help="Lowest level of detection rate", type=float, default=0.5)
    parser.add_argument('--queue',default=1, help="Number of Images before it get send", type=int )
    parser.add_argument('--debug', help="Image should be saved", action='store_true')
    parser.add_argument('--single', help="Only a Single image will be processed", action='store_true')
    main(parser.parse_args())
