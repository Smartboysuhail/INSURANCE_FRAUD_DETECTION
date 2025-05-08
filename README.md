# Insurance Fraud Detection System

A web-based application for detecting insurance fraud using machine learning.

## Features

- User authentication (register/login)
- Secure file upload
- Real-time fraud detection
- Interactive dashboard
- Detailed prediction results
- User session management

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd insurance-fraud-detection
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Deployment on Render.com

1. Create a free account on [Render.com](https://render.com)

2. Create a new Web Service:
   - Connect your GitHub repository
   - Select "Python" as the runtime
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn app:app`
   - Add environment variables:
     - `PYTHON_VERSION`: 3.9.0
     - `SECRET_KEY`: (generate a secure random key)

3. Deploy!

## Project Structure

```
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── Procfile                 # Deployment configuration
├── templates/               # HTML templates
│   ├── index.html          # Login page
│   ├── register.html       # Registration page
│   └── results.html        # Dashboard page
├── uploads/                # Uploaded files
├── Prediction_Output_File/ # Prediction results
├── file_methods/          # File handling utilities
│   ├── __init__.py
│   └── file_operations.py
├── preprocessing/         # Data preprocessing modules
│   ├── __init__.py
│   └── preprocessor.py
├── EDA/                  # Exploratory Data Analysis
│   ├── __init__.py
│   └── eda_utils.py
├── simple_predict/       # Prediction modules
│   ├── __init__.py
│   └── predictor.py
└── models/              # Trained model files
    └── model.pkl
```

## Required Files for Deployment

Make sure to include these essential files in your GitHub repository:

1. **Core Application Files**:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - All template files in `templates/`

2. **ML and Processing Files**:
   - `file_methods/` directory with all file handling utilities
   - `preprocessing/` directory with data preprocessing modules
   - `EDA/` directory with analysis utilities
   - `simple_predict/` directory with prediction modules
   - `models/` directory with your trained model

3. **Configuration Files**:
   - `.gitignore`
   - `README.md`

## Security Notes

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting
- Add input validation
- Use environment variables for sensitive data
- Keep your trained model secure
- Don't commit sensitive data or API keys

## License

MIT License 