import matplotlib.pyplot as plt
import networkx as nx
import xml.etree.ElementTree as ET
import geopandas as gpd
import numpy as np
from shapely.ops import unary_union
from shapely.geometry import Polygon
import math

# Load data from XML
tree = ET.parse('graph_files/King_county_NG911.graphml')
root = tree.getroot()

# Initialize the network graph
G = nx.DiGraph()

# Type attribute key
type_attribute_key = 'type'
# Namespace from root
nsmap = {'xmlns': 'http://graphml.graphdrawing.org/xmlns'}

node_positions = {}
psap_ids = []
psap_coordinates = []
calr_nodes = []
caller_region_patches = []

region_string = []  # stores the strings of squares that will be set as caller region attributes

out_file_name = "King_county_NG911"

square_counter = 0

psap_layer = gpd.read_file("GIS_data/Layers/PSAP_layer.gpkg")
provisioning_layer = gpd.read_file("GIS_data/Layers/Provisioning_layer.gpkg")

    # create series of boolean values denoting whether geometry is within King County
psap_within_kc = psap_layer.within(provisioning_layer.iloc[21].geometry)

    # create new GeoDataFrames of just items located within King County using series above
kc_psap = psap_layer.drop(np.where(psap_within_kc == False)[0])


    # area_multiplier gets multiplied by the smallest psap area to determine size of the squares in the grid
area_multiplier = 10

    # Some of the data from the state had messed up psap names. This line fixes them so they can be consolidated
kc_psap.loc[[265, 262, 185], 'DsplayName'] = "King County Sheriff's Office - Marine Patrol"

names = [] # 2 empty lists for storing names and polygons for merging psaps together
polys = []
es_nguid = [] # list for storing the nguids

    # Loops through and finds all unique names, as well as sorting all the polygons that make up those regions
for n in range(kc_psap.shape[0]):
    if (kc_psap.iloc[n].DsplayName) in names:
        polys[names.index(kc_psap.iloc[n].DsplayName)].append(kc_psap.iloc[n].geometry)
    else:
        names.append(kc_psap.iloc[n].DsplayName)
        polys.append([kc_psap.iloc[n].geometry])
        es_nguid.append(kc_psap.iloc[n].ES_NGUID)

    # Takes the lists of polygons, and merges them into new polygons for the creation of the merged_kc_psap GeoDataFrame
merged_polys = []
for m in range(len(polys)):
    merged_polys.append(unary_union(polys[m]))

    # Create a new GeoDataFrame with the unique names and merged geometries
merged_kc_psap = gpd.GeoDataFrame({'DisplayName': names, 'geometry': merged_polys, 'ES_NGUID': es_nguid}, crs=kc_psap.crs)

    # Find the area of the smallest merged psap, use that to determine the square size
areas = merged_kc_psap.area
side_length = math.sqrt(areas.min() * area_multiplier)

    # Creates a grid of squares based on the bounds of merged_kc_psaps, and the side_length
xmin, ymin, xmax, ymax = merged_kc_psap.total_bounds
cols = list(np.arange(xmin, xmax + side_length, side_length))
rows = list(np.arange(ymin, ymax + side_length, side_length))
squares = []
for x in cols[:-1]:
    for y in rows[:-1]:
        squares.append(
            Polygon([(x, y), (x + side_length, y), (x + side_length, y + side_length), (x, y + side_length)]))
grid = gpd.GeoDataFrame({'geometry': squares}, crs=kc_psap.crs)
kc_psap.plot()

#stores all PSAP nodes
for node in root.findall('.//{http://graphml.graphdrawing.org/xmlns}node'):
    type_element = node.find(f'.//{{{nsmap["xmlns"]}}}data[@key="{type_attribute_key}"]')
    if type_element is not None and type_element.text == 'PSAP':
        node_id = node.get('id')
        psap_ids.append(node_id)

        for data in node.findall(f'.//{{{nsmap["xmlns"]}}}data', namespaces=nsmap):
            if data.get('key') == 'x':
                node_x = float(data.text)
                psap_coordinates.append(node_x)
            elif data.get('key') == 'y':
                node_y = float(data.text)
                psap_coordinates.append(node_y)

        if 'node_x' in locals() and 'node_y' in locals():
            G.add_node(node_id)
            node_positions[node_id] = (node_x, node_y)
            G.nodes[node_id]['pos'] = (node_x, node_y)
            G.nodes[node_id]['color'] = 'cyan'
    #find all EMS nodes
    elif type_element is not None and type_element.text == 'EMS':
        node_id = node.get('id')

        for data in node.findall(f'.//{{{nsmap["xmlns"]}}}data', namespaces = nsmap):
            if data.get('key') == 'x':
                node_x = float(data.text)
            if data.get('key') == 'y':
                node_y = float(data.text)

        if 'node_x' in locals() and 'node_y' in locals():
            G.add_node(node_id)
            node_positions[node_id] = (node_x, node_y)
            G.nodes[node_id]['pos'] = (node_x, node_y)
            G.nodes[node_id]['color'] = 'blue'




for node in root.findall('.//{http://graphml.graphdrawing.org/xmlns}node'):
    type_element = node.find(f'.//{{{nsmap["xmlns"]}}}data[@key="{type_attribute_key}"]')
    if type_element is not None and type_element.text == 'CALR':
        node_id = node.get('id')
        calr_nodes.append(node_id)

        segments_data = node.find(f'.//{{{nsmap["xmlns"]}}}data[@key="segments"]')
        if segments_data is not None:
            segments_str = segments_data.text
            segments_str = segments_str.replace("[(", "").replace(")]", "")
            segments_list = segments_str.split("), (")

            # Convert segments into a list of coordinate tuples
            coordinates = [tuple(map(float, segment.split(", "))) for segment in segments_list]

            # Calculate the average position as the node position- this should be the center of the region- can map 
            # onto the graph
            avg_x = sum(coord[0] for coord in coordinates) / len(coordinates)
            avg_y = sum(coord[1] for coord in coordinates) / len(coordinates)

            G.add_node(node_id)
            node_positions[node_id] = (avg_x, avg_y)
            G.nodes[node_id]['pos'] = (avg_x, avg_y)
            G.nodes[node_id]['color'] = 'green' 



for edge in root.findall('.//{http://graphml.graphdrawing.org/xmlns}edge'):
    edge_source = edge.get('source')
    edge_target = edge.get('target')

    # Check if both source and target nodes are in G
    if edge_source in G.nodes() and edge_target in G.nodes():
        G.add_edge(edge_source, edge_target)
# Create the combined plot
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the network graph
edge_alpha = 0.4
default_node_color = 'gray' 
node_colors = [G.nodes[node_id].get('color', default_node_color) for node_id in G.nodes()]
nx.draw(G, node_size=30, pos=node_positions, node_color=node_colors, with_labels=False,
        alpha=edge_alpha, width=0.3, ax=ax)

label_pos = {k: (v[0], v[1] + 0.01) for k, v in node_positions.items()}  
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=8, ax=ax)

# Plot the GIS map without the grid
kc_psap.plot(ax=ax, color='none', edgecolor='black')

# Show the combined plot
plt.show()