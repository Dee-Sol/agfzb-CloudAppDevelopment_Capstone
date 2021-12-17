import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException


def main(dict):
    
    secret={ 
        "IAM_API_KEY": "insert API Key", 
        "COUCH_USERNAME": "Insert Username" 
    }
    
    client = Cloudant.iam(
        account_name = secret["COUCH_USERNAME"],
        api_key = secret["IAM_API_KEY"],
        connect=True
    )
    my_database = client["reviews"]
    
    try:
            
        selector = {"dealership": {"$eq": int(dict["dealerId"])}}
        result_by_filter = my_database.get_query_result(selector,raw_result=True)
        
        result= {
        'headers':{'Content-Type':'application/json'},
        'body':{'data':result_by_filter,
                'filter': dict["dealerId"]}
        }
        return result
        
    except:
        
        return {
                'statusCode': 404,
                'message':'Something went wrong'
        }   