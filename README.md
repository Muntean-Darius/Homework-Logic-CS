## Overview
This program checks whether a given propositional formula is well-formed and evaluates its truth value based on a specified interpretation. It utilizes tree data structures to represent the formula and processes logical operations.

## Requirements
- Python 3.6 or higher
- `anytree` library

## Installation
To install the necessary tools for the program to work, follow these steps:

1. **Install Python**
   - Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install the `anytree` library**
   Open your terminal or command prompt and run the following command:
   ```
   pip install anytree

## How to use the program
Clone the repository (if applicable):

```
git clone <repository-url>
cd <repository-directory> 
```
Open the Python script: Open the script file containing the program in your preferred code editor.

Modify the input formulas: The list of propositional formulas is defined at the beginning of the script. You can modify the list l with any well-formed formulas you want to check.

Example:
```
l = [
    '((P⇒Q)∧((¬Q)∧(¬P)))',
    '((P⇒Q)⇒((Q⇒S)⇒((P∨Q)⇒R)))',
    ...
]
```
Run the program: Execute the script using Python:
```
python <script-name>.py
```
Interpretations: The script includes an example interpretation at the bottom, which you can uncomment and modify. Add more interpretations as needed:

```
interpretation({'P': True, 'Q': True}, root)
interpretation({'P': True, 'Q': False}, root)
```
Example of interpretation output
```
⇔
├── P
└── Q
¬
└── Q
⇒
├── P
└── ¬
    └── Q
¬
└── ⇒
    ├── P
    └── ¬
        └── Q
⇔
├── ⇔
│   ├── P
│   └── Q
└── ¬
    └── ⇒
        ├── P
        └── ¬
            └── Q
We introduce the truth values into the tree
⇔
├── ⇔
│   ├── True
│   └── True
└── ¬
    └── ⇒
        ├── True
        └── ¬
            └── True
The value of the proposition is True for the interpretation: {'P': True, 'Q': True}
```
Example of Program Output
When you run the program, it will check each formula in the list l and print whether it is well-formed or not. For example:
```
((P⇒Q)∧((¬Q)∧(¬P))): 
We check if it has the correct number of binary operators for the number of variables

This proposition has the correct number of binary operators: 4 variables and 3 binary operators

We check if it has the correct number of parentheses for the number of variables

This proposition has the correct number of parentheses: '()'-5 and 5 operators

We check if the proposition has the correct arrangement of elements

Arrangement is correct
The proposition is a well formed propositional formulae
⇒
├── P
└── Q
¬
└── Q
¬
└── P
∧
├── ¬
│   └── Q
└── ¬
    └── P
∧
├── ⇒
│   ├── P
│   └── Q
└── ∧
    ├── ¬
    │   └── Q
    └── ¬
        └── P
```

