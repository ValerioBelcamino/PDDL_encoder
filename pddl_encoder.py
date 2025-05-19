#!/usr/bin/env python3
"""
PDDL Encoder Tool

A tool to encode names in PDDL files while preserving keywords.
The encoding is simple, short, and decoupled from the semantic context.
Supports reversible encoding and stochastic encoding for LLM training.
"""

import re
import os
import sys
import random
import string
import argparse
from typing import Dict, List, Tuple, Set, Optional, Union

# PDDL keywords that should not be encoded
PDDL_KEYWORDS = {
    # PDDL requirements
    'strips', 'typing', 'negative-preconditions', 'disjunctive-preconditions',
    'equality', 'existential-preconditions', 'universal-preconditions',
    'quantified-preconditions', 'conditional-effects', 'fluents',
    'numeric-fluents', 'adl', 'durative-actions', 'duration-inequalities',
    'continuous-effects', 'derived-predicates', 'timed-initial-literals',
    'preferences', 'constraints', 'action-costs',
    # Domain keywords
    'define', 'domain', 'requirements', 'types', 'constants', 'predicates',
    'functions', 'constraints', 'action', 'parameters', 'precondition', 'effect',
    'and', 'or', 'not', 'imply', 'exists', 'forall', 'when', 'increase', 'decrease',
    'assign', 'scale-up', 'scale-down', 'durative-action', 'duration', 'condition',
    'at', 'start', 'end', 'over', 'all', 'preference', 'always', 'sometime',
    'within', 'at-most-once', 'sometime-after', 'sometime-before',
    'always-within', 'hold-during', 'hold-after',
    # Problem keywords
    'problem', 'objects', 'init', 'goal', 'metric', 'minimize', 'maximize',
    'total-time', 'is-violated',
    # Requirements keywords
    ':strips', ':typing', ':negative-preconditions', ':disjunctive-preconditions',
    ':equality', ':existential-preconditions', ':universal-preconditions',
    ':quantified-preconditions', ':conditional-effects', ':fluents',
    ':numeric-fluents', ':adl', ':durative-actions', ':duration-inequalities',
    ':continuous-effects', ':derived-predicates', ':timed-initial-literals',
    ':preferences', ':constraints', ':action-costs',
    # Types
    'number', 'object',
    # Operators and symbols
    '=', '<', '>', '<=', '>=', '+', '-', '*', '/', '(', ')', '-', '?',
}


class PDDLEncoder:
    """A class to encode names in PDDL files with support for reversible and stochastic encoding."""

    def __init__(self, stochastic: bool = False, seed: Optional[int] = None):
        self.encoding_map: Dict[str, str] = {}
        self.decoding_map: Dict[str, str] = {}
        self.next_id = 0
        self.prefix = 'x'  # Default prefix for non-stochastic mode
        self.stochastic = stochastic
        self.max_symbols = len(string.ascii_lowercase) * 10  # Initial capacity
        self.current_prefix_index = 0
        
        # Initialize random state for reproducibility
        self.random_state = random.Random()
        if seed is not None:
            self.random_state.seed(seed)

    def reset(self):
        """Reset the encoder state."""
        self.encoding_map = {}
        self.decoding_map = {}
        self.next_id = 0

    def encode_name(self, name: str) -> str:
        """Encode a name if it's not already encoded."""
        # Don't encode if it's a keyword or already encoded
        if name.lower() in PDDL_KEYWORDS or name in self.encoding_map:
            return self.encoding_map.get(name, name)

        # Generate a new encoded name
        if self.stochastic:
            # Check if we need to expand capacity
            if self.next_id >= self.max_symbols:
                self.current_prefix_index += 1
                self.next_id = 0
                self.max_symbols = len(string.ascii_lowercase) * 10 * (self.current_prefix_index + 1)
            
            # Generate random prefix and number using instance's random state
            prefix = self.random_state.choice(string.ascii_lowercase)
            number = self.next_id % 10
            if self.current_prefix_index > 0:
                prefix = ''.join(self.random_state.choices(string.ascii_lowercase, k=self.current_prefix_index + 1))
            
            encoded_name = f"{prefix}{number}"
        else:
            encoded_name = f"{self.prefix}{self.next_id}"
            
        self.encoding_map[name] = encoded_name
        self.decoding_map[encoded_name] = name
        self.next_id += 1
        return encoded_name
        
    def decode_name(self, encoded_name: str) -> str:
        """Decode an encoded name back to its original form."""
        # If it's a keyword or not in our decoding map, return as is
        if encoded_name.lower() in PDDL_KEYWORDS:
            return encoded_name
            
        return self.decoding_map.get(encoded_name, encoded_name)

    def save_encoding_map(self, output_file: str):
        """Save the encoding map to a file."""
        with open(output_file, 'w') as f:
            for original, encoded in self.encoding_map.items():
                f.write(f"{original}\t{encoded}\n")

    def load_encoding_map(self, input_file: str):
        """Load the encoding map from a file."""
        self.encoding_map = {}
        self.decoding_map = {}
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    original, encoded = line.strip().split('\t')
                    self.encoding_map[original] = encoded
                    self.decoding_map[encoded] = original
                    
                    # Update next_id to be greater than any existing id
                    if encoded.startswith(self.prefix):
                        try:
                            # Handle both standard and stochastic encodings
                            if '_' in encoded:
                                id_part = encoded[len(self.prefix):].split('_')[0]
                                id_num = int(id_part)
                            else:
                                id_num = int(encoded[len(self.prefix):])
                            self.next_id = max(self.next_id, id_num + 1)
                        except ValueError:
                            pass

    def process_pddl_file(self, input_file: str, output_file: str) -> None:
        """Process a PDDL file and encode names."""
        try:
            # Try to use the pddl library if available
            import pddl
            return self._process_with_pddl_lib(input_file, output_file)
        except ImportError:
            # Fall back to regex-based processing
            return self._process_with_regex(input_file, output_file)

    def _process_with_pddl_lib(self, input_file: str, output_file: str) -> None:
        """Process a PDDL file using the pddl library."""
        import pddl
        
        # Determine if it's a domain or problem file
        with open(input_file, 'r') as f:
            content = f.read()
        
        if '(define (domain' in content:
            # It's a domain file
            domain = pddl.parse_domain(input_file)
            # Encode domain name
            domain.name = self.encode_name(domain.name)
            
            # Encode types
            if domain.types:
                encoded_types = {}
                for type_name, parent_type in domain.types.items():
                    if type_name.lower() not in PDDL_KEYWORDS:
                        encoded_name = self.encode_name(type_name)
                        encoded_types[encoded_name] = parent_type
                    else:
                        encoded_types[type_name] = parent_type
                domain.types = encoded_types
            
            # Encode constants
            if domain.constants:
                for constant in domain.constants:
                    if constant.name.lower() not in PDDL_KEYWORDS:
                        constant.name = self.encode_name(constant.name)
            
            # Encode predicates
            if domain.predicates:
                for predicate in domain.predicates:
                    if predicate.name.lower() not in PDDL_KEYWORDS:
                        predicate.name = self.encode_name(predicate.name)
            
            # Encode actions
            if domain.actions:
                for action in domain.actions:
                    if action.name.lower() not in PDDL_KEYWORDS:
                        action.name = self.encode_name(action.name)
            
            # Write the encoded domain
            with open(output_file, 'w') as f:
                f.write(str(domain))
        
        elif '(define (problem' in content:
            # It's a problem file
            problem = pddl.parse_problem(input_file)
            # Encode problem name
            problem.name = self.encode_name(problem.name)
            
            # Encode domain reference
            problem.domain = self.encode_name(problem.domain)
            
            # Encode objects
            if problem.objects:
                for obj in problem.objects:
                    if obj.name.lower() not in PDDL_KEYWORDS:
                        obj.name = self.encode_name(obj.name)
            
            # Write the encoded problem
            with open(output_file, 'w') as f:
                f.write(str(problem))
        
        else:
            raise ValueError(f"File {input_file} does not appear to be a valid PDDL domain or problem file.")

    def _process_with_regex(self, input_file: str, output_file: str) -> None:
        """Process a PDDL file using regex patterns when pddl library is not available."""
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Pattern to match PDDL names (identifiers)
        # This is a simplified pattern and might need refinement
        name_pattern = r'\b([a-zA-Z][a-zA-Z0-9_-]*)\b'
        
        def replace_name(match):
            name = match.group(1)
            if name.lower() in PDDL_KEYWORDS:
                return name
            return self.encode_name(name)
        
        # Replace names with encoded versions
        encoded_content = re.sub(name_pattern, replace_name, content)
        
        with open(output_file, 'w') as f:
            f.write(encoded_content)


    def decode_pddl_file(self, input_file: str, output_file: str) -> None:
        """Decode an encoded PDDL file back to its original form."""
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Pattern to match encoded names (identifiers)
        # This handles both standard and stochastic encodings
        encoded_pattern = r'\b(' + self.prefix + r'\d+(?:_\d+)?)\b'
        
        def replace_encoded(match):
            encoded_name = match.group(1)
            return self.decode_name(encoded_name)
        
        # Replace encoded names with original versions
        decoded_content = re.sub(encoded_pattern, replace_encoded, content)
        
        with open(output_file, 'w') as f:
            f.write(decoded_content)


def main():
    parser = argparse.ArgumentParser(description='Encode names in PDDL files.')
    parser.add_argument('input', help='Input PDDL file or directory')
    parser.add_argument('output', help='Output PDDL file or directory')
    parser.add_argument('--map', help='File to save/load the encoding map')
    parser.add_argument('--prefix', default='x', help='Prefix for encoded names')
    parser.add_argument('--batch', action='store_true', help='Process all PDDL files in the input directory')
    parser.add_argument('--decode', action='store_true', help='Decode encoded PDDL files back to original form')
    parser.add_argument('--stochastic', action='store_true', help='Use stochastic encoding for varied outputs')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible stochastic encoding')
    
    args = parser.parse_args()
    
    encoder = PDDLEncoder(stochastic=args.stochastic, seed=args.seed)
    encoder.prefix = args.prefix
    
    # Load existing encoding map if provided
    if args.map and os.path.exists(args.map):
        encoder.load_encoding_map(args.map)
    
    if args.batch and os.path.isdir(args.input):
        # Process all PDDL files in the directory
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        
        for filename in os.listdir(args.input):
            if filename.endswith('.pddl'):
                input_path = os.path.join(args.input, filename)
                output_path = os.path.join(args.output, filename)
                
                if args.decode:
                    encoder.decode_pddl_file(input_path, output_path)
                    print(f"Decoded {input_path} -> {output_path}")
                else:
                    encoder.process_pddl_file(input_path, output_path)
                    print(f"Processed {input_path} -> {output_path}")
    else:
        # Process a single file
        if args.decode:
            encoder.decode_pddl_file(args.input, args.output)
            print(f"Decoded {args.input} -> {args.output}")
        else:
            encoder.process_pddl_file(args.input, args.output)
            print(f"Processed {args.input} -> {args.output}")
    
    # Save the encoding map if requested
    if args.map:
        encoder.save_encoding_map(args.map)
        print(f"Saved encoding map to {args.map}")


if __name__ == "__main__":
    main()