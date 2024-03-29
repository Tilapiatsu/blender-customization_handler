import bpy

def get_slot(context):
	idx = context.scene.custo_handler_settings.custo_slots_idx
	slots = context.scene.custo_handler_settings.custo_slots

	active = slots[idx] if len(slots) else None

	return idx, slots, active


class UI_MoveSlot(bpy.types.Operator):
	bl_idname = "scene.move_customization_slot"
	bl_label = "Move Slot"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Slot up or down.\nThis controls the position in the List."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_slots)

	def execute(self, context):
		idx, slot, _ = get_slot(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(slot) - 1)

		slot.move(idx, nextidx)
		context.scene.custo_handler_settings.custo_slots_idx = nextidx

		return {'FINISHED'}


class UI_ClearSlots(bpy.types.Operator):
	bl_idname = "scene.clear_customization_slots"
	bl_label = "Clear All Slots"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Slots"

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_slots)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		context.scene.custo_handler_settings.custo_slots.clear()
		bpy.ops.object.refresh_part_slots()
		return {'FINISHED'}


class UI_RemoveSlot(bpy.types.Operator):
	bl_idname = "scene.remove_customization_slot"
	bl_label = "Remove Selected Slot"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected slot"
	
	index : bpy.props.IntProperty(name="slot index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_slots
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		_, slots, _ = get_slot(context)

		slots.remove(self.index)

		context.scene.custo_handler_settings.custo_slots_idx = min(self.index, len(context.scene.custo_handler_settings.custo_slots) - 1)

		bpy.ops.object.refresh_part_slots()
		return {'FINISHED'}


class UI_DuplicateSlot(bpy.types.Operator):
	bl_idname = "scene.duplicate_customization_slot"
	bl_label = "Duplicate Selected Slot"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Slot"
	
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_slots

	def execute(self, context):
		_, slot, _ = get_slot(context)

		s = slot.add()
		s.name = slot[self.index].name+'_dup'
		slot.move(len(slot) - 1, self.index + 1)
		bpy.ops.object.refresh_part_slots()
		return {'FINISHED'}


class UI_EditSlot(bpy.types.Operator):
	bl_idname = "scene.edit_customization_slot"
	bl_label = "Edit Slot"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current customization slot"

	index : bpy.props.IntProperty(name="Slot Index", default=0)
	name : bpy.props.StringProperty(name="Slot Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Slot Name')
	
	def invoke(self, context, event):
		current_slot = context.scene.custo_handler_settings.custo_slots[self.index]
		self.name = current_slot.name
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=500)
	
	def execute(self, context):
		s = context.scene.custo_handler_settings.custo_slots[self.index]
		s.name = self.name
		bpy.ops.object.refresh_part_slots()
		return {'FINISHED'}


class UI_AddSlot(bpy.types.Operator):
	bl_idname = "scene.add_customization_slot"
	bl_label = "Add Slot"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a customization slot"

	name : bpy.props.StringProperty(name="Slot Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='name')

	def invoke(self, context, event):
		wm = context.window_manager
		self.name = ''
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		s = context.scene.custo_handler_settings.custo_slots.add()
		s.name = self.name
		bpy.ops.object.refresh_part_slots()
		return {'FINISHED'}

classes = ( UI_MoveSlot, 
            UI_EditSlot, 
            UI_ClearSlots, 
            UI_AddSlot,
            UI_RemoveSlot,
            UI_DuplicateSlot)

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