# PDDL Encoder Tool

A Python tool to encode names in PDDL (Planning Domain Definition Language) files while preserving keywords. The encoding is simple, short, and decoupled from the semantic context. Now supports reversible encoding and stochastic encoding for LLM training.

## Features

- Encodes names in domain, problem, and plan PDDL files
- Preserves all PDDL keywords
- Maintains consistent encoding between domain, problem, and plan files
- Supports batch processing of multiple files
- Supports JSON-based batch processing for domain-problem-plan tuples
- Can save and load encoding maps for reference
- Works with or without the PDDL parser library
- **Reversible encoding**: Decode encoded PDDL files back to their original form
- **Stochastic encoding**: Generate different encodings for the same file to enhance LLM training
- **Reproducible randomness**: Control stochasticity with seeds when needed for testing

## Installation

### Prerequisites

- Python 3.6 or higher

### Optional Dependencies

For enhanced parsing capabilities, you can install the PDDL parser library:

```bash
pip install pddl
```

If the PDDL parser is not available, the tool will fall back to a regex-based approach.

## Usage

### Basic Usage

```bash
python pddl_encoder.py input.pddl output.pddl
```

### Save Encoding Map

```bash
python pddl_encoder.py input.pddl output.pddl --map encoding_map.txt
```

### Process Multiple Files

```bash
python pddl_encoder.py input_dir/ output_dir/ --batch --map encoding_map.txt
```

### Custom Prefix

By default, encoded names use the prefix 'x'. You can change this:

```bash
python pddl_encoder.py input.pddl output.pddl --prefix e
```

### Decode Encoded Files

Convert encoded PDDL files back to their original form:

```bash
python pddl_encoder.py encoded.pddl decoded.pddl --map encoding_map.txt --decode
```

### Stochastic Encoding for LLM Training

Generate different encodings each time for the same file:

```bash
python pddl_encoder.py input.pddl output.pddl --stochastic
```

### Reproducible Stochastic Encoding

Use a seed to make stochastic encoding reproducible (useful for testing):

```bash
python pddl_encoder.py input.pddl output.pddl --stochastic --seed 42
```

### Decode Encoded Files

Convert encoded PDDL files back to their original form:

```bash
python pddl_encoder.py encoded.pddl decoded.pddl --map encoding_map.txt --decode
```

### Stochastic Encoding for LLM Training

Generate different encodings each time for the same file:

```bash
python pddl_encoder.py input.pddl output.pddl --stochastic
```

### JSON-based Batch Processing

Process multiple domain-problem-plan tuples using a JSON configuration file:

```bash
python batch_encoder.py config.json --input-dir example --output-dir example/encoded
```

Example JSON configuration file:
```json
[
    {
        "instruction": "Encode blocks world example",
        "input": {
            "domain": "blocks_domain.pddl",
            "problem": "blocks_problem.pddl",
            "plan": "blocks_plan.pddl"
        },
        "output": {
            "domain": "blocks_domain_encoded.pddl",
            "problem": "blocks_problem_encoded.pddl",
            "plan": "blocks_plan_encoded.pddl",
            "map": "blocks_encoding_map.txt"
        }
    }
]
```

### Reproducible Stochastic Encoding

Use a seed to make stochastic encoding reproducible (useful for testing):

```bash
python pddl_encoder.py input.pddl output.pddl --stochastic --seed 42
```

## Example

Original domain file (domain.pddl):
```
(define (domain blocks-world)
  (:requirements :strips :typing)
  (:types block table - object)
  (:predicates 
    (on ?x - block ?y - object)
    (clear ?x - object)
    (handempty)
  )
  
  (:action pickup
    :parameters (?x - block)
    :precondition (and (clear ?x) (on ?x table) (handempty))
    :effect (and (not (on ?x table)) (not (clear ?x)) (not (handempty)))
  )
)
```

Encoded domain file:
```
(define (domain x0)
  (:requirements :strips :typing)
  (:types x1 x2 - object)
  (:predicates 
    (x3 ?x - x1 ?y - object)
    (x4 ?x - object)
    (x5)
  )
  
  (:action x6
    :parameters (?x - x1)
    :precondition (and (x4 ?x) (x3 ?x x2) (x5))
    :effect (and (not (x3 ?x x2)) (not (x4 ?x)) (not (x5)))
  )
)
```

Original plan file (plan.pddl):
```
(pickup blockA)
(stack blockA blockB)
```

Encoded plan file:
```
(x6 x14)
(x11 x14 x15)
```

Encoding map (encoding_map.txt):
```
blocks-world	x0
block	x1
table	x2
on	x3
clear	x4
handempty	x5
pickup	x6
stack	x11
blockA	x14
blockB	x15
```

## License

MIT