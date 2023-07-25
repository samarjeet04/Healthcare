import requests
import base64
import json

# Define the Kibana server URL and API key credentials
kibana_url = "http://localhost:5601"
api_key_id = ""
api_key = ""

# Encode the API key ID and key in Base64 format
api_key_encoded = base64.standard_b64encode(f"{api_key_id}:{api_key}".encode("utf-8")).decode("utf-8")


# Function to send requests to the Kibana API using the API key for authentication
def send_kibana_request(method, endpoint, data=None):
    headers = {
        "Authorization": f"ApiKey {api_key_encoded}",
        "kbn-xsrf": "true"
    }
    url = f"{kibana_url}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError("Invalid HTTP method.")

    return response

def create_pie_chart(index_pattern_id):
    # Define the endpoint for creating a new visualization
    endpoint = "/api/saved_objects/visualization"

    # Create the visualization configuration for the pie chart
    visualization_config = {
        "attributes": {
            "title": "Pie Chart",
            "visState": json.dumps({
                "type": "pie",
                "params": {
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "isDonut": False,
                    "labels": {
                        "show": True,
                        "values": True,
                        "last_level": True,
                        "truncate": 100
                    },
                    "dimension": {
                        "accessor": 0,
                        "formatFn": None,
                        "params": {},
                        "aggType": "count"
                    },
                    "metric": {
                        "accessor": 1,
                        "formatFn": None,
                        "params": {}
                    },
                    "bucket": {
                        "accessor": 2,
                        "formatFn": None,
                        "params": {
                            "field": "customer_gender",
                            "size": 5,
                            "order": "desc",
                            "orderBy": "_key"
                        },
                        "aggType": "terms"
                    }
                },
                "aggs": [
                    {
                        "id": "2",
                        "type": "terms",
                        "schema": "segment",
                        "params": {
                            "field": "customer_gender",
                            "size": 5,
                            "order": {
                                "_key": "desc"
                            }
                        }
                    },
                    {
                        "id": "1",
                        "type": "cardinality",
                        "schema": "metric",
                        "params": {
                            "field": "order_date"
                        }
                    },
                    {
                        "id": "3",
                        "type": "terms",
                        "schema": "bucket",
                        "params": {
                            "field": "order_date",
                            "size": 0,
                            "order": {
                                "_key": "desc"
                            }
                        }
                    }
                ],
                "listeners": {}
            }),
            "uiStateJSON": "{}",
            "description": "",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": index_pattern_id,
                    "query": {
                        "query": "",
                        "language": "kuery"
                    },
                    "filter": []
                })
            }
        }
    }

    # Send the POST request to create the visualization
    response = send_kibana_request("POST", endpoint, data=visualization_config)

    if response.status_code == 200:
        print("Pie chart visualization created successfully!")
    else:
        print("Failed to create pie chart visualization. Status code:", response.status_code)
        print("Error message:", response.text)

# Your index pattern ID (replace this with the correct ID of your index pattern)
index_pattern_id = "kibana_sample_data_ecommerce"

# Call the function to create the pie chart visualization
create_pie_chart(index_pattern_id)
