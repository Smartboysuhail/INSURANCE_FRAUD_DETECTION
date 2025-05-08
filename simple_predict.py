import pandas as pd
import numpy as np
import os
from file_methods.file_operations import File_Operation
from preprocessing.preprocessor import Preprocessor

class SimplePredictor:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir

    def predict(self, input_csv, output_csv='Predictions.csv'):
        # Load data
        data = pd.read_csv(input_csv)
        
        # Remove label column if present
        if 'fraud_reported' in data.columns:
            data = data.drop('fraud_reported', axis=1)
        
        # Remove columns not needed for prediction
        drop_cols = [
            'policy_number','policy_bind_date','policy_state','insured_zip','incident_location',
            'incident_date','incident_state','incident_city','insured_hobbies','auto_make',
            'auto_model','auto_year','age','total_claim_amount'
        ]
        data = data.drop([col for col in drop_cols if col in data.columns], axis=1)
        
        # Replace '?' with np.nan
        data.replace('?', np.nan, inplace=True)
        
        # Preprocessing
        preprocessor = Preprocessor(None, None)
        is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)
        if is_null_present:
            data = preprocessor.impute_missing_values(data, cols_with_missing_values)

        # After imputation, before encoding
        if 'policy_csl' in data.columns:
            csl_map = {val: idx+1 for idx, val in enumerate(data['policy_csl'].unique())}
            data['policy_csl'] = data['policy_csl'].map(csl_map)

        data = preprocessor.encode_categorical_columns(data)

        # Now, only convert columns that are still object to numeric if you expect them to be numeric
        for col in data.columns:
            if data[col].dtype == 'object':
                print(f"WARNING: Column {col} is still object after encoding. Consider checking your data or encoding logic.")

        # Drop rows with NaNs
        data = data.dropna().reset_index(drop=True)
        data = preprocessor.scale_numerical_columns(data)
        
        # Load KMeans and assign clusters
        file_loader = File_Operation()
        kmeans = file_loader.load_model('KMeans/KMeans.sav')
        clusters = kmeans.predict(data)
        data['clusters'] = clusters
        
        # Predict for each cluster
        predictions = []
        for i in data['clusters'].unique():
            cluster_data = data[data['clusters'] == i].drop('clusters', axis=1)
            model_path = file_loader.find_correct_model_file(str(i))
            model = file_loader.load_model(model_path)
            result = model.predict(cluster_data)
            predictions.extend(['Y' if r else 'N' for r in result])
        
        # Save predictions
        pd.DataFrame({'Predictions': predictions}).to_csv(output_csv, index=False)
        print(f"Predictions saved to {output_csv}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python simple_predict.py <input_csv> [output_csv]")
    else:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2] if len(sys.argv) > 2 else 'Predictions.csv'
        predictor = SimplePredictor()
        predictor.predict(input_csv, output_csv)
