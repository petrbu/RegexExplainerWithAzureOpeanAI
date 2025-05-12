import os
import re
import argparse # Added import

from azure_openai_service import OpenAIService

from csv_parser import TranslationPatternParser

def main():
    """Main entry point for the application."""
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Process translation patterns and generate explanations using Azure OpenAI.")
    parser.add_argument("input_file", help="Path to the input tab-separated UTF-16 file.")
    parser.add_argument("output_file", help="Path to the output tab-separated UTF-16 CSV file.")
    args = parser.parse_args()
    # --- End Argument Parsing ---

    try:
        # Initialize the OpenAI service
        openai_service = OpenAIService()
        
        # Ensure the directory for the output file exists
        output_dir = os.path.dirname(args.output_file)
        if output_dir: # Ensure output_dir is not an empty string (e.g. if output_file is just a filename)
            os.makedirs(output_dir, exist_ok=True)
        
        # Use arguments for input and output files
        input_file = args.input_file
        output_file = args.output_file
    
        parser_instance = TranslationPatternParser(input_file) # Renamed parser to parser_instance to avoid conflict
        patterns = parser_instance.parse()
    
        print(f"Found {len(patterns)} translation patterns in {input_file}")

        # Process patterns in batches of 20
        batch_size = 20
        for i in range(0, len(patterns), batch_size):
            batch_patterns = patterns[i:i + batch_size]

            print(f"\nProcessing batch {i // batch_size + 1} with {len(batch_patterns)} patterns...")

            # Construct the prompt for the batch
            prompt_lines = [
                "You are an expert in regular expressions. For each regular expression below, provide a very concise summary of the literal words or short phrases it matches.",
                "This is for a QA check, so keep the explanations extremely brief. Focus only on the key terms.",
                "Provide the explanation for each regex on a new line, prefixed with the regex number and a. For example:",
                "1. matches 'apple' or 'banana'",
                "2. looks for 'error' followed by a number",
                "\nHere are the regular expressions:"
            ]
            
            for idx, pattern_data in enumerate(batch_patterns):
                prompt_lines.append(f"{idx + 1}. {pattern_data['source_pattern']}")
            
            full_prompt = "\n".join(prompt_lines)

            try:
                # Send to Azure OpenAI
                response_text = openai_service.generate_completion(full_prompt, temperature=0.0)

                # Parse the response
                explanations = []
                if response_text:
                    # Use splitlines() for robust line splitting
                    response_lines = response_text.strip().splitlines()
                    for i_line, line_content in enumerate(response_lines):
                        current_line_to_process = line_content.strip() # Strip each line individually
                        # Try to match lines like "1. Explanation text"
                        # Group 1: digits, Group 2: the explanation text
                        match = re.match(r"^(\d+)\.\s*(.*)", current_line_to_process)
                        if match:
                            explanation_text = match.group(2).strip() # Explanation is in group 2
                            # Remove "matches " prefix if present
                            if explanation_text.lower().startswith("matches "):
                                explanation_text = explanation_text[len("matches "):].strip()

                            explanations.append(explanation_text)
                        else:
                            print(f"DEBUG: Line {i_line + 1} DID NOT MATCH regex.")
                
                if len(explanations) == len(batch_patterns):
                    print(f"\nExplanations for batch {i // batch_size + 1}:")
                    for idx, pattern_data in enumerate(batch_patterns):
                        print(f"  Regex: {pattern_data['source_pattern']}")
                        print(f"  Explanation: {explanations[idx]}")
                        # Add the explanation to the pattern_data dictionary
                        pattern_data['explanation'] = explanations[idx]
                else:
                    print(f"Warning: Number of explanations ({len(explanations)}) does not match number of regexes sent ({len(batch_patterns)}) for batch {i // batch_size + 1}.")
                    print("  Raw response was:")
                    print(response_text)
                    # Ensure all patterns in the batch have an explanation key, even if empty, to avoid issues during CSV writing
                    for pattern_data in batch_patterns:
                        if 'explanation' not in pattern_data:
                            pattern_data['explanation'] = "Error: Failed to get explanation"

            except Exception as e_openai:
                print(f"Error processing batch {i // batch_size + 1} with OpenAI: {str(e_openai)}")
                # Ensure all patterns in the batch have an explanation key if an error occurs
                for pattern_data in batch_patterns:
                    if 'explanation' not in pattern_data:
                        pattern_data['explanation'] = "Error: OpenAI call failed"

        # After processing all batches, save the updated patterns data (including explanations) to CSV
        print(f"\nSaving all patterns with explanations to {output_file}...")
        parser_instance.save_as_csv(output_file) # Use parser_instance
    

            
    except Exception as e:
        print(f"Error: {str(e)}")
        

if __name__ == "__main__":
    main()