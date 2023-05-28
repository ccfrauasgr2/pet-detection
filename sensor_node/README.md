# Model Training

The Model Training was done with ultralytics' YOLOv8 in a Google Colab notebook.

## Annotation

The annotation for the training images was done with MegaDetector and converted with the `convert_to_yolov8_annotation.py` ([here](https://github.com/ccfrauasgr2/pet-detection/tree/main/sensor_node\model_training)) script.

## Requirements

We used the versions of the following python packages:
- ultralytics v. 8.0.105
- scikit-learn v. 1.2.2

## Results

The results of the training are the model itself `best.pt` ([here](https://github.com/ccfrauasgr2/pet-detection/tree/main/sensor_node/model_training)) and the evaluation of the results either as a table `results.csv` ([here](https://github.com/ccfrauasgr2/pet-detection/tree/main/sensor_node/model_training)) or as plots `results.png` ([here](https://github.com/ccfrauasgr2/pet-detection/tree/main/docs/img)).