#!/usr/bin/env python3
"""
Test script to verify the reversibility of the PDDL batch encoding process.

This script tests:
1. If the encoding process is reversible (can we decode back to the original)
2. If processing the same JSON twice produces different encodings (with stochastic option)
3. Using VAL to validate the encoded PDDL tuples (if VAL is available)
"""

import os
import sys
import json
import tempfile
import subprocess
import argparse
import shutil
from pddl_encoder import PDDLEncoder, PDDL_KEYWORDS

# Function to decode PDDL string using encoding map
def decode_pddl_string(encoded_string, encoding_map):
    """Decode an encoded PDDL string back to its original form using the encoding map."""
    # The encoding_map is already in the format {encoded: original}
    
    # Start with the encoded string
    
    # Replace each encoded name with its original name
    # Sort by length in descending order to avoid partial replacements
    for original, encoded in encoding_map.items():
        encoded_string = encoded_string.replace(encoded, original)
        # Use word boundaries to ensure we're replacing complete tokens
    
    return encoded_string

# Function to test reversibility
def test_reversibility(json_file, encoded_data_file, encoding_maps_file):
    """Test if the encoding process is reversible."""
    print("\nTesting reversibility of the encoding process...")
    
    # Load the original JSON file
    with open(json_file, 'r') as f:
        original_data = json.load(f)
    
    # Load the encoded data
    with open(encoded_data_file, 'r') as f:
        encoded_data = json.load(f)
    
    # Load the encoding maps
    with open(encoding_maps_file, 'r') as f:
        encoding_maps = json.load(f)
    
    # Check if the number of entries match
    if len(original_data) != len(encoded_data):
        print(f"ERROR: Number of entries doesn't match. Original: {len(original_data)}, Encoded: {len(encoded_data)}")
        return False
    
    all_reversible = True
    
    # Process each entry
    for i, (original_entry, encoded_entry) in enumerate(zip(original_data, encoded_data)):
        print(f"\nChecking entry {i+1}/{len(original_data)}")
        
        # Get the encoding map for this entry
        map_entry = next((m for m in encoding_maps if m["entry_id"] == i), None)
        if not map_entry:
            print(f"ERROR: No encoding map found for entry {i}")
            all_reversible = False
            continue
        
        # Parse the encoding map
        encoding_map = map_entry["encoding_map"]

        

        
        # Decode the encoded PDDL strings
        decoded_domain = decode_pddl_string(encoded_entry["instruction"], encoding_map)
        decoded_problem = decode_pddl_string(encoded_entry["input"], encoding_map)
        decoded_plan = decode_pddl_string(encoded_entry["output"], encoding_map)
        
        # print(encoded_entry["instruction"])
        # with open("temp.pddl", "w") as f:
        #     f.write(decoded_domain)
        # # print(decoded_domain)
        # # print(original_entry["instruction"])
        # with open("temp2.pddl", "w") as f:
        #     f.write(original_entry["instruction"])
        # exit()
        # Compare with the original
        domain_match = decoded_domain.strip() == original_entry["instruction"].strip()
        problem_match = decoded_problem.strip() == original_entry["input"].strip()
        plan_match = decoded_plan.strip() == original_entry["output"].strip()
        
        if domain_match and problem_match and plan_match:
            print(f"Entry {i+1}: Successfully decoded back to the original")
        else:
            print(f"Entry {i+1}: Decoding failed")
            if not domain_match:
                print("  Domain doesn't match")
            if not problem_match:
                print("  Problem doesn't match")
            if not plan_match:
                print("  Plan doesn't match")
            all_reversible = False
    
    return all_reversible

# Function to test if processing twice produces different encodings (with stochastic option)
def test_stochastic_encoding(json_file):
    """Test if processing the same JSON twice with stochastic option produces different encodings."""
    print("\nTesting if stochastic encoding produces different results...")
    
    # Create temporary directories for the two runs
    temp_dir1 = tempfile.mkdtemp()
    temp_dir2 = tempfile.mkdtemp()
    
    try:
        # Run the batch encoder twice with stochastic option
        subprocess.run([sys.executable, "batch_encoder.py", json_file, 
                        "--output-dir", temp_dir1, "--stochastic"], check=True)
        subprocess.run([sys.executable, "batch_encoder.py", json_file, 
                        "--output-dir", temp_dir2, "--stochastic"], check=True)
        
        # Load the encoded data from both runs
        with open(os.path.join(temp_dir1, "encoded_data.json"), 'r') as f:
            encoded_data1 = json.load(f)
        
        with open(os.path.join(temp_dir2, "encoded_data.json"), 'r') as f:
            encoded_data2 = json.load(f)
        
        # Check if the encodings are different
        if len(encoded_data1) != len(encoded_data2):
            print("ERROR: Number of entries doesn't match between the two runs")
            return False
        
        all_different = True
        
        for i, (entry1, entry2) in enumerate(zip(encoded_data1, encoded_data2)):
            print(f"\nChecking entry {i+1}/{len(encoded_data1)}")
            
            # Compare the encoded strings
            domain_different = entry1["instruction"] != entry2["instruction"]
            problem_different = entry1["input"] != entry2["input"]
            plan_different = entry1["output"] != entry2["output"]
            
            if domain_different and problem_different and plan_different:
                print(f"Entry {i+1}: Stochastic encoding produced different results")
            else:
                print(f"Entry {i+1}: Stochastic encoding produced same results")
                if not domain_different:
                    print("  Domain encoding is the same")
                if not problem_different:
                    print("  Problem encoding is the same")
                if not plan_different:
                    print("  Plan encoding is the same")
                all_different = False
        
        return all_different
    
    finally:
        # Clean up temporary directories
        shutil.rmtree(temp_dir1)
        shutil.rmtree(temp_dir2)

# Function to test VAL validation
def test_val_validation(json_file, encoded_data_file, encoding_maps_file):
    """Test if VAL can validate the encoded PDDL tuples."""
    print("\nTesting VAL validation of encoded PDDL tuples...")
    
    # Check if VAL is available
    try:
        subprocess.run(["validate", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("WARNING: VAL not found in PATH. Skipping validation test.")
        return None
    
    # Create a temporary directory for the decoded files
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Load the encoded data
        with open(encoded_data_file, 'r') as f:
            encoded_data = json.load(f)
        
        # Load the encoding maps
        with open(encoding_maps_file, 'r') as f:
            encoding_maps = json.load(f)
        
        all_valid = True
        
        # Process each entry
        for i, encoded_entry in enumerate(encoded_data):
            print(f"\nValidating entry {i+1}/{len(encoded_data)}")
            
            # Get the encoding map for this entry
            map_entry = next((m for m in encoding_maps if m["entry_id"] == i), None)
            if not map_entry:
                print(f"ERROR: No encoding map found for entry {i}")
                all_valid = False
                continue
            
            # Parse the encoding map
            encoding_map = {}
            for line in map_entry["encoding_map"].split('\n'):
                if line.strip():
                    original, encoded = line.split('\t')
                    encoding_map[encoded] = original
            
            # Write the encoded PDDL to temporary files
            domain_file = os.path.join(temp_dir, f"domain_{i}.pddl")
            problem_file = os.path.join(temp_dir, f"problem_{i}.pddl")
            plan_file = os.path.join(temp_dir, f"plan_{i}.pddl")
            
            with open(domain_file, 'w') as f:
                f.write(encoded_entry["instruction"])
            
            with open(problem_file, 'w') as f:
                f.write(encoded_entry["input"])
            
            with open(plan_file, 'w') as f:
                f.write(encoded_entry["output"])
            
            # Run VAL to validate the plan
            try:
                result = subprocess.run(["validate", domain_file, problem_file, plan_file], 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                        text=True, check=False)
                
                if result.returncode == 0:
                    print(f"Entry {i+1}: VAL validation successful")
                else:
                    print(f"Entry {i+1}: VAL validation failed")
                    print(f"  Error: {result.stderr}")
                    all_valid = False
            except Exception as e:
                print(f"Entry {i+1}: VAL validation error: {e}")
                all_valid = False
        
        return all_valid
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

def main():
    parser = argparse.ArgumentParser(description='Test the reversibility of PDDL batch encoding.')
    parser.add_argument('json_file', help='Original JSON file with PDDL code')
    parser.add_argument('--encoded-data', default='example/encoded/encoded_data.json', 
                        help='Encoded data JSON file')
    parser.add_argument('--encoding-maps', default='example/encoded/encoding_maps.json', 
                        help='Encoding maps JSON file')
    parser.add_argument('--test-reversibility', action='store_true', 
                        help='Test if the encoding process is reversible')
    parser.add_argument('--test-stochastic', action='store_true', 
                        help='Test if stochastic encoding produces different results')
    parser.add_argument('--test-val', action='store_true', 
                        help='Test if VAL can validate the encoded PDDL tuples')
    
    args = parser.parse_args()
    
    # Convert relative paths to absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, args.json_file) if not os.path.isabs(args.json_file) else args.json_file
    encoded_data = os.path.join(script_dir, args.encoded_data) if not os.path.isabs(args.encoded_data) else args.encoded_data
    encoding_maps = os.path.join(script_dir, args.encoding_maps) if not os.path.isabs(args.encoding_maps) else args.encoding_maps
    
    # If no specific tests are requested, run all tests
    run_all = not (args.test_reversibility or args.test_stochastic or args.test_val)
    
    # Run the requested tests
    if run_all or args.test_reversibility:
        reversible = test_reversibility(json_file, encoded_data, encoding_maps)
        print(f"\nReversibility test {'PASSED' if reversible else 'FAILED'}")
    
    if run_all or args.test_stochastic:
        different = test_stochastic_encoding(json_file)
        if different is not None:
            print(f"\nStochastic encoding test {'PASSED' if different else 'FAILED'}")
    
    if run_all or args.test_val:
        valid = test_val_validation(json_file, encoded_data, encoding_maps)
        if valid is not None:
            print(f"\nVAL validation test {'PASSED' if valid else 'FAILED'}")

if __name__ == "__main__":
    main()