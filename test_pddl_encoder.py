#!/usr/bin/env python3
"""
Unit tests for the PDDL Encoder tool.
Includes tests for reversibility and stochasticity features.
"""

import os
import unittest
import tempfile
import filecmp
from pddl_encoder import PDDLEncoder

class TestPDDLEncoder(unittest.TestCase):
    """Test cases for the PDDLEncoder class, including reversibility and stochasticity."""

    def setUp(self):
        """Set up test fixtures."""
        self.encoder = PDDLEncoder()
        self.test_dir = tempfile.mkdtemp()
        
        # Sample PDDL content for testing
        self.domain_content = """
(define (domain test-domain)
  (:requirements :strips :typing)
  (:types block table - object)
  (:predicates 
    (on ?x - block ?y - object)
    (clear ?x - object)
  )
  (:action move
    :parameters (?b - block ?from ?to - object)
    :precondition (and (on ?b ?from) (clear ?b) (clear ?to))
    :effect (and (not (on ?b ?from)) (not (clear ?to)) (on ?b ?to) (clear ?from))
  )
)
"""
        
        self.problem_content = """
(define (problem test-problem)
  (:domain test-domain)
  (:objects
    blockA blockB - block
    table - table
  )
  (:init
    (clear blockA)
    (clear blockB)
    (clear table)
    (on blockA table)
    (on blockB table)
  )
  (:goal (on blockA blockB))
)
"""
        
        # Create temporary files
        self.domain_file = os.path.join(self.test_dir, "domain.pddl")
        self.problem_file = os.path.join(self.test_dir, "problem.pddl")
        
        with open(self.domain_file, "w") as f:
            f.write(self.domain_content)
        
        with open(self.problem_file, "w") as f:
            f.write(self.problem_content)

    def test_encode_name(self):
        """Test the encode_name method."""
        # Keywords should not be encoded
        pddl_keywords = ["define", "domain", "requirements", "strips", "typing", "types", "predicates", "action", "parameters", "precondition", "effect", "not", "and", "or"]
        for keyword in pddl_keywords:
            self.assertEqual(self.encoder.encode_name(keyword), keyword, f"PDDL keyword {keyword} should not be encoded")
        
        # Regular names should be encoded
        self.assertEqual(self.encoder.encode_name("test-domain"), "x0")
        self.assertEqual(self.encoder.encode_name("block"), "x1")
        
        # Same name should get same encoding
        first_encoding = self.encoder.encode_name("some-name")
        second_encoding = self.encoder.encode_name("some-name")
        self.assertEqual(first_encoding, second_encoding)

    def test_encoding_map(self):
        """Test saving and loading the encoding map."""
        # Encode some names
        self.encoder.encode_name("test-domain")
        self.encoder.encode_name("block")
        self.encoder.encode_name("table")
        
        # Save the map
        map_file = os.path.join(self.test_dir, "map.txt")
        self.encoder.save_encoding_map(map_file)
        
        # Create a new encoder and load the map
        new_encoder = PDDLEncoder()
        new_encoder.load_encoding_map(map_file)
        
        # Check that the maps match
        self.assertEqual(self.encoder.encoding_map, new_encoder.encoding_map)

    def test_process_pddl_file_regex(self):
        """Test processing a PDDL file with regex approach."""
        # Force regex approach by monkey patching
        
    def test_decode_name(self):
        """Test the decode_name method."""
        # Encode some names
        self.encoder.encode_name("test-domain")
        self.encoder.encode_name("block")
        self.encoder.encode_name("table")
        
        # Test decoding
        self.assertEqual(self.encoder.decode_name("x0"), "test-domain")
        self.assertEqual(self.encoder.decode_name("x1"), "block")
        self.assertEqual(self.encoder.decode_name("x2"), "table")
        
        # Keywords should not be affected
        self.assertEqual(self.encoder.decode_name("define"), "define")
        
        # Unknown encoded names should be returned as is
        self.assertEqual(self.encoder.decode_name("x999"), "x999")
        
    def test_reversibility(self):
        """Test that encoding and then decoding preserves the original content."""
        # Create temporary files for the test
        encoded_file = os.path.join(self.test_dir, "encoded.pddl")
        decoded_file = os.path.join(self.test_dir, "decoded.pddl")
        
        # Encode the domain file
        self.encoder.process_pddl_file(self.domain_file, encoded_file)
        
        # Decode the encoded file
        self.encoder.decode_pddl_file(encoded_file, decoded_file)
        
        # Compare original and decoded files
        self.assertTrue(filecmp.cmp(self.domain_file, decoded_file, shallow=False))
        
    def test_stochastic_encoding(self):
        """Test that stochastic encoding produces different results."""
        # Create two encoders with stochasticity enabled
        encoder1 = PDDLEncoder(stochastic=True)
        encoder2 = PDDLEncoder(stochastic=True)
        
        # Encode the same name with both encoders
        encoded1 = encoder1.encode_name("test-name")
        encoded2 = encoder2.encode_name("test-name")
        
        # The encodings should be different
        self.assertNotEqual(encoded1, encoded2)
        
        # But they should both decode back to the original
        self.assertEqual(encoder1.decode_name(encoded1), "test-name")
        self.assertEqual(encoder2.decode_name(encoded2), "test-name")
        
    def test_reproducible_encoding(self):
        """Test that stochastic encoding with the same seed produces identical results."""
        # Create two encoders with the same seed
        seed = 42
        encoder1 = PDDLEncoder(stochastic=True, seed=seed)
        encoder2 = PDDLEncoder(stochastic=True, seed=seed)
        
        # Encode the same names with both encoders
        names = ["domain", "block", "table", "on", "clear"]
        
        for name in names:
            encoded1 = encoder1.encode_name(name)
            encoded2 = encoder2.encode_name(name)
            # With the same seed, encodings should be identical
            self.assertEqual(encoded1, encoded2)
        original_process = self.encoder._process_with_pddl_lib
        self.encoder._process_with_pddl_lib = lambda *args: None
        
        # Process the domain file
        output_domain = os.path.join(self.test_dir, "domain_encoded.pddl")
        self.encoder.process_pddl_file(self.domain_file, output_domain)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(output_domain))
        
        # Restore original method
        self.encoder._process_with_pddl_lib = original_process

    def test_consistent_encoding(self):
        """Test that domain and problem files are encoded consistently."""
        # Process the domain file
        output_domain = os.path.join(self.test_dir, "domain_encoded.pddl")
        self.encoder.process_pddl_file(self.domain_file, output_domain)
        
        # Process the problem file with the same encoder
        output_problem = os.path.join(self.test_dir, "problem_encoded.pddl")
        self.encoder.process_pddl_file(self.problem_file, output_problem)
        
        # Read the encoded files
        with open(output_domain, "r") as f:
            encoded_domain = f.read()
        
        with open(output_problem, "r") as f:
            encoded_problem = f.read()
        
        # Check that the domain name in the problem file matches the encoded domain name
        domain_name = self.encoder.encoding_map.get("test-domain")
        self.assertIn(f"(:domain {domain_name})", encoded_problem)

if __name__ == "__main__":
    unittest.main()