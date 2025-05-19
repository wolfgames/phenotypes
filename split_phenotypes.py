import re
import os
import sys

def split_phenotypes(input_filepath, output_dir="PHENO"):
    """
    Reads a markdown file, splits it by phenotype markers, and saves
    each phenotype to a separate file in the specified output directory.
    """
    try:
        with open(input_filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        sys.exit(1)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Regex to find phenotype blocks
    # It looks for lines starting with {# PHENOTYPE: ... #} and {# END_PHENOTYPE: ... #}
    # and captures the phenotype name.
    phenotype_pattern = re.compile(r'^{# PHENOTYPE: (.*?) #}(.*?)^{# END_PHENOTYPE: \1 #}', re.DOTALL | re.MULTILINE)

    matches = phenotype_pattern.findall(content)

    if not matches:
        print("No phenotype markers found in the file.")
        return

    for phenotype_name, phenotype_content in matches:
        # Clean up the phenotype name for filename
        filename = f"{phenotype_name.strip()}.md"
        output_filepath = os.path.join(output_dir, filename)

        # Remove leading line numbers and pipe characters from the content
        cleaned_content = re.sub(r'^\s*\d+\s*\|\s*', '', phenotype_content, flags=re.MULTILINE)

        try:
            with open(output_filepath, 'w') as outfile:
                # Add the phenotype marker back to the beginning of the individual file
                outfile.write(f"{{# PHENOTYPE: {phenotype_name.strip()} #}}\n\n")
                outfile.write(cleaned_content.strip())
                outfile.write(f"\n\n{{# END_PHENOTYPE: {phenotype_name.strip()} #}}\n")
            print(f"Saved {filename}")
        except IOError as e:
            print(f"Error writing file {output_filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_phenotypes.py <input_markdown_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    split_phenotypes(input_file)