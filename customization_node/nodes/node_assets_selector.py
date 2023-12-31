import bpy
import numpy as np
from bpy.types import Node
from .node import CustomizationTreeNode

class AssetsSelectorNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Selector node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsSelectorNodeType'
	# Label for nice name display
	bl_label = "Asset Selector"
	# Icon identifier
	bl_icon = 'NODETREE'

	subsockets = {'Spawn Rate': ['PercentageSocketType', False]}
	
	@property
	def label_names(self):
		return [l.name for l in self.labels]

	def init(self, context):
		self.inputs.new('AssetsSocketType', "Assets")
		for name,socket in self.subsockets.items():
			input = self.inputs.new(socket[0], name)
			input.hide = socket[1]
		self.outputs.new('AssetsSocketType', "Assets")

	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		self.layout_header(layout, context, asset_count=False)
	
	def draw_labels(self, layout):
		row = layout.row(align=True)
		rows = 20 if len(self.labels) > 20 else len(self.labels) + 3
		row.template_list('NODE_UL_AssetPercentageNode', '', self, 'labels', self, 'labels_idx', rows=rows)


	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Asset Selector"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		CustomizationTreeNode.update_inputs(self, 'AssetsSocketType', "Assets", sub_socket_dict=self.subsockets)
	
	def get_assets(self):
		spawn_rates = {sr: self.inputs[i-1] for i,sr in enumerate(self.inputs) if (i % 2) and self.inputs[i-1].is_linked}

		input_socket = self.random_pick_by_percentage(spawn_rates)
		
		if input_socket is None:
			return []
		
		input_node = input_socket.links[0].from_node
		input_assets = input_node.get_assets()

		return input_assets
	
	def random_pick_by_percentage(self, spawn_rate_dict):
		weights, value = zip(*spawn_rate_dict.items())
		weights = [w.input_value for w in weights]
		probs = np.array(weights, dtype=float) / float(sum(weights))

		try:
			choice = np.random.choice(value, 1, p=probs)[0]
		except ValueError:
			choice = None

		return choice
	
classes = ( AssetsSelectorNode,)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)


def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()