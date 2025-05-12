import os

from azure_openai_service import OpenAIService

def ensure_directories_exist(config):
    """Ensure that the input and output directories specified in config exist."""
    for dir_key in ["input_directory", "output_directory"]:
        if dir_key in config:
            os.makedirs(config[dir_key], exist_ok=True)

def main():
    """Main entry point for the application."""
    try:
        # Initialize the OpenAI service
        openai_service = OpenAIService()
        
        # Ensure required directories exist
        ensure_directories_exist(openai_service.config)
        
        # Test prompt
        test_prompt = "Explain what natural language processing is in one paragraph."
        
        print("Sending test prompt to Azure OpenAI...")
        print(f"Prompt: {test_prompt}")
        
        # Generate and print the response
        response = openai_service.generate_completion(test_prompt)
        
        print("\nResponse from Azure OpenAI:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        # Save the response to a file in the output directory
        output_file = os.path.join(openai_service.config["output_directory"], "test_response.txt")
        with open(output_file, 'w') as f:
            f.write(response)
        
        print(f"\nResponse saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()