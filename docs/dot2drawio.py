import sys
import pygraphviz as pgv
from xml.dom.minidom import Document

def generate_drawio(dot_file_path, drawio_file_path):
    try:
        # Load the .dot file and create a graph from it
        graph = pgv.AGraph(filename=dot_file_path)
    except Exception as e:
        print(f"Failed to load .dot file: {e}")
        return
    
    try:
        # Create a new XML document
        doc = Document()
        
        # Create the mxfile and diagram elements
        mxfile = doc.createElement('mxfile')
        mxfile.setAttribute('host', 'app.diagrams.net')
        doc.appendChild(mxfile)

        diagram = doc.createElement('diagram')
        diagram.setAttribute('name', 'Page-1')
        mxfile.appendChild(diagram)

        # Create the mxGraphModel element
        graph_model = doc.createElement('mxGraphModel')
        diagram.appendChild(graph_model)

        # Create the root element
        root = doc.createElement('root')
        graph_model.appendChild(root)

        # Add the base elements
        mxCell = doc.createElement('mxCell')
        mxCell.setAttribute('id', '0')
        root.appendChild(mxCell)

        mxCell = doc.createElement('mxCell')
        mxCell.setAttribute('id', '1')
        mxCell.setAttribute('parent', '0')
        root.appendChild(mxCell)

        # Create elements for each node in the graph
        node_id_map = {}  # To map node names to IDs
        for i, node in enumerate(graph.nodes(), start=2):
            node_id = str(i)
            node_id_map[node] = node_id
            
            node_element = doc.createElement('mxCell')
            node_element.setAttribute('id', node_id)
            node_element.setAttribute('value', node)
            node_element.setAttribute('style', 'shape=ellipse;fillColor=#FF0000;strokeColor=#000000;')
            node_element.setAttribute('vertex', '1')
            node_element.setAttribute('parent', '1')
            
            geometry = doc.createElement('mxGeometry')
            geometry.setAttribute('x', '20')
            geometry.setAttribute('y', str(40 * i))  # Spread nodes vertically
            geometry.setAttribute('width', '80')
            geometry.setAttribute('height', '40')
            geometry.setAttribute('as', 'geometry')
            
            node_element.appendChild(geometry)
            root.appendChild(node_element)

        # Create elements for each edge in the graph
        edge_id = len(graph.nodes()) + 2  # Start edge IDs after node IDs
        for edge in graph.edges():
            edge_element = doc.createElement('mxCell')
            edge_element.setAttribute('id', str(edge_id))
            edge_id += 1
            edge_element.setAttribute('value', '')
            edge_element.setAttribute('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;')
            edge_element.setAttribute('edge', '1')
            edge_element.setAttribute('source', node_id_map[edge[0]])
            edge_element.setAttribute('target', node_id_map[edge[1]])
            edge_element.setAttribute('parent', '1')
            
            edge_geometry = doc.createElement('mxGeometry')
            edge_geometry.setAttribute('relative', '1')
            edge_geometry.setAttribute('as', 'geometry')
            
            edge_element.appendChild(edge_geometry)
            root.appendChild(edge_element)

        # Write the XML document to the .drawio file
        with open(drawio_file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='  '))
    except Exception as e:
        print(f"Failed to write .drawio file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dot2drawio.py <dot_file>")
        sys.exit(1)
    
    dot_file_path = sys.argv[1]
    drawio_file_path = dot_file_path.replace('.dot', '.drawio')
    generate_drawio(dot_file_path, drawio_file_path)
