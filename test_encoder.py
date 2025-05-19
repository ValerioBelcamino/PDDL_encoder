#!/usr/bin/env python3
"""
Test script for the PDDL Encoder tool.

This script demonstrates how to use the PDDL encoder with the example files.
"""

import os
import sys
import argparse
from pddl_encoder import PDDLEncoder

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test the PDDL encoder with example files.')
    parser.add_argument('--stochastic', action='store_true', help='Use stochastic encoding')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible stochastic encoding')
    args = parser.parse_args()
    
    # Create the encoder with specified options
    encoder = PDDLEncoder(stochastic=args.stochastic, seed=args.seed)
    
    # Set up paths
    example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example')
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example', 'encoded')
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process domain file
    domain_file = os.path.join(example_dir, 'blocks_domain.pddl')
    encoded_domain_file = os.path.join(output_dir, 'blocks_domain_encoded.pddl')
    encoder.process_pddl_file(domain_file, encoded_domain_file)
    print(f"Encoded domain file: {encoded_domain_file}")
    
    # Process problem file (using the same encoder to maintain consistent mapping)
    problem_file = os.path.join(example_dir, 'blocks_problem.pddl')
    encoded_problem_file = os.path.join(output_dir, 'blocks_problem_encoded.pddl')
    encoder.process_pddl_file(problem_file, encoded_problem_file)
    print(f"Encoded problem file: {encoded_problem_file}")
    
    # Save the encoding map
    map_file = os.path.join(output_dir, 'encoding_map.txt')
    encoder.save_encoding_map(map_file)
    print(f"Saved encoding map to: {map_file}")
    
    # Print the encoding map
    print("\nEncoding Map:")
    for original, encoded in encoder.encoding_map.items():
        print(f"{original} -> {encoded}")

if __name__ == "__main__":
    main()