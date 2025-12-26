# file backend/server/server/wsgi.py
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
application = get_wsgi_application()

# ML registry
import inspect
from apps.ml.registry import MLRegistry
from apps.ml.classifier.random_forest import RandomForestClassifier
from apps.ml.classifier.extra_tree import ExtraTreeClassifier
from apps.ml.classifier.decision_tree import DecisionTreeClassifier

try:
    registry = MLRegistry() # create ML registry
    # Random Forest classifier
    rf = RandomForestClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="classifier",
                            algorithm_object=rf,
                            algorithm_name="random forest",
                            algorithm_status="production",
                            algorithm_version="1.0.2",
                            owner="Afra",
                            algorithm_description="Random Forest with simple pre- and post-processing",
                            algorithm_code=inspect.getsource(RandomForestClassifier))

    et = ExtraTreeClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="classifier",
                            algorithm_object=et,
                            algorithm_name="extra trees",
                            algorithm_status="testing",
                            algorithm_version="0.0.1",
                            owner="Afra",
                            algorithm_description="Extra Trees with simple pre- and post-processing",
                            algorithm_code=inspect.getsource(ExtraTreeClassifier))
    
    dt = DecisionTreeClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="classifier",
                            algorithm_object=dt,
                            algorithm_name="decision tree",
                            algorithm_status="testing",
                            algorithm_version="0.0.1",
                            owner="Afra",
                            algorithm_description="Decision Trees with simple pre- and post-processing",
                            algorithm_code=inspect.getsource(DecisionTreeClassifier))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))