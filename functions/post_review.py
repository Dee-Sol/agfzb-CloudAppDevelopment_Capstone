import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(dict):
    
    

    secret={ 
        "IAM_API_KEY": "R1LTcrjNtP1j8jFAWLfmXq9d88Lokeku0MJ_4G_Nq5Bn", 
        "COUCH_USERNAME": "5d49aa0b-868a-461b-bcb2-221fff937f75-bluemix" 
    }

    try:
        client = Cloudant.iam(
        account_name = secret["COUCH_USERNAME"],
        api_key = secret["IAM_API_KEY"],
        connect=True
        )

        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    # Define Target DB
    my_db = client["reviews"]
 
    try:
        #Query Largest Review ID number
        selector = {"_id": {"$gt": "0"}}
        query = my_db.get_query_result(
            selector, 
            raw_result = True, 
            fields = ["id"], 
            sort= [{"_id": "desc"}], 
            limit=1
            )["docs"][0]
        
        # Increment New Review ID
        new_id = int(query["id"])+1

        review = dict["review"]

        new_doc = {
            "id": new_id,
            "name": review["name"],
            "dealership": int(review["dealership"]),	
            "review": review["review"],	
            "purchase":	review["purchase"],
            "purchase_date": review["purchase_date"],
            "car_make":	review["car_make"],
            "car_model":  review["car_model"],
            "car_year": int(review["car_year"])
        }

        new_review_doc = my_db.create_document(new_doc)

        result = {
        'headers':{'Content-Type':'application/json'},
        'body':{"new_review_doc": new_review_doc}
        }

        return result
        
    except:
        
        return {
                'statusCode': 404,
                'message':'Something went wrong'
        }
    