#!/usr/bin/env python3
"""
Decode Batch PDDL Encoder Tool

This script decodes encoded PDDL code from JSON format back to the original format.
It takes the encoded_data.json and encoding_maps.json files and produces a JSON file
with the original PDDL code.
"""

import os
import sys
import json
import re
import argparse

def decode_pddl_string(encoded_string, encoding_map):
    """Decode an encoded PDDL string back to its original form using the encoding map."""
    import re
    
    # Start with the encoded string
    decoded_string = encoded_string
    
    # Replace each encoded name with its original name
    # Sort by length in descending order to avoid partial replacements
    for encoded, original in sorted(encoding_map.items(), key=lambda x: len(x[0]), reverse=True):
        # Use word boundaries to ensure we're replacing complete tokens
        decoded_string = re.sub(r'\b' + re.escape(encoded) + r'\b', original, decoded_string)
    
    return decoded_string

def decode_json_batch(encoded_data_file, encoding_maps_file, output_file):
    """Decode a batch of encoded PDDL code specified in JSON files."""
    # Load the encoded data
    with open(encoded_data_file, 'r') as f:
        encoded_data = json.load(f)
    
    # Load the encoding maps
    with open(encoding_maps_file, 'r') as f:
        encoding_maps = json.load(f)
    
    # Prepare output data structure
    decoded_data = []
    
    # Process each entry in the batch
    for i, entry in enumerate(encoded_data):
        print(f"\nDecoding entry {i+1}/{len(encoded_data)}")
        
        # Get the encoding map for this entry
        map_entry = next((m for m in encoding_maps if m["entry_id"] == i), None)
        if not map_entry:
            print(f"ERROR: No encoding map found for entry {i}")
            continue
        
        # Parse the encoding map
        encoding_map = {}
        for line in map_entry["encoding_map"].split('\n'):
            if line.strip():
                original, encoded = line.split('\t')
                encoding_map[encoded] = original
        
        # Get encoded PDDL code from the JSON structure
        encoded_domain = entry.get('instruction', '')
        encoded_problem = entry.get('input', '')
        encoded_plan = entry.get('output', '')
        
        # Decode PDDL code
        decoded_domain = decode_pddl_string(encoded_domain, encoding_map) if encoded_domain else ''
        print(f"Decoded domain PDDL code")
        
        decoded_problem = decode_pddl_string(encoded_problem, encoding_map) if encoded_problem else ''
        print(f"Decoded problem PDDL code")
        
        decoded_plan = decode_pddl_string(encoded_plan, encoding_map) if encoded_plan else ''
        print(f"Decoded plan PDDL code")
        
        # Prepare output entry
        output_entry = {
            "instruction": decoded_domain,
            "input": decoded_problem,
            "output": decoded_plan
        }
        
        # Add to output data structure
        decoded_data.append(output_entry)
        
        print(f"Decoded entry {i+1}")
    
    # Save the decoded data JSON
    with open(output_file, 'w') as f:
        json.dump(decoded_data, f, indent=4)
    print(f"\nSaved decoded data to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Decode batch of encoded PDDL code specified in JSON files.')
    parser.add_argument('encoded_data', help='JSON file containing encoded PDDL code')
    parser.add_argument('encoding_maps', help='JSON file containing encoding maps')
    parser.add_argument('output_file', help='Output JSON file for decoded PDDL code')
    
    args = parser.parse_args()
    
    # Convert relative paths to absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    encoded_data = os.path.join(script_dir, args.encoded_data) if not os.path.isabs(args.encoded_data) else args.encoded_data
    encoding_maps = os.path.join(script_dir, args.encoding_maps) if not os.path.isabs(args.encoding_maps) else args.encoding_maps
    output_file = os.path.join(script_dir, args.output_file) if not os.path.isabs(args.output_file) else args.output_file
    
    # Decode the batch
    decode_json_batch(encoded_data, encoding_maps, output_file)

if __name__ == "__main__":
    main()