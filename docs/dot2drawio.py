# 1) Use an AI to write the DOT file format for the logic 
#    in the source code or in the text to analize.

# 2) Convert a DOT file to a draw.io or mermaid file, using this python script

# 3) Install DrawIO extension on VScode to open the file and modifiy it.


# sudo apt install python3-pip graphviz graphviz-dev
# pip3 install graphviz2drawio --upgrade
from graphviz2drawio import graphviz2drawio
import sys
import re

def convert_dot_to_mermaid(dot_file_path):
    with open(dot_file_path, 'r') as file:
        dot_content = file.read()

    # Remove the 'digraph G {' and '}' lines
    dot_content = re.sub(r'digraph \w+ \{', '', dot_content)
    dot_content = dot_content.replace('}', '')

    # Replace '->' with '-->'
    mermaid_content = dot_content.replace('->', '-->')

    # Add 'graph TD;' at the beginning and trim whitespace
    mermaid_content = 'graph TD;\n' + mermaid_content.strip()

    return mermaid_content


def main(dot_file_name):
    # Convert the DOT file to XML
    xml_content = graphviz2drawio.convert(dot_file_name)
    mermaid_content = convert_dot_to_mermaid(dot_file_name)
    
    # Construct the output XML file name by changing the.dot extension to.xml
    output_drawio_file_name = dot_file_name.replace('.dot', '.mermaid') 
    # Write the XML content to the output file
    with open(output_drawio_file_name, 'w') as f:
        f.write(xml_content)

    # Construct the output mermaid file name by changing the.dot extension to.drawio
    output_mermaid_file_name = dot_file_name.replace('.dot', '.drawio')
    # Write the mermaid content to the output file
    with open(output_mermaid_file_name, 'w') as f:
        f.write(mermaid_content)

if __name__ == "__main__":
    # Check if a DOT file name was provided as a command-line argument
    if len(sys.argv) > 1:
        dot_file_name = sys.argv[1]
        main(dot_file_name)
    else:
        print("Please provide a DOT file name as a command-line argument.")

  
  
  
  
