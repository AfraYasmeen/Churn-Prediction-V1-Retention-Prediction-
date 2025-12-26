# ML_Pipeline Architecture

## Overview

ML_Pipeline follows a modular, microservice-inspired architecture built on Django, designed for scalable machine learning model deployment and management. The system separates concerns between API management, ML model serving, and research/development workflows.

## System Components

### 1. Django Backend (`backend/server/`)

The core web application layer built with Django and Django REST Framework.

#### Key Components:
- **Django REST Framework**: Provides RESTful API endpoints with serialization
- **SQLite Database**: Stores metadata for endpoints, algorithms, requests, and A/B tests
- **ML Registry**: In-memory registry managing ML algorithm instances and their lifecycle
- **WSGI Application**: Entry point that initializes ML algorithms on startup

#### Responsibilities:
- HTTP request/response handling
- Database operations and data persistence
- API routing and view logic
- Authentication and authorization (extensible)
- Request logging and monitoring

### 2. ML Models Layer (`apps/ml/`)

The machine learning execution layer that encapsulates model logic.

#### Key Components:
- **ML Registry (`registry.py`)**: Central registry for algorithm management
- **Classifier Implementations**: Individual algorithm classes (Random Forest, Extra Trees, Decision Tree)
- **Preprocessing/Postprocessing Pipelines**: Data transformation logic

#### Responsibilities:
- Model loading and initialization
- Input data preprocessing
- ML prediction execution
- Output postprocessing and formatting
- Algorithm versioning and status management

### 3. API Endpoints Layer (`apps/endpoints/`)

The business logic layer handling API operations and domain rules.

#### Key Components:
- **Model Management Views**: CRUD operations for endpoints and algorithms
- **Prediction Service**: Real-time inference endpoints
- **A/B Testing Engine**: Automated algorithm comparison system
- **Batch Processing**: CSV-based bulk prediction capabilities

#### Responsibilities:
- Endpoint and algorithm lifecycle management
- Prediction request orchestration
- A/B test coordination and evaluation
- Batch job processing
- Request validation and error handling

### 4. Research and Development (`research/`)

The experimentation and model development environment.

#### Key Components:
- **Jupyter Notebooks**: Interactive development environment
- **Training Scripts**: Model training and evaluation code
- **Serialized Models**: Joblib-pickled ML models and preprocessing artifacts
- **Data Processing**: Training data preparation and feature engineering

#### Responsibilities:
- Model experimentation and prototyping
- Data analysis and visualization
- Model training and hyperparameter tuning
- Performance evaluation and validation
- Artifact generation for production deployment

## Data Flow Architecture

### Phase 1: Model Development (Research → Production)

```
Raw Data → Jupyter Notebook → Data Processing → Model Training → Evaluation → Serialization → Production Deployment
```

1. **Data Ingestion**: CSV data loaded and explored in Jupyter notebooks
2. **Feature Engineering**: Data preprocessing, feature selection, and transformation
3. **Model Training**: Multiple algorithms trained and evaluated
4. **Artifact Generation**: Models and preprocessing objects serialized with joblib
5. **Production Packaging**: Classifier classes created with loading and prediction logic

### Phase 2: System Initialization (Startup)

```
WSGI Init → Registry Creation → Algorithm Loading → Database Sync → Service Ready
```

1. **Registry Initialization**: MLRegistry instance created in WSGI application
2. **Algorithm Instantiation**: Classifier classes loaded with trained models
3. **Database Synchronization**: Algorithm metadata stored in Django models
4. **Status Management**: Algorithms assigned initial statuses (testing/production)

### Phase 3: Prediction Request Processing

```
Client Request → API View → Registry Lookup → Algorithm Selection → Preprocessing → ML Prediction → Postprocessing → Response
```

1. **Request Reception**: JSON payload received via REST API
2. **Algorithm Resolution**: Registry queried for active algorithm by endpoint/status/version
3. **A/B Test Logic**: Random selection between competing algorithms if in A/B mode
4. **Data Transformation**: Input preprocessing (DataFrame conversion, missing value handling)
5. **Model Execution**: Scikit-learn prediction with probability outputs
6. **Result Formatting**: Postprocessing converts probabilities to business labels
7. **Response Generation**: JSON response with prediction, confidence, and metadata

### Phase 4: A/B Testing Workflow

```
Test Creation → Status Update → Request Distribution → Feedback Collection → Accuracy Calculation → Winner Promotion
```

1. **Test Initialization**: ABTest record created, algorithms set to "ab_testing" status
2. **Traffic Splitting**: Prediction requests randomly distributed (50/50)
3. **Performance Tracking**: All predictions logged with algorithm association
4. **Feedback Integration**: User feedback collected and linked to predictions
5. **Accuracy Computation**: Correct predictions calculated per algorithm
6. **Automated Promotion**: Higher-performing algorithm promoted to production

## Component Interaction Patterns

### Registry Pattern
The MLRegistry implements a centralized registry for algorithm management:
- **Registration**: Algorithms registered with metadata and instances
- **Lookup**: Runtime algorithm resolution by ID
- **Lifecycle**: Status transitions and version management

### Strategy Pattern
Classifier implementations follow a consistent interface:
- **Initialization**: Model and preprocessing artifact loading
- **Preprocessing**: Input data transformation
- **Prediction**: ML model execution
- **Postprocessing**: Output formatting

### Repository Pattern
Django models provide data access abstraction:
- **Endpoint Repository**: Endpoint metadata management
- **Algorithm Repository**: ML algorithm tracking
- **Request Repository**: Prediction logging and analytics

## Deployment Architecture

### Development Environment
- **Local SQLite**: Lightweight database for development
- **File-based Models**: Joblib artifacts stored locally
- **Django Dev Server**: Built-in development server
- **Debug Mode**: Full error reporting and debugging tools

### Production Environment
- **Production Database**: PostgreSQL/MySQL for scalability
- **Model Storage**: Cloud storage or dedicated ML artifact repository
- **WSGI Server**: Gunicorn/uWSGI for production serving
- **Load Balancing**: Nginx/HAProxy for request distribution
- **Monitoring**: Application performance monitoring and logging

## Security Architecture

### Data Protection
- **Input Validation**: Request data validation and sanitization
- **Error Handling**: Controlled error messages without information leakage
- **Rate Limiting**: API rate limiting to prevent abuse (extensible)

### Model Security
- **Version Control**: Algorithm versioning for rollback capabilities
- **Access Control**: Status-based algorithm access control
- **Audit Logging**: Comprehensive request logging for compliance

## Scalability Considerations

### Horizontal Scaling
- **Stateless Design**: API instances can be scaled independently
- **Shared Database**: Centralized metadata storage
- **Load Balancing**: Request distribution across multiple instances

### Performance Optimization
- **Model Caching**: In-memory model instances in registry
- **Batch Processing**: Efficient bulk prediction handling
- **Async Processing**: Potential for background job processing

### Monitoring and Observability
- **Request Metrics**: Prediction request volume and latency tracking
- **Model Performance**: Accuracy and drift monitoring
- **System Health**: Application and infrastructure monitoring

## Extensibility Patterns

### Adding New Algorithms
1. Implement classifier class following the standard interface
2. Train and serialize model artifacts
3. Register algorithm in WSGI initialization
4. Update API endpoints if needed

### Adding New Endpoints
1. Create new endpoint in database
2. Implement corresponding views and serializers
3. Add URL routing
4. Update registry logic if required

### Custom Pre/Post-processing
1. Extend classifier base class
2. Implement custom preprocessing methods
3. Add domain-specific postprocessing logic
4. Test with existing prediction flow

This architecture provides a robust, maintainable foundation for ML model deployment while supporting common MLOps patterns like A/B testing, model versioning, and continuous deployment.