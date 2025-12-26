# ML_Pipeline: Customer Retention Prediction API

## Overview

ML_Pipeline is a comprehensive machine learning API service built with Django and Django REST Framework for customer retention prediction. The system provides a production-ready ML pipeline that supports multiple algorithms, A/B testing, batch predictions, and model management.

## Architecture

For detailed information about the system architecture, component interactions, data flows, and design patterns, see [ARCHITECTURE.md](ARCHITECTURE.md).

### Quick Architecture Overview

The application follows a modular architecture with the following key components:

#### 1. Django Backend (`backend/server/`)
- **Django REST Framework**: Provides RESTful API endpoints
- **SQLite Database**: Stores endpoints, algorithms, requests, and A/B test data
- **ML Registry**: Manages ML algorithm instances and their metadata

#### 2. ML Models (`apps/ml/`)
- **Registry System**: Central registry for managing ML algorithms
- **Classifier Implementations**: Individual classifier classes (Random Forest, Extra Trees, Decision Tree)
- **Preprocessing/Postprocessing**: Data transformation pipelines

#### 3. API Endpoints (`apps/endpoints/`)
- **Model Management**: CRUD operations for endpoints and algorithms
- **Prediction Service**: Real-time prediction endpoints
- **A/B Testing**: Automated testing between algorithms
- **Batch Processing**: CSV-based batch predictions

#### 4. Research (`research/`)
- **Training Notebooks**: Jupyter notebooks for model development
- **Trained Models**: Serialized joblib models
- **Data Processing**: Training data preparation and preprocessing

### Data Flow

1. **Model Training** (Research Phase):
   - Data preprocessing in Jupyter notebooks
   - Model training and evaluation
   - Model serialization with joblib

2. **Model Registration** (WSGI Initialization):
   - Algorithms loaded into ML registry
   - Database entries created for tracking

3. **API Requests**:
   - Client sends prediction request
   - Registry selects appropriate algorithm
   - Preprocessing → Prediction → Postprocessing
   - Response returned with prediction and metadata

4. **A/B Testing**:
   - Two algorithms compared in production
   - Requests randomly distributed
   - Accuracy calculated from user feedback
   - Winner promoted to production

## How the Code Works

### Core Classes and Models

#### Database Models (`apps/endpoints/models.py`)

- **Endpoint**: Represents ML API endpoints (e.g., "classifier")
- **MLAlgorithm**: Stores algorithm metadata, code, and version info
- **MLAlgorithmStatus**: Tracks algorithm lifecycle (testing → staging → production)
- **MLRequest**: Logs all prediction requests and responses
- **ABTest**: Manages A/B testing between algorithms

#### ML Registry (`apps/ml/registry.py`)

```python
class MLRegistry:
    def __init__(self):
        self.endpoints = {}  # Stores algorithm instances by ID
    
    def add_algorithm(self, endpoint_name, algorithm_object, ...):
        # Creates database entries and stores algorithm instance
```

#### Classifier Classes (`apps/ml/classifier/`)

Each classifier follows the same pattern:

```python
class RandomForestClassifier:
    def __init__(self):
        # Load trained model and preprocessing artifacts
        self.model = joblib.load("random_forest.joblib")
        self.values_fill_missing = joblib.load("train_mode.joblib")
    
    def compute_prediction(self, input_data):
        input_data = self.preprocessing(input_data)
        prediction = self.predict(input_data)
        return self.postprocessing(prediction)
```

### Prediction Flow

1. **API Request** (`PredictView.post()`):
   - Receives JSON input data
   - Queries active algorithms by endpoint/status/version
   - For A/B testing: randomly selects between two algorithms

2. **Algorithm Execution**:
   - `preprocessing()`: Converts JSON to DataFrame, handles missing values
   - `predict()`: Calls sklearn's `predict_proba()`
   - `postprocessing()`: Converts probabilities to labels

3. **Response & Logging**:
   - Returns prediction with probability and label
   - Creates `MLRequest` record for tracking

### A/B Testing Implementation

- **Start Test**: Creates `ABTest` record, sets both algorithms to "ab_testing" status
- **Request Distribution**: 50/50 random split between algorithms
- **Stop Test**: Calculates accuracy from user feedback, promotes winner to production

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Navigate to project directory**:
   ```bash
   cd ML_Pipe
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   
   **Windows (Command Prompt)**:
   ```cmd
   venv\Scripts\activate
   ```
   
   **Windows (PowerShell)**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Navigate to Django project**:
   ```bash
   cd backend\server
   ```

6. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Start the server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Usage

### Base URL
```
http://127.0.0.1:8000/api/v1/
```

### Available Endpoints

#### 1. List Endpoints
```http
GET /api/v1/endpoints
```

#### 2. List ML Algorithms
```http
GET /api/v1/mlalgorithms
```

#### 3. Make Prediction
```http
POST /api/v1/{endpoint_name}/predict
```

**Example Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/classifier/predict \
  -H "Content-Type: application/json" \
  -d '{
    "feature1": 1.0,
    "feature2": 0.5,
    "feature3": 100
  }'
```

**Query Parameters**:
- `status`: Algorithm status (testing, production, ab_testing) - default: testing
- `version`: Specific algorithm version

#### 4. Batch Prediction
```http
POST /api/v1/batch-predict
Content-Type: multipart/form-data
```

Upload a CSV file with prediction data.

#### 5. A/B Testing
```http
POST /api/v1/abtests
POST /api/v1/stop_ab_test/{ab_test_id}
```

### Prediction Response Format

```json
{
  "probability": 0.75,
  "label": "1",
  "status": "OK",
  "request_id": 123
}
```

## Model Training

### Training Process

1. **Data Preparation** (`research/Train_Retension_Model.ipynb`):
   - Load processed CSV data
   - Split features and target (`IsRetained`)
   - Train/test split (75/25)

2. **Model Training**:
   - **Random Forest**: 100 estimators
   - **Extra Trees**: 100 estimators  
   - **Decision Tree**: Max 100 leaf nodes

3. **Preprocessing Artifacts**:
   - `train_mode.joblib`: Mode values for missing data imputation
   - Individual model files: `random_forest.joblib`, etc.

### Adding New Models

1. Train model in research notebook
2. Save model with joblib
3. Create classifier class in `apps/ml/classifier/`
4. Register in `server/wsgi.py`
5. Update status via API

## Configuration

### Django Settings (`server/settings.py`)

- **Database**: SQLite (development)
- **Installed Apps**: Django REST Framework, custom apps
- **Security**: DEBUG=True (development only)

### ML Configuration

- **Model Path**: `../../research/` (relative to classifier files)
- **Active Models**: Configured in WSGI initialization
- **Prediction Threshold**: 0.5 (probability > 0.5 → label "1")

## Deployment Considerations

### Production Setup

1. **Database**: Switch to PostgreSQL/MySQL
2. **Settings**: Set DEBUG=False, configure ALLOWED_HOSTS
3. **Static Files**: Configure static file serving
4. **Security**: Use environment variables for secrets
5. **Scaling**: Consider using Redis for caching, load balancer

### Model Updates

- Implement model versioning
- Use CI/CD for automated deployment
- Monitor prediction performance
- Implement model rollback capabilities

## Troubleshooting

### Common Issues

1. **Model Loading Errors**: Check file paths in classifier `__init__`
2. **Database Errors**: Run `python manage.py migrate`
3. **Import Errors**: Ensure virtual environment is activated
4. **Prediction Errors**: Verify input data format matches training data

### Logs

- Django logs: Console output during `runserver`
- Request logs: Stored in `MLRequest` model
- Error handling: Try/catch blocks return error messages

## Contributing

1. Follow Django best practices
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages

## License

