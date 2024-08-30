import requests

class OAuthAPIClient:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.token = None

    def load_config(self, config_file):
        config = {}
        with open(config_file, 'r') as file:
            for line in file:
                key, value = line.strip().split('=', 1)
                config[key] = value
        return config

    def api_authentication(self):
        # Read the values from the loaded config
        token_url = self.config['token_url']
        client_id = self.config['client_id']
        client_pass = self.config['client_pass']
        
        # Payload for the token request
        payload = {
            'client_id': client_id,
            'client_secret': client_pass,
            'grant_type': 'client_credentials'
        }
        
        # Make a POST request to get the token
        response = requests.post(token_url, data=payload)
        response.raise_for_status()  # Raises an error for bad status codes
        
        # Store the token for future use
        self.token = response.json().get('access_token')

    def make_connection(self, base_url, params=None):
        if not self.token:
            raise ValueError("Authentication token is not available. Please authenticate first.")
        
        # Set the Authorization header using the token
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        # Make the GET request with the token in the headers
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        
        # Return the response data
        return response.json()

# Example Usage
client = OAuthAPIClient('path/to/oauth_keys.config')
client.api_authentication()
response_data = client.make_connection('https://example.com/api/resource')
print(response_data)
