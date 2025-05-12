import csv
import os
from typing import List, Dict, Optional


class TranslationPatternParser:
    """
    Parser for translation pattern files that are tab-separated.
    Each row contains regular expression patterns and additional metadata.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the parser with the path to the pattern file.
        
        Args:
            file_path: Path to the pattern file to be parsed
        """
        self.file_path = file_path
        self.patterns = []
        
    def parse(self) -> List[Dict[str, str]]:
        """
        Parse the pattern file and extract structured data.
        
        Returns:
            A list of dictionaries containing the parsed patterns
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        patterns = []
        
        with open(self.file_path, 'r', encoding='utf-16') as file:
            for line in file:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Split by tabs
                parts = line.strip().split('\t')
                
                # Ensure we have at least the required columns
                if len(parts) >= 4:
                    pattern = {
                        'source_pattern': parts[0],
                        'target_pattern': parts[1],
                        'description': parts[2],
                        'flags': parts[3]
                    }
                    patterns.append(pattern)
                else:
                    print(f"Warning: Skipping malformed line: {line}")
        
        self.patterns = patterns
        return patterns
    
    def save_as_csv(self, output_path: str) -> None:
        """
        Save the parsed patterns as a properly formatted CSV file.
        
        Args:
            output_path: Path where the CSV file will be saved
        """
        if not self.patterns:
            self.parse()
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-16', newline='') as csvfile:
            # Define fieldnames in the desired order
            fieldnames = ['source_pattern', 'target_pattern', 'description', 'flags']
            if self.patterns and 'explanation' in self.patterns[0]:
                fieldnames.append('explanation')
            
            # Use tab as a delimiter and do not write a header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
            
            # writer.writeheader() # Removed to omit header
            for pattern in self.patterns:
                writer.writerow(pattern)
        
        print(f"CSV file saved at: {output_path}")
 