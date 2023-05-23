import os
from sklearn.metrics import average_precision_score

def calculate_top1_accuracy(target_folder, test_folder):
    target_files = os.listdir(target_folder)
    test_files = os.listdir(test_folder)

    total_samples = min(len(target_files), len(test_files))
    correct_count = 0

    for i in range(total_samples):
        target_file = os.path.join(target_folder, target_files[i])
        test_file = os.path.join(test_folder, test_files[i])

        with open(target_file, 'r') as f1, open(test_file, 'r') as f2:
            target_lines = f1.readlines()
            test_lines = f2.readlines()

        target_predictions = [line.strip()[0] for line in target_lines]
        test_predictions = [line.strip()[0] for line in test_lines]

        correct_count += sum(t_pred == test_pred for t_pred, test_pred in zip(target_predictions, test_predictions))

    top1_accuracy = (correct_count / total_samples) * 100
    return top1_accuracy

def calculate_mAP(target_folder, test_folder):
    target_files = os.listdir(target_folder)
    test_files = os.listdir(test_folder)

    common_files = set(target_files).intersection(test_files)
    all_targets = []
    all_predictions = []

    for file in common_files:
        target_file = os.path.join(target_folder, file)
        test_file = os.path.join(test_folder, file)
        count_target_lines = 0
        
        with open(target_file, 'r') as f1, open(test_file, 'r') as f2:
            target_lines = f1.readlines()
            test_lines = f2.readlines()
        if len(test_lines) > len(target_lines):
            continue
        if len(test_lines) < len(target_lines):
            count_target_lines = len(target_lines)
            test_labels = [0] * count_target_lines
        else:
            test_labels = [int(line.strip()[0]) for line in test_lines if line.strip()]
            
        target_labels = [int(line.strip()[0]) for line in target_lines if line.strip()]
        
        #print(f"target: {target_labels} test: {test_labels}")
        all_targets.extend(target_labels)
        all_predictions.extend(test_labels)

    mAP = average_precision_score(all_targets, all_predictions, pos_label=1)
    return mAP

# CHANGE DIR
target_folder_path = 'D:/A_Master/1. Semester/Cloud Computing/results/target' #path/to/correct/labels
test_folder_path = 'D:/A_Master/1. Semester/Cloud Computing/results/predict/labels' #path/to/labels/from/testing

# TOP 1 ACCURACY
accuracy = calculate_top1_accuracy(target_folder_path, test_folder_path)
print(f'Top-1-Accuracy: {accuracy:.2f}%')

# mAP
mAP = calculate_mAP(target_folder_path, test_folder_path)
print(f'mAP: {mAP:.5f}')
