from . import custo_label_properties, custo_slot_properties, custo_asset_properties, custo_object_property

def register():
    custo_object_property.register()
    custo_label_properties.register()
    custo_slot_properties.register()
    custo_asset_properties.register()

def unregister():
    custo_asset_properties.unregister()
    custo_slot_properties.unregister()
    custo_label_properties.unregister()
    custo_object_property.unregister()
