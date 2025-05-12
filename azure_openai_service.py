import os
import json
from openai import AzureOpenAI

class OpenAIService:
    """
    Service class to handle communication with Azure OpenAI API.
    Loads configuration from the config.json file.
    """
    
    def __init__(self, config_path='config.json'):
        """Initialize the OpenAI service with configuration from the config file."""
        self.config = self._load_config(config_path)
        self.client = self._initialize_client()
    
    def _load_config(self, config_path):
        """Load configuration from the specified JSON file."""
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            return config
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client with configuration settings."""
        try:
            client = AzureOpenAI(
                api_key=self.config["azure_openai_key"],
                api_version=self.config["azure_openai_api_version"],
                azure_endpoint=self.config["azure_openai_endpoint"]
            )
            return client
        except Exception as e:
            raise Exception(f"Error initializing Azure OpenAI client: {str(e)}")
    
    def generate_completion(self, prompt, max_tokens=1000, temperature=0.7):
        """
        Generate a completion using Azure OpenAI API.
        
        Args:
            prompt (str): The prompt to send to the API
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Controls randomness (0.0-1.0)
            
        Returns:
            str: The generated completion text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config["azure_openai_deployment"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating completion: {str(e)}")