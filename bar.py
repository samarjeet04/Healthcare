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

    print("API Request:")
    print("Method:", method)
    print("Endpoint:", endpoint)
    print("Data:", data)

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

# Function to create a bar chart visualization with the provided aggregation query
def create_histogram_bar_chart(index_pattern_id):
    # Define the endpoint for creating a new visualization
    endpoint = "/api/saved_objects/visualization"

    # Create the visualization configuration for the histogram bar chart
    visualization_config ={
    "attributes": {
        "title": "Records Count by Day of the Week",
        "visState": json.dumps({
            "type": "histogram",
            "params": {
                "addLegend": True,
                "addTimeMarker": False,
                "addTooltip": True,
                "defaultYExtents": False,
                "legendPosition": "right",
                "scale": "linear",
                "setYExtents": False,
                "shareYAxis": True,
                "times": [],
                "yAxis": {
                    "id": "1",
                    "type": "metrics",
                    "schema": "metric",
                    "params": {
                        "field": "day_of_week_i",
                        "customLabel": "Count",
                        "orderAgg": "2",
                        "orderBy": "1"
                    }
                }
            },
            "aggs": [
                {
                    "id": "2",
                    "type": "count",
                    "schema": "metric",
                    "params": {}
                },
                {
                    "id": "3",
                    "type": "histogram",
                    "schema": "segment",
                    "params": {
                        "field": "day_of_week_i",
                        "interval": 1,
                        "min_doc_count": 0
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
                "index": "kibana_sample_ecommerce_data",
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
        print("Histogram bar chart visualization created successfully!")
    else:
        print("Failed to create histogram bar chart visualization. Status code:", response.status_code)
        print("Error message:", response.text)

# Your index pattern ID (replace this with the correct ID of your index pattern)
index_pattern_id = "kibana_sample_data_ecommerce"

# Call the function to create the histogram bar chart visualization
create_histogram_bar_chart(index_pattern_id)