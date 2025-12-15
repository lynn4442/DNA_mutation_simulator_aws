# DNA Mutation Simulator

A web-based DNA mutation simulator that visualizes how different types of mutations (point mutations, insertions, and deletions) affect DNA sequences, RNA transcription, and protein translation.

## Features

- **Multiple Mutation Types**: Simulates point mutations, insertions, and deletions
- **Real Gene Examples**: Pre-loaded with real gene sequences (Insulin, Hemoglobin, BRCA1, p53, CFTR)
- **Custom DNA Input**: Enter your own DNA sequences for analysis
- **Visual Analytics**: Automatically generates charts showing:
  - Distribution of mutation types
  - Mutation positions along the sequence
  - Effects on protein structure
  - Amino acid changes
- **Responsive Design**: Modern, mobile-friendly interface using Bootstrap 5

## Project Structure

```
DNA_mutation_simulator_aws/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web interface template
├── .ebextensions/
│   └── 01_flask.config        # AWS Elastic Beanstalk configuration
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## How It Works

1. **DNA to RNA**: Transcribes DNA by replacing thymine (T) with uracil (U)
2. **RNA to Protein**: Translates RNA codons into amino acids using the genetic code
3. **Mutations**: Randomly generates mutations that modify the DNA sequence
4. **Analysis**: Compares original and mutated sequences to show the impact

### Mutation Types

- **Point Mutation**: Single nucleotide base change (e.g., A → G)
- **Insertion**: Addition of 1-3 nucleotides
- **Deletion**: Removal of 1-3 nucleotides

## Local Development Setup

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   # For development (with debug mode)
   export FLASK_ENV=development
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## AWS Elastic Beanstalk Deployment

### Prerequisites

- AWS Account
- EB CLI installed (`pip install awsebcli`)

### Deployment Steps

1. Initialize Elastic Beanstalk:
   ```bash
   eb init -p python-3.12 dna-mutation-simulator
   ```

2. Create an environment and deploy:
   ```bash
   eb create dna-mutation-env
   ```

3. Open the application:
   ```bash
   eb open
   ```

### Update Deployment

After making changes:
```bash
eb deploy
```

### Monitor Logs

```bash
eb logs
```

## Usage

### Using Pre-loaded Genes

1. Select a gene from the dropdown (Insulin, Hemoglobin, BRCA1, p53, or CFTR)
2. Choose the number of mutations (1-10)
3. Click "Generate Mutations"
4. View the results showing original vs mutated sequences and statistics

### Using Custom DNA

1. Select "Custom DNA" from the dropdown
2. Enter your DNA sequence (only A, T, G, C bases)
   - The start codon (ATG) will be added automatically if not present
   - Minimum 3 bases required
3. Choose the number of mutations (1-10)
4. Click "Generate Mutations"

### Using Random DNA

1. Select "Random DNA" from the dropdown
2. A random 100-base sequence will be generated (starting with ATG)
3. Choose the number of mutations
4. Click "Generate Mutations"

## API Endpoints

### GET /
Returns the main HTML interface

### POST /mutate
Generates mutations for a DNA sequence

**Request Body:**
```json
{
  "gene": "Insulin",           // Optional: gene name or "random"
  "custom_dna": "ATGCGT...",   // Optional: custom DNA sequence
  "num_mutations": 3            // Required: 1-10
}
```

**Response:**
```json
{
  "starting_info": {
    "dna": "ATGCGT...",
    "rna": "AUGCGU...",
    "protein": "MR..."
  },
  "mutations": [
    {
      "mutation_type": "point",
      "description": "Changed base at position 5 from T to G",
      "original_dna": "ATGCGT...",
      "mutated_dna": "ATGCGG...",
      "original_protein": "MR...",
      "mutated_protein": "MR...",
      "effect": "unchanged",
      "amino_changes": 0,
      "position": 5
    }
  ],
  "visualization": "base64_encoded_image"
}
```

## Technologies Used

- **Backend**: Flask 3.1.2
- **Data Visualization**: Matplotlib 3.10.8
- **Numerical Computing**: NumPy 1.26.4
- **Frontend**: Bootstrap 5.3.2, Vanilla JavaScript
- **Deployment**: AWS Elastic Beanstalk

## Error Handling

The application includes comprehensive error handling:
- Invalid DNA sequences are rejected with clear error messages
- Number of mutations is validated (must be 1-10)
- Custom DNA must be at least 3 bases long
- Edge cases in deletion mutations are handled gracefully

## Security Notes

- Debug mode is automatically disabled in production
- Input validation prevents invalid data from being processed
- Error messages don't expose sensitive system information

## Contributing

Feel free to submit issues or pull requests to improve the simulator.

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Genetic code table based on standard codon usage
- Sample gene sequences from public databases
