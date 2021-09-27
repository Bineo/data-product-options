from unittest import TestCase, main as unit_main
import requests

URL = "http://localhost:5000/v1/cx-engine/get-user-360"
URL = "https://wap-cx-user-360-dev.azurewebsites.net/v1/cx-engine/get-user-360"


class TestFilters(TestCase): 
    def simple_example(self):
        example_request = { 
            "input"     : {
                "user360Request": {"userId" : "2872"}
            }, 
            "output"    : {
                'userContext': {
                    'userName':'Asunción Perez',
                    'userId'  : '2872',
                    'userProfile': "Marta",
                    'situationContext': {
                        'overallScore': 55, 
                        'tags': ['enojado-con-app', 'activo-en-app', 'consume-moderado']},
                    'lifecycleContext': [
                        {   'id': 799441, 
                            'date': '2020-11-03',
                            'lifecycle': 'Onboarding',
                            'class': 'credit-card',
                            'annualRate': 0.09,
                            'amount': 29000.0},
                        {   'id': 845859,
                            'date': '2021-07-23',
                            'lifecycle': 'Churn',
                            'class': 'debit'}]
                    },
                'productOffers': [],
                'pastInteractions': []
        }   }
        return example_request


    def test_app_gets_sample(self):
        sample   = self.simple_example()
        # response = requests.post(URL, json=example_request["input"])
        response = requests.post(URL, json=sample["input"])
        obtained = response.json()
        self.assertEqual(obtained, sample["output"])


if __name__ == "__main__": 
    unit_main()

