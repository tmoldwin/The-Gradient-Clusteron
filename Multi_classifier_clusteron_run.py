"""
Clusteron  multiclassifier
"""
from Multi_classifier_for_clusteron import MultiClassifier as clstrn_multi

num_of_epochs = 2

multiclassifier = clstrn_multi()
multiclassifier.train(num_of_epochs)
