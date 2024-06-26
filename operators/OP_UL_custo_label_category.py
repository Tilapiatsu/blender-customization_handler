import bpy
from .properties.custo_label_properties import label_categories_enum

def get_label_category(context):
	idx = context.scene.custo_handler_settings.custo_label_categories_idx
	label_categories = context.scene.custo_handler_settings.custo_label_categories

	active = label_categories[idx] if len(label_categories) else None

	return idx, label_categories, active


class UI_MoveLabelCategory(bpy.types.Operator):
	bl_idname = "scene.move_customization_label_category"
	bl_label = "Move Label Category"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Label_category up or down.\nThis controls the position in the List."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_label_categories) and context.scene.custo_handler_settings.custo_label_categories_idx > -1 and context.scene.custo_handler_settings.custo_label_categories_idx < len(context.scene.custo_handler_settings.custo_label_categories)

	def execute(self, context):
		idx, label_category, _ = get_label_category(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(label_category) - 1)

		label_category.move(idx, nextidx)
		context.scene.custo_handler_settings.custo_label_categories_idx = nextidx

		return {'FINISHED'}


class UI_ClearLabelCategories(bpy.types.Operator):
	bl_idname = "scene.clear_customization_label_categories"
	bl_label = "Clear All Label Categories"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Label_categories"

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_label_categories)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		context.scene.custo_handler_settings.custo_label_categories.clear()
		bpy.ops.object.refresh_label_definition('EXEC_DEFAULT')
		return {'FINISHED'}


class UI_RemoveLabelCategory(bpy.types.Operator):
	bl_idname = "scene.remove_customization_label_category"
	bl_label = "Remove Selected Label Category"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected label_category"
	
	index : bpy.props.IntProperty(name="label_category index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_label_categories
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		_, label_categories, _ = get_label_category(context)

		label_categories.remove(self.index)

		context.scene.custo_handler_settings.custo_label_categories_idx = min(self.index, len(context.scene.custo_handler_settings.custo_label_categories) - 1)
		bpy.ops.object.refresh_label_definition('EXEC_DEFAULT')
		return {'FINISHED'}


class UI_DuplicateLabelCategory(bpy.types.Operator):
	bl_idname = "scene.duplicate_customization_label_category"
	bl_label = "Duplicate Selected Label Category"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Label_category"
	
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_label_categories

	def execute(self, context):
		_, label_category, _ = get_label_category(context)

		s = label_category.add()
		s.name = label_category[self.index].name+'_dup'
		self.duplicate_labels(label_category[self.index].labels, s.labels)
		label_category.move(len(label_category) - 1, self.index + 1)
		bpy.ops.object.refresh_label_definition('EXEC_DEFAULT')
		return {'FINISHED'}

	def duplicate_labels(self, source, destination):
		for l in source:
			label = destination.add()
			label.name = l.name


class UI_EditLabelCategory(bpy.types.Operator):
	bl_idname = "scene.edit_customization_label_category"
	bl_label = "Edit Label Category"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current customization label_category"

	index : bpy.props.IntProperty(name="Label_category Index", default=0)
	name : bpy.props.StringProperty(name="Label_category Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Label_category Name')
	
	def invoke(self, context, event):
		current_label_category = context.scene.custo_handler_settings.custo_label_categories[self.index]
		self.name = current_label_category.name
		self.old_name = current_label_category.name
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=500)
	
	def execute(self, context):
		s = context.scene.custo_handler_settings.custo_label_categories[self.index]
		s.name = self.name
		self.refresh_asset_type_label_categories(context)
		bpy.ops.object.refresh_label_definition('EXEC_DEFAULT')
		return {'FINISHED'}
	
	def refresh_asset_type_label_categories(self, context):
		for asset_type in context.scene.custo_handler_settings.custo_asset_types:
			lc = asset_type.asset_label_category.label_category
			if lc.name == self.old_name:
				lc.name = self.name

			for lcp in asset_type.mesh_variation_label_categories:
				lc = lcp.label_category
				if lc.name == self.old_name:
					lc.name = self.name
			
			if asset_type.mesh_slot_label_category.name == self.old_name:
				asset_type.mesh_slot_label_category.name = self.name

			if asset_type.material_label_category.name == self.old_name:
				asset_type.material_label_category.name = self.name
			
			for lc in asset_type.material_variation_label_categories:
				if lc.name == self.old_name:
					lc.name = self.name
		
		for o in bpy.data.objects:
			for lc in o.custo_label_category_definition:
				if lc.name == self.old_name:
					lc.name = self.name
		
		for m in bpy.data.materials:
			for lc in m.custo_label_category_definition:
				if lc.name == self.old_name:
					lc.name = self.name


class UI_AddLabelCategory(bpy.types.Operator):
	bl_idname = "scene.add_customization_label_category"
	bl_label = "Add Label Category"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a customization label_category"

	name : bpy.props.StringProperty(name="Label_category Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='name')

	def invoke(self, context, event):
		wm = context.window_manager
		self.name = ''
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		s = context.scene.custo_handler_settings.custo_label_categories.add()
		s.name = self.name
		bpy.ops.object.refresh_label_definition('EXEC_DEFAULT')
		return {'FINISHED'}
	
classes = ( UI_MoveLabelCategory, 
			UI_EditLabelCategory, 
			UI_ClearLabelCategories, 
			UI_AddLabelCategory, 
			UI_RemoveLabelCategory,
			UI_DuplicateLabelCategory)

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