# NLP Project for Translation

This project appears to be focused on Natural Language Processing (NLP) tasks, specifically related to translation and utilizing Azure OpenAI services.

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
    python main.py <path_to_input_file> <path_to_output_file>
    ```
    For example:
    ```bash
    python main.py data/input/CTG_en-US_pt-BR_mini.txt data/output/processed_CTG_en-US_pt-BR_mini.csv
    ```
    **Note:** The paths `data/input/...` and `data/output/...` in the example are conventional. You can use any valid file paths. If you use the example input path, ensure the `data/input/` directory and the specified input file exist. The script will create the output directory (e.g., `data/output/`) if it doesn't already exist.

## Purpose

The project seems to process input text files (containing text in different languages), potentially perform translations or other NLP tasks using Azure OpenAI, and then output the results in CSV format.

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
