     from sklearn.model_selection import StratifiedKFold
     import numpy as np

     def cross_validate_model(model, data, labels, num_folds=5):
         skf = StratifiedKFold(n_splits=num_folds)
         for train_index, val_index in skf.split(data, labels):
             train_data, val_data = data[train_index], data[val_index]
             train_labels, val_labels = labels[train_index], labels[val_index]
             
             model.fit(train_data, train_labels, validation_data=(val_data, val_labels), epochs=10)
             
             val_loss, val_accuracy = model.evaluate(val_data, val_labels)
             print(f'Validation Loss: {val_loss}, Validation Accuracy: {val_accuracy}')