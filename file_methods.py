import os
import json
import pickle

class File_Operation:
    def __init__(self):
        self.model_directory = 'models'
      
    def load_model(self, filename):
        try:
            # If filename is already a full path, use it directly
            if os.path.isabs(filename) or os.path.exists(filename):
                path = filename
            else:
                # Otherwise, look in the model directory
                path = os.path.join(self.model_directory, filename)
                
            if not os.path.exists(path):
                raise FileNotFoundError(f"Model file not found at {path}")
                
            with open(path, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            raise e

    def find_correct_model_file(self, cluster_number):
        try:
            # Look for model in cluster directory
            cluster_dir = os.path.join(self.model_directory, 'KMeans', f'cluster_{cluster_number}')
            model_path = os.path.join(cluster_dir, 'model.sav')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"No model file found for cluster {cluster_number}")
                
            return model_path
        except Exception as e:
            raise e