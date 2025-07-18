#!/usr/bin/env python3
"""
Batch PDDL Encoder Tool

This script processes PDDL code in JSON format, encoding domain, problem, and plan content.
The JSON file should contain a list of entries, each with 'instruction', 'input', and 'output' keys.

Example JSON format:
[
    {
        "instruction": "Encode blocks world",
        "input": {
            "domain": "(define (domain blocks-world) ...)",
            "problem": "(define (problem blocks-problem) ...)",
            "plan": "(pickup blockA) ..."
        },
        "output": {
            "domain": "encoded_domain_content",
            "problem": "encoded_problem_content",
            "plan": "encoded_plan_content",
            "map": "encoding_map_content"
        }
    }
]
"""

import os
import sys
import json
import re
import argparse
from pddl_encoder import PDDLEncoder, PDDL_KEYWORDS

def process_pddl_string(encoder, pddl_string):
    """Process a PDDL string and return the encoded version."""
    # Pattern to match PDDL names (identifiers)
    name_pattern = r'\b([a-zA-Z][a-zA-Z0-9_-]*)\b'
    
    def replace_name(match):
        name = match.group(1)
        if name.lower() in PDDL_KEYWORDS:
            return name
        return encoder.encode_name(name)
    
    # Replace names with encoded versions
    return re.sub(name_pattern, replace_name, pddl_string)

def process_json_batch(json_file, output_dir, stochastic=False, seed=None):
    """Process a batch of PDDL code specified in a JSON file."""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the JSON file
    with open(json_file, 'r') as f:
        batch_data = json.load(f)
    
    # Prepare output data structures
    encoded_data = []
    encoding_maps = []
    
    # Process each entry in the batch
    for i, entry in enumerate(batch_data):
        print(f"\nProcessing entry {i+1}/{len(batch_data)}")
        
        # Create a new encoder for each entry to ensure clean encoding
        encoder = PDDLEncoder(stochastic=stochastic, seed=seed)
        
        # Get PDDL code from the JSON structure
        domain_code = entry.get('instruction', '')
        problem_code = entry.get('input', '')
        plan_code = entry.get('output', '')
        
        # Process domain PDDL code
        encoded_domain = process_pddl_string(encoder, domain_code) if domain_code else ''
        print(f"Encoded domain PDDL code")
        
        # Process problem PDDL code
        encoded_problem = process_pddl_string(encoder, problem_code) if problem_code else ''
        print(f"Encoded problem PDDL code")
        
        # Process plan PDDL code
        encoded_plan = process_pddl_string(encoder, plan_code) if plan_code else ''
        print(f"Encoded plan PDDL code")
        
        # Prepare output entry
        output_entry = {
            "instruction": encoded_domain,
            "input": encoded_problem,
            "output": encoded_plan
        }
        
        # Get encoding map as string
        map_content = '\n'.join([f"{original}\t{encoded}" for original, encoded in encoder.encoding_map.items()])
        
        # Add to output data structures
        encoded_data.append(output_entry)
        encoding_maps.append({
            "entry_id": i,
            "encoding_map": encoder.encoding_map
        })
        
        print(f"Processed entry {i+1}")
    
    # Save the encoded data JSON
    encoded_data_path = os.path.join(output_dir, "encoded_data.json")
    with open(encoded_data_path, 'w') as f:
        json.dump(encoded_data, f, indent=4)
    print(f"\nSaved encoded data to: {encoded_data_path}")
    
    # Save the encoding maps JSON
    encoding_maps_path = os.path.join(output_dir, "encoding_maps.json")
    with open(encoding_maps_path, 'w') as f:
        json.dump(encoding_maps, f, indent=4)
    print(f"Saved encoding maps to: {encoding_maps_path}")

def main():
    parser = argparse.ArgumentParser(description='Batch process PDDL code specified in a JSON file.')
    parser.add_argument('json_file', help='JSON file containing batch processing instructions with PDDL code')
    parser.add_argument('--output-dir', default='example/encoded', help='Directory for output encoded files')
    parser.add_argument('--stochastic', action='store_true', help='Use stochastic encoding')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible stochastic encoding')
    
    args = parser.parse_args()
    
    # Convert relative paths to absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, args.output_dir) if not os.path.isabs(args.output_dir) else args.output_dir
    
    # Process the batch
    process_json_batch(args.json_file, output_dir, args.stochastic, args.seed)

if __name__ == "__main__":
    main()