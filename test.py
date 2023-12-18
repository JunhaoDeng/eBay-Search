import requests
# App ID (Client ID): JunhaoDe-AndrewEB-PRD-492d3cfae-fb57cd3e
# Dev ID: c82d051d-a8ce-408a-958a-fb36c330a45a
# Cert ID (Client Secret): PRD-92d3cfae414a-29b3-4d01-9e3f-3610

# eBay API endpoint URL
url = "https://svcs.eBay.com/services/search/FindingService/v1"

# Query parameters
params = {
    "OPERATION-NAME": "findItemsAdvanced",
    "SERVICE-VERSION": "1.0.0",
    # Replace with your API key
    "SECURITY-APPNAME": "JunhaoDe-AndrewEB-PRD-492d3cfae-fb57cd3e",
    "RESPONSE-DATA-FORMAT": "JSON",
    "keywords": "harry potter",
    "sortOrder": "PricePlusShippingLowest"
}

# Send the GET request to the eBay API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse and process the JSON response
    data = response.json()
    # Handle the eBay API response data as needed
    # (e.g., extracting item information)
    print(data)  # This will print the entire API response JSON

else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)  # Print the response text for debugging purposes
