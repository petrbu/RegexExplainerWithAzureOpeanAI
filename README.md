# Regular Expression Explainer using Azure OpenAI

This project processes a list of regular expressions, sends them to Azure OpenAI to generate concise explanations of what each regex matches, and saves the original regex along with its explanation to an output file.

## Project Structure

- `main.py`: The main entry point for the application.
- `azure_openai_service.py`: Handles interactions with Azure OpenAI services.
- `csv_parser.py`: Contains logic for parsing CSV files.
- `config.json`: Configuration file, likely for API keys and endpoints. (A `config-sample.json` is provided as a template).
- `requirements.txt`: Lists the Python dependencies for this project.
- `data/input/`: Conventional directory for input text files. If using example paths, you may need to create this directory and place your input files here (e.g., `mkdir -p data/input`).
- `data/output/`: Conventional directory for output files. If using example paths, the script will create this directory if it does not exist.

## Getting Started

1.  **Set up Configuration**: Copy `config-sample.json` to `config.json` and fill in your Azure OpenAI credentials.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Application**:
    ```bash
    python3 main.py <path_to_input_file> <path_to_output_file>
    ```
    For example:
    ```bash
    python3 main.py data/input/en-US_pt-BR_mini.txt data/output/processed_en-US_pt-BR_mini.csv
    ```
    **Note:** The paths `data/input/...` and `data/output/...` in the example are conventional. You can use any valid file paths. If you use the example input path, ensure the `data/input/` directory and the specified input file exist. The script will create the output directory (e.g., `data/output/`) if it doesn't already exist.

## Purpose

This project takes an input file containing tab-separated data, where one column includes regular expressions. It processes these regular expressions in batches:
1.  It sends each batch of regular expressions to the Azure OpenAI service.
2.  It requests a very concise summary (explanation) of the literal words or short phrases that each regular expression matches. This is intended for a QA check, focusing on key terms.
3.  It parses the explanations received from Azure OpenAI.
4.  It then saves the original data along with the generated explanations into a new tab-separated UTF-16 CSV file.

## Setup

### Configuration

This project requires configuration for accessing Azure OpenAI services.

1.  **Create `config.json`:**
    Copy the contents of `config-sample.json` into a new file named `config.json` in the project's root directory.

2.  **Update `config.json` values:**
    Open `config.json` and replace the placeholder values with your actual Azure OpenAI credentials:
    *   `azure_openai_key`: Your Azure OpenAI API key.
    *   `azure_openai_endpoint`: Your Azure OpenAI endpoint URL.
    *   `azure_openai_deployment`: The name of your Azure OpenAI deployment (e.g., "gpt-4o").
    *   `azure_openai_api_version`: The API version for Azure OpenAI (e.g., "2025-01-01-preview").

    **Example `config.json` structure:**
    ```json
    {
      "azure_openai_key": "your-actual-azure-openai-key",
      "azure_openai_endpoint": "https://your-endpoint.openai.azure.com",
      "azure_openai_deployment": "your-deployment-name",
      "azure_openai_api_version": "your-api-version"
    }
    ```

    **Note:** Ensure that `config.json` is included in your `.gitignore` file to prevent committing sensitive credentials to your repository.
