import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    if 'api_key' in kwargs:
    # Basic authentication GET
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                                auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
    # GET request without authentication
        try:
        # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'}, 
                                    params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = response.json()
    #json_data = json.loads(response.text)
    return json_data


# A `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))

    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    json_data = response.json()
    print('json_data', json_data)
    print("POST with status {} ".format(status_code))
    return json_data


# A get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# <OPTIONAL> # Create a get_dealer_by_id_from_cf method to filter by dealer id (or by state) from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

# get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):

    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            review_doc = review
            review_obj = DealerReview(dealership=review_doc["dealership"], purchase=review_doc["purchase"], 
                                   id=review_doc["id"], review=review_doc["review"], purchase_date=review_doc["purchase_date"],
                                   car_make=review_doc["car_make"], car_model=review_doc["car_model"], car_year=review_doc["car_year"],
                                   name=review_doc["name"], sentiment = "",
                                   )
            if review_obj.review:
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            else:
                review_obj.sentiment = 'neutral'
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = '70cCUs7COF4cQNoyqyvC7FydCy1oc1nMUs8NjOcTpVKg'
    version = '2021-08-01'
    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ceaa1b3b-5bc1-4103-9eac-7896b55ee389'
    features = Features(sentiment=SentimentOptions())
    return_analyzed_text = True
    
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=version,
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    # json_result = get_request(url, text=text, version=version, features=features, return_analyzed_text=return_analyzed_text, api_key=api_key)
    response = natural_language_understanding.analyze(
        text=text,
        features=features,
        language='en',
        return_analyzed_text=return_analyzed_text
    ).get_result()
    print(response)
    sentiment = ((response['sentiment'])['document'])['label']
    
    return sentiment
