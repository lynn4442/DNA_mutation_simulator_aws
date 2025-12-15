from flask import Flask, render_template, request, jsonify
import random
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server
import matplotlib.pyplot as plt

app = Flask(__name__)

rna_to_amino = {
    'AUA': 'I', 'AUC': 'I', 'AUU': 'I', 'AUG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',
    'AAC': 'N', 'AAU': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGU': 'S', 'AGA': 'R', 'AGG': 'R',
    'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P',
    'CAC': 'H', 'CAU': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R',
    'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',
    'GAC': 'D', 'GAU': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G',
    'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S',
    'UUC': 'F', 'UUU': 'F', 'UUA': 'L', 'UUG': 'L',
    'UAC': 'Y', 'UAU': 'Y', 'UAA': '_', 'UAG': '_',
    'UGC': 'C', 'UGU': 'C', 'UGA': '_', 'UGG': 'W',
}

sample_genes = {
    "Insulin": "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTC",
    "Hemoglobin": "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG",
    "BRCA1": "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTG",
    "p53": "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGCCGTCCCAA",
    "CFTR": "ATGCAGAGGTCGCCTCTGGAAAAGGCCAGCGTTGTCTCCAAACTTTTTTTCAGCTGGACCAGACCAATTTTGAGGAAAGGATACAGACAGCGCCTGGAATTGTCAGACATATACCA"
}

def make_random_dna(length=100):
    bases = ['A', 'T', 'G', 'C']
    dna = "ATG"
    for i in range(length - 3):
        dna = dna + random.choice(bases)
    return dna

def dna_to_rna(dna):
    rna = ""
    for base in dna:
        if base == 'T':
            rna = rna + 'U'
        else:
            rna = rna + base
    return rna

def dna_to_protein(dna):
    dna = dna.upper()
    rna = dna_to_rna(dna)
    start = rna.find('AUG')

    if start == -1:
        return "No start codon found"

    protein = ""
    i = start
    while i < len(rna) - 2:
        codon = rna[i:i+3]
        if len(codon) < 3:
            break
        if codon in rna_to_amino:
            amino = rna_to_amino[codon]
        else:
            amino = 'X'
        if amino == '_':
            break
        protein = protein + amino
        i = i + 3

    return protein

def create_mutation(dna):
    types = ["point", "insertion", "deletion"]
    mutation_type = random.choice(types)
    original_dna = dna

    if mutation_type == "point":
        position = random.randint(0, len(dna) - 1)
        old_base = dna[position]
        bases = ['A', 'T', 'G', 'C']
        bases.remove(old_base)
        new_base = random.choice(bases)
        mutated_dna = dna[:position] + new_base + dna[position+1:]
        description = f"Changed base at position {position} from {old_base} to {new_base}"

    elif mutation_type == "insertion":
        position = random.randint(0, len(dna))
        new_bases = ""
        for i in range(random.randint(1, 3)):
            new_bases = new_bases + random.choice(['A', 'T', 'G', 'C'])
        mutated_dna = dna[:position] + new_bases + dna[position:]
        description = f"Added {new_bases} at position {position}"

    else:  # deletion
        if len(dna) <= 3:
            # If DNA is too short, skip deletion and do a point mutation instead
            position = random.randint(0, len(dna) - 1)
            old_base = dna[position]
            bases = ['A', 'T', 'G', 'C']
            bases.remove(old_base)
            new_base = random.choice(bases)
            mutated_dna = dna[:position] + new_base + dna[position+1:]
            description = f"Changed base at position {position} from {old_base} to {new_base} (deletion skipped - sequence too short)"
        else:
            position = random.randint(0, len(dna) - 1)
            num_to_delete = min(3, len(dna) - position)
            if num_to_delete == 0:
                num_to_delete = 1
                position = max(0, position - 1)
            num_to_delete = random.randint(1, num_to_delete)
            deleted = dna[position:position+num_to_delete]
            mutated_dna = dna[:position] + dna[position+num_to_delete:]
            description = f"Removed {deleted} at position {position}"

    old_protein = dna_to_protein(original_dna)
    new_protein = dna_to_protein(mutated_dna)
    old_rna = dna_to_rna(original_dna)
    new_rna = dna_to_rna(mutated_dna)

    if old_protein == new_protein:
        effect = "unchanged"
    elif len(new_protein) < len(old_protein):
        effect = "shorter"
    elif len(new_protein) > len(old_protein):
        effect = "longer"
    else:
        effect = "changed"

    changes = 0
    for i in range(min(len(old_protein), len(new_protein))):
        if old_protein[i] != new_protein[i]:
            changes += 1

    return {
        "original_dna": original_dna,
        "mutated_dna": mutated_dna,
        "original_rna": old_rna,
        "mutated_rna": new_rna,
        "description": description,
        "mutation_type": mutation_type,
        "original_protein": old_protein,
        "mutated_protein": new_protein,
        "effect": effect,
        "amino_changes": changes,
        "position": position
    }

def generate_visualization(mutations):
    mutation_stats = {
        "types": [m["mutation_type"] for m in mutations],
        "positions": [m["position"] for m in mutations],
        "protein_effects": [m["effect"] for m in mutations],
        "amino_changes": [m["amino_changes"] for m in mutations]
    }

    if len(mutation_stats["types"]) == 0:
        return None

    plt.figure(figsize=(14, 10))

    # Plot 1: Mutation Types
    plt.subplot(2, 2, 1)
    types_count = {"point": 0, "insertion": 0, "deletion": 0}
    for t in mutation_stats["types"]:
        types_count[t] += 1
    plt.bar(types_count.keys(), types_count.values(), color=['blue', 'green', 'red'])
    plt.title('Types of Mutations', pad=15)
    plt.ylabel('Count')

    # Plot 2: Mutation Positions
    plt.subplot(2, 2, 2)
    plt.hist(mutation_stats["positions"], bins=10, color='orange')
    plt.title('Mutation Positions', pad=15)
    plt.xlabel('Position in DNA')
    plt.ylabel('Frequency')

    # Plot 3: Protein Effects
    plt.subplot(2, 2, 3)
    effects_count = {"unchanged": 0, "shorter": 0, "longer": 0, "changed": 0}
    for e in mutation_stats["protein_effects"]:
        effects_count[e] += 1
    plt.bar(effects_count.keys(), effects_count.values(), color=['green', 'red', 'blue', 'purple'])
    plt.title('Effects on Protein', pad=15)
    plt.ylabel('Count')

    # Plot 4: Amino Acid Changes
    plt.subplot(2, 2, 4)
    if len(mutation_stats["amino_changes"]) == 0:
        plt.text(0.5, 0.5, "No amino acid changes to display",
                horizontalalignment='center', verticalalignment='center')
        plt.title('Number of Amino Acid Changes', pad=15)
    else:
        max_change = max(mutation_stats["amino_changes"]) + 1
        plt.hist(mutation_stats["amino_changes"], bins=range(max_change + 1), color='purple')
        plt.title('Number of Amino Acid Changes', pad=15)
        plt.xlabel('Number of Changes')
        plt.ylabel('Frequency')

    plt.tight_layout(pad=4.0)

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return img_base64

@app.route('/')
def index():
    return render_template('index.html', genes=sample_genes)

@app.route('/mutate', methods=['POST'])
def mutate():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        gene_name = data.get('gene')
        custom_dna = data.get('custom_dna', '').upper()

        # Validate num_mutations
        try:
            num_mutations = int(data.get('num_mutations', 1))
            if num_mutations < 1 or num_mutations > 10:
                return jsonify({'error': 'Number of mutations must be between 1 and 10'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid number of mutations'}), 400

        # Get starting DNA
        if custom_dna:
            clean_dna = ''.join([c for c in custom_dna if c in 'ATGC'])
            if len(clean_dna) < 3:
                return jsonify({'error': 'DNA sequence too short (minimum 3 bases)'}), 400
            if not clean_dna.startswith('ATG'):
                clean_dna = 'ATG' + clean_dna
            current_dna = clean_dna
        elif gene_name in sample_genes:
            current_dna = sample_genes[gene_name]
        else:
            current_dna = make_random_dna(100)

        # Store starting DNA info
        starting_info = {
            'dna': current_dna,
            'rna': dna_to_rna(current_dna),
            'protein': dna_to_protein(current_dna)
        }

        # Generate mutations
        mutations = []
        for i in range(num_mutations):
            mutation = create_mutation(current_dna)
            mutations.append(mutation)
            current_dna = mutation['mutated_dna']

        # Generate visualization
        img_base64 = generate_visualization(mutations)

        return jsonify({
            'starting_info': starting_info,
            'mutations': mutations,
            'visualization': img_base64
        })

    except Exception as e:
        # Log the error in production, return generic message to user
        print(f"Error in /mutate endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

if __name__ == '__main__':
    # Debug mode should be False in production (Elastic Beanstalk sets FLASK_ENV)
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

# Required for AWS Elastic Beanstalk
application = app
