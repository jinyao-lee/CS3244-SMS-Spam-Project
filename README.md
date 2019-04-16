# CS3244: SMS Spam Project
CS3244 project - working on SMS spam classifier using K-Nearest Neighbors (k-NN) algorithm.

This repo contains the code used for implmenting k-NN algorithm to classify spam and ham SMS messages from the dataset spam.csv.


File contents list: -

| File  | Details |
| ------------- | ------------- |
| [knn_v2.py](../master/src/knn_v2.py)  | Contains the source code for k-NN implementation. This version randomly shuffles and obtains 20% of training data to be the validation set.|
| [knn_v3.py](../master/src/knn_v3.py)  | Contains the source code for k-NN implementation. This version implements 10-fold cross validation. |
| [Training data](../master/data/spam.csv) | Contains the training data used to classify SMS messages. |
| [Experiment results](../master/data/kValidation%20Results.xlsx) | Contains the experimental accuracy results for classifying messages using k-NN. (Note: x-axis denotes k-value, y-axis denotes validation error) |
