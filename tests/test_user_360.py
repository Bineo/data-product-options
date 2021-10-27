from unittest import TestCase, main as unit_main
import requests

URL = "http://localhost:5000/v1/cx-engine/get-user-360"
# URL = "https://wap-cx-user-360-dev.azurewebsites.net/v1/cx-engine/get-user-360"


class TestFilters(TestCase): 
    def simple_example(self, source):
        if source not in ["tidy", "xls"]: 
            raise "Source for example is not Valid. "
        
        if source == "xls":
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
        elif source == "tidy":
            example_request = { 
                "input"     : {
                    "user360Request": {"userId" : "0001000524"}
                }, 
                "output"    : {
                    'userContext': {
                        'userName':'Arturo de la Torre',
                        'userId'  : '0001000522',
                        'userProfile': "María",
                        'situationContext': {
                            'overallScore': 84, 
                            'tags': ['innovador-tecnológico', 'califica-constructivamente']},
                        'lifecycleContext': [
                            ]
                        },
                    'productOffers': [{   'id': 532518, 
                                'date': '2021-04-06',
                                'expiry': '2021-05-06',
                                'class': 'credit-card',
                                'annualRate': 0.13,
                                'amount': 108000},
                            {   'id': 586373,
                                'date': '2021-05-12',
                                'expiry': '2021-06-11',
                                'class': 'mortgage', 
                                'annualRate': 0.07, 
                                'amount' : 2674000, 
                                'tenor'  : 79, 
                                'payments': 79}],
                    'pastInteractions': []
            }   }
        return example_request


    def test_returns_200(self): 
        sample   = self.simple_example(source="tidy")
        response = requests.post(URL, json=sample["input"])
        self.assertEqual(response.status_code, 200)


    def non_test_app_gets_sample(self):
        sample   = self.simple_example(source="tidy")
        response = requests.post(URL, json=sample["input"])
        obtained = response.json()
        self.assertEqual(obtained, sample["output"])
        


if __name__ == "__main__": 
    unit_main()

if False:
    from importlib import reload
    import tests.test_user_360 as test_360
    import src.engine as engine
    reload(test_360)
    reload(engine)

    the_tests = test_360.TestFilters()
    sample     = the_tests.simple_example(source="tidy")
    a_request  = sample["input"]["user360Request"]
    the_id     = a_request["userId"]
    
    a_response   = requests.post(URL, json=sample["input"])
    pre_response = engine.get_user_360(the_id, source="tidy")