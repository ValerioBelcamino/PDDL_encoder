#!/usr/bin/env python3
"""
Test script for the PDDL Encoder tool's reversibility and stochasticity features.

This script demonstrates:
1. Encoding a PDDL file
2. Decoding it back to verify reversibility (pddl -> encoded -> decoded == original)
3. Stochastic encoding to generate different encodings of the same file
"""

import os
import sys
import filecmp
import tempfile
from pddl_encoder import PDDLEncoder

def test_reversibility():
    """Test that encoding and then decoding preserves the original PDDL content."""
    print("\n=== Testing Reversibility ===\n")
    
    # Create the encoder
    encoder = PDDLEncoder()
    
    # Set up paths
    example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example')
    temp_dir = tempfile.mkdtemp()
    
    # Original files
    domain_file = os.path.join(example_dir, 'blocks_domain.pddl')
    problem_file = os.path.join(example_dir, 'blocks_problem.pddl')
    
    # Encoded files
    encoded_domain_file = os.path.join(temp_dir, 'blocks_domain_encoded.pddl')
    encoded_problem_file = os.path.join(temp_dir, 'blocks_problem_encoded.pddl')
    
    # Decoded files
    decoded_domain_file = os.path.join(temp_dir, 'blocks_domain_decoded.pddl')
    decoded_problem_file = os.path.join(temp_dir, 'blocks_problem_decoded.pddl')
    
    # Encoding map
    map_file = os.path.join(temp_dir, 'encoding_map.txt')
    
    # Step 1: Encode the files
    print("Step 1: Encoding PDDL files...")
    encoder.process_pddl_file(domain_file, encoded_domain_file)
    encoder.process_pddl_file(problem_file, encoded_problem_file)
    encoder.save_encoding_map(map_file)
    
    # Step 2: Decode the files
    print("Step 2: Decoding PDDL files...")
    encoder.decode_pddl_file(encoded_domain_file, decoded_domain_file)
    encoder.decode_pddl_file(encoded_problem_file, decoded_problem_file)
    
    # Step 3: Compare original and decoded files
    print("Step 3: Comparing original and decoded files...")
    domain_match = filecmp.cmp(domain_file, decoded_domain_file, shallow=False)
    problem_match = filecmp.cmp(problem_file, decoded_problem_file, shallow=False)
    
    if domain_match and problem_match:
        print("✅ SUCCESS: Original and decoded files match!")
    else:
        print("❌ FAILURE: Original and decoded files do not match!")
        if not domain_match:
            print("  - Domain files differ")
        if not problem_match:
            print("  - Problem files differ")
    
    return domain_match and problem_match

def test_stochasticity():
    """Test that stochastic encoding produces different encodings for the same file."""
    print("\n=== Testing Stochasticity ===\n")
    
    # Set up paths
    example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example')
    temp_dir = tempfile.mkdtemp()
    
    # Original file
    domain_file = os.path.join(example_dir, 'blocks_domain.pddl')
    
    # Encoded files (multiple versions)
    encoded_file1 = os.path.join(temp_dir, 'blocks_domain_encoded1.pddl')
    encoded_file2 = os.path.join(temp_dir, 'blocks_domain_encoded2.pddl')
    
    # Encoding maps
    map_file1 = os.path.join(temp_dir, 'encoding_map1.txt')
    map_file2 = os.path.join(temp_dir, 'encoding_map2.txt')
    
    # Step 1: Create two encoders with stochasticity enabled
    print("Step 1: Creating stochastic encoders...")
    encoder1 = PDDLEncoder(stochastic=True)
    encoder2 = PDDLEncoder(stochastic=True)
    
    # Step 2: Encode the same file twice
    print("Step 2: Encoding the same file twice...")
    encoder1.process_pddl_file(domain_file, encoded_file1)
    encoder1.save_encoding_map(map_file1)
    
    encoder2.process_pddl_file(domain_file, encoded_file2)
    encoder2.save_encoding_map(map_file2)
    
    # Step 3: Compare the encoded files
    print("Step 3: Comparing encoded files...")
    files_match = filecmp.cmp(encoded_file1, encoded_file2, shallow=False)
    
    if files_match:
        print("❌ FAILURE: Stochastic encoding produced identical files!")
    else:
        print("✅ SUCCESS: Stochastic encoding produced different files!")
        
        # Print a sample of the differences
        print("\nSample of encoding differences:")
        with open(map_file1, 'r') as f1, open(map_file2, 'r') as f2:
            map1 = dict(line.strip().split('\t') for line in f1 if line.strip())
            map2 = dict(line.strip().split('\t') for line in f2 if line.strip())
            
            # Show a few examples of different encodings
            count = 0
            for key in map1:
                if key in map2 and map1[key] != map2[key]:
                    print(f"  {key}: {map1[key]} vs {map2[key]}")
                    count += 1
                    if count >= 5:  # Limit to 5 examples
                        break
    
    return not files_match

def test_reproducibility():
    """Test that stochastic encoding with the same seed produces identical results."""
    print("\n=== Testing Reproducibility with Seeds ===\n")
    
    # Set up paths
    example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example')
    temp_dir = tempfile.mkdtemp()
    
    # Original file
    domain_file = os.path.join(example_dir, 'blocks_domain.pddl')
    
    # Encoded files (multiple versions)
    encoded_file1 = os.path.join(temp_dir, 'blocks_domain_encoded_seed1.pddl')
    encoded_file2 = os.path.join(temp_dir, 'blocks_domain_encoded_seed2.pddl')
    
    # Step 1: Create two encoders with the same seed
    print("Step 1: Creating stochastic encoders with the same seed...")
    seed = 42  # Any fixed seed value
    encoder1 = PDDLEncoder(stochastic=True, seed=seed)
    encoder2 = PDDLEncoder(stochastic=True, seed=seed)
    
    # Step 2: Encode the same file twice with the same seed
    print("Step 2: Encoding the same file twice with the same seed...")
    encoder1.process_pddl_file(domain_file, encoded_file1)
    encoder2.process_pddl_file(domain_file, encoded_file2)
    
    # Step 3: Compare the encoded files
    print("Step 3: Comparing encoded files...")
    files_match = filecmp.cmp(encoded_file1, encoded_file2, shallow=False)
    
    if files_match:
        print("✅ SUCCESS: Encoders with the same seed produced identical files!")
    else:
        print("❌ FAILURE: Encoders with the same seed produced different files!")
    
    return files_match

def main():
    print("\n==== PDDL Encoder Reversibility and Stochasticity Tests ====\n")
    
    # Run all tests
    reversibility_passed = test_reversibility()
    stochasticity_passed = test_stochasticity()
    reproducibility_passed = test_reproducibility()
    
    # Summary
    print("\n==== Test Summary ====\n")
    print(f"Reversibility Test: {'PASSED' if reversibility_passed else 'FAILED'}")
    print(f"Stochasticity Test: {'PASSED' if stochasticity_passed else 'FAILED'}")
    print(f"Reproducibility Test: {'PASSED' if reproducibility_passed else 'FAILED'}")
    
    # Overall result
    if reversibility_passed and stochasticity_passed and reproducibility_passed:
        print("\n✅ All tests PASSED!")
        return 0
    else:
        print("\n❌ Some tests FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())