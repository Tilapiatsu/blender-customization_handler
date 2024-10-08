import bpy
from bpy.types import NodeTree
from .node_const import TREE_NAME

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class CustomizationTree(NodeTree):
	# Description string
	'''Let you define the rules for assembling the final asset'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = TREE_NAME
	# Label for nice name display
	bl_label = "Customization Tree"
	# Icon identifier
	bl_icon = 'NODETREE'

	asset_type : bpy.props.StringProperty(name='Asset Type', default='Asset Type')
	
	@property
	def custo_nodes(self):
		return [n for n in self.nodes if n.bl_static_type not in ['REROUTE', 'FRAME']]
	
	@property
	def priority_range(self):
		r = [0, 0]
		for n in self.custo_nodes:
			if n.mute or not len(n.assets):
				continue
			r[0] = min(n.priority, r[0])
			r[1] = max(n.priority, r[1])

		return tuple(r)

	
	def draw(self, context):
		if bpy.context.space_data.tree_type != TREE_NAME or bpy.context.space_data.edit_tree is None:
			return
		self.layout.prop_search(bpy.context.space_data.edit_tree, "asset_type", context.scene.custo_handler_settings, "custo_asset_types", text='')


classes = ( CustomizationTree,
			)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	
	bpy.types.NODE_HT_header.prepend(CustomizationTree.draw)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

	bpy.types.NODE_HT_header.remove(CustomizationTree.draw)

if __name__ == "__main__":
	register()