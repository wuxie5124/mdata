import networkx as nx
import matplotlib.pyplot as plt

data = r"D:\DATA\海图\S127\S-127-1.0.0 SampleData\MTM_ROOT\127JS00EX_A0001\127JS00EX_A0001.GML"
Graph=nx.read_gml(data,label='id')
nx.draw(Graph, with_labels=True)
plt.show()