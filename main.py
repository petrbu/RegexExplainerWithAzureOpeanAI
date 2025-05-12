import os
import re

from azure_openai_service import OpenAIService

from csv_parser import TranslationPatternParser

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
        
        # Test prompt, keep the commented part for future reference
        # test_prompt = "Explain what natural language processing is in one paragraph."
        
        # print("Sending test prompt to Azure OpenAI...")
        # print(f"Prompt: {test_prompt}")
        
        # # Generate and print the response
        # response = openai_service.generate_completion(test_prompt)
        
        # print("\nResponse from Azure OpenAI:")
        # print("-" * 50)
        # print(response)
        # print("-" * 50)
        
        # # Save the response to a file in the output directory
        # output_file = os.path.join(openai_service.config["output_directory"], "test_response.txt")
        # with open(output_file, 'w') as f:
        #     f.write(response)
        
        # print(f"\nResponse saved to {output_file}")

        input_file = os.path.join('data', 'input', 'CTG_en-US_pt-BR_uni.txt') # Or your chosen input file
        input_basename = os.path.basename(input_file)
        output_filename_stem = os.path.splitext(input_basename)[0]
        output_file = os.path.join('data', 'output', f"{output_filename_stem}.csv")
    
        parser = TranslationPatternParser(input_file)
        patterns = parser.parse()
    
        print(f"Found {len(patterns)} translation patterns")

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
            
            # print(f"\\n--- Prompt for Batch {i // batch_size + 1} ---")
            # print(full_prompt)
            # print("--- End of Prompt ---")

            try:
                # Send to Azure OpenAI
                response_text = openai_service.generate_completion(full_prompt, temperature=0.0)
                
                print(f"DEBUG: Raw OpenAI Response Text:\n'''{response_text}'''") # Added for debugging

                # print(f"\\n--- Response for Batch {i // batch_size + 1} ---")
                # print(response_text)
                # print("--- End of Response ---")

                # Parse the response
                explanations = []
                if response_text:
                    # Use splitlines() for robust line splitting
                    response_lines = response_text.strip().splitlines()
                    print(f"DEBUG: Number of response_lines from splitlines(): {len(response_lines)}")
                    for i_line, line_content in enumerate(response_lines):
                        current_line_to_process = line_content.strip() # Strip each line individually
                        print(f"DEBUG: Processing stripped line {i_line + 1}/{len(response_lines)}: ''{current_line_to_process}''")
                        # Try to match lines like "1. Explanation text"
                        # Group 1: digits, Group 2: the explanation text
                        match = re.match(r"^(\d+)\.\s*(.*)", current_line_to_process)
                        if match:
                            explanation_text = match.group(2).strip() # Explanation is in group 2
                            print(f"DEBUG: Line {i_line + 1} MATCHED. Explanation part: ''{explanation_text}''")
                            
                            # Remove "matches " prefix if present
                            if explanation_text.lower().startswith("matches "):
                                explanation_text = explanation_text[len("matches "):].strip()
                                print(f"DEBUG: Line {i_line + 1} after removing 'matches ': ''{explanation_text}''")

                            # Attempt to remove the bolded regex if OpenAI includes it
                            # e.g., "1. **^.*(?U) Expression** This is the explanation."
                            # if explanation_text.startswith('**'):
                            #     end_bold_regex_idx = explanation_text.find('**', 2) # Find closing **
                            #     if end_bold_regex_idx != -1:
                            #         explanation_text = explanation_text[end_bold_regex_idx + 2:].lstrip()
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

            # # Break after the first batch for debugging
            # print("\nDebugging: Processed only the first batch.")
            # break

        # After processing all batches, save the updated patterns data (including explanations) to CSV
        print(f"\nSaving all patterns with explanations to {output_file}...")
        parser.save_as_csv(output_file)
    
        # Print statistics (optional, if still relevant)
        # stats = parser.get_stats()
        # print("\\nStatistics:")
        # for key, value in stats.items():
        #     print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        

if __name__ == "__main__":
    main()