import bpy
from .properties.custo_label_properties import update_node_label_categories

class UI_RefreshLabelDefinition(bpy.types.Operator):
	bl_idname = "object.refresh_label_definition"
	bl_label = "Refresh Part labels"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Refresh Part Labels from the Label Definition"


	def execute(self, context):
		if context.object is None:
			return {'FINISHED'}
		# print(f'refreshing {context.object.name} part slots')
		
		for lc in context.scene.custo_handler_settings.custo_label_categories:
			# print(s.name)
			if lc.name not in context.object.custo_label_category_definition:
				self.add_label_category(context.object.custo_label_category_definition, lc)
			else:
				self.edit_label_category(context.object.custo_label_category_definition, lc)
			
			for s in context.object.material_slots:
				if s.material is None:
					continue
				
				if lc.name not in s.material.custo_label_category_definition:
					self.add_label_category(s.material.custo_label_category_definition, lc)
				else:
					self.edit_label_category(s.material.custo_label_category_definition, lc)
		
		self.clean_label_category(context.object.custo_label_category_definition)
		for s in context.object.material_slots:
			if s.material is None:
				continue
			self.clean_label_category(s.material.custo_label_category_definition)
		
		self.reorder_label_category(context, context.object.custo_label_category_definition)
		for s in context.object.material_slots:
			if s.material is None:
				continue
			self.reorder_label_category(context,s.material.custo_label_category_definition)

        # Update Node Label Category
		for asset_type in context.scene.custo_handler_settings.custo_asset_types:
			update_node_label_categories(asset_type.name)
			
		return {'FINISHED'}
	
	def add_label_category(self, prop, label_category):
		# print(f'adding {lc.name}')
		lcategory = prop.add()
		lcategory.name = label_category.name
		for l in label_category.labels:
			# print(f'adding {l.name}')
			label = lcategory.labels.add()
			label.name = l.name

	def edit_label_category(self, prop, label_category):
		olc = prop[label_category.name].labels
		for l in label_category.labels:
			if l.name not in olc:
				# print(f'adding {l.name}')
				label = olc.add()
				label.name = l.name

	def clean_label_category(self, prop):
		for i, lc in enumerate(prop):
			if lc.name not in prop:
				prop.remove(i)
			if lc.name not in bpy.context.scene.custo_handler_settings.custo_label_categories:
				prop.remove(i)
	
	def reorder_label_category(self, context, prop):
		source_label_categories = []
		for lc in context.scene.custo_handler_settings.custo_label_categories:
			source_label_categories.append(lc.name)
		
		target_label_categories = []
		for lc in prop:
			target_label_categories.append(lc.name)
		
		# print(source_label_categories)
		# print(target_label_categories)

		for i, lc in enumerate(source_label_categories):
			if lc == target_label_categories[i]:
				continue
			
			# Get index of element to move
			src_index = target_label_categories.index(lc)
			target_label_categories.insert(i, target_label_categories.pop(src_index))

			# Move Element to the proper index
			# print(f'Moving "{lc}" from {src_index} to {i}')
			prop.move(src_index, i)

	
classes = ( UI_RefreshLabelDefinition, 
			)

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