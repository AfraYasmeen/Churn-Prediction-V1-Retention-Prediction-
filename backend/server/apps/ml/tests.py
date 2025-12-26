from django.test import TestCase
import inspect
from apps.ml.registry import MLRegistry

from apps.ml.classifier.random_forest import RandomForestClassifier
from apps.ml.classifier.extra_tree import ExtraTreeClassifier
from apps.ml.classifier.decision_tree import DecisionTreeClassifier

class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {'C0RPRODUCTTYPE': 3.0,
        'ELECMETERTYPE': 0.0, 
        'TOTELECCONSUMPTION': 2531.0, 
        'TOTE7CONSUMPTION': 0.0, 
        'TOTGASCONSUMPTION': 0.0, 
        'DNO': 14.0, 
        'DAYSINCONTRACTEND': 71.0, 
        'Home': 1.0, 
        'Intermediate': 1.0, 
        'Results': 1.0, 
        'MoreInfo': 0.0, 
        'CustomerDetails': 0.0, 
        'Journey': 2.0, 
        'SwitchCounts': 1.0, 
        'MinTotalCost': 0.0, 
        'MaxTotalCost': 0.0, 
        'Big6SavingPercentage': 0.0, 
        'SavingPecentage': 0.0, 
        'MinSavings': 0.0, 
        'MaxSavings': 0.0, 
        'CheapestBig6': 0.0, 
        'SelectedTariff_HasCancellationFee': 0.0, 
        'SelectedTariff_HasOnlineManagement': 0.0, 
        'SelectedTariff_HasPaperBilling': 0.0, 
        'SelectedTariff_HasWarmHomeDiscount': 0.0}
        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('<=50K', response['label'])

    def test_et_algorithm(self):
        input_data = {'C0RPRODUCTTYPE': 3.0,
        'ELECMETERTYPE': 0.0, 
        'TOTELECCONSUMPTION': 2531.0, 
        'TOTE7CONSUMPTION': 0.0, 
        'TOTGASCONSUMPTION': 0.0, 
        'DNO': 14.0, 
        'DAYSINCONTRACTEND': 71.0, 
        'Home': 1.0, 
        'Intermediate': 1.0, 
        'Results': 1.0, 
        'MoreInfo': 0.0, 
        'CustomerDetails': 0.0, 
        'Journey': 2.0, 
        'SwitchCounts': 1.0, 
        'MinTotalCost': 0.0, 
        'MaxTotalCost': 0.0, 
        'Big6SavingPercentage': 0.0, 
        'SavingPecentage': 0.0, 
        'MinSavings': 0.0, 
        'MaxSavings': 0.0, 
        'CheapestBig6': 0.0, 
        'SelectedTariff_HasCancellationFee': 0.0, 
        'SelectedTariff_HasOnlineManagement': 0.0, 
        'SelectedTariff_HasPaperBilling': 0.0, 
        'SelectedTariff_HasWarmHomeDiscount': 0.0}
        my_alg = ExtraTreeClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('<=50K', response['label'])
    
    def test_df_algorithm(self):
        input_data = {'C0RPRODUCTTYPE': 3.0,
        'ELECMETERTYPE': 0.0, 
        'TOTELECCONSUMPTION': 2531.0, 
        'TOTE7CONSUMPTION': 0.0, 
        'TOTGASCONSUMPTION': 0.0, 
        'DNO': 14.0, 
        'DAYSINCONTRACTEND': 71.0, 
        'Home': 1.0, 
        'Intermediate': 1.0, 
        'Results': 1.0, 
        'MoreInfo': 0.0, 
        'CustomerDetails': 0.0, 
        'Journey': 2.0, 
        'SwitchCounts': 1.0, 
        'MinTotalCost': 0.0, 
        'MaxTotalCost': 0.0, 
        'Big6SavingPercentage': 0.0, 
        'SavingPecentage': 0.0, 
        'MinSavings': 0.0, 
        'MaxSavings': 0.0, 
        'CheapestBig6': 0.0, 
        'SelectedTariff_HasCancellationFee': 0.0, 
        'SelectedTariff_HasOnlineManagement': 0.0, 
        'SelectedTariff_HasPaperBilling': 0.0, 
        'SelectedTariff_HasWarmHomeDiscount': 0.0}
        my_alg = DecisionTreeClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('<=50K', response['label'])

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "income_classifier"
        algorithm_object = RandomForestClassifier()
        algorithm_name = "random forest"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Afra"
        algorithm_description = "Random Forest with simple pre- and post-processing"
        algorithm_code = inspect.getsource(RandomForestClassifier)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                    algorithm_status, algorithm_version, algorithm_owner,
                    algorithm_description, algorithm_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)