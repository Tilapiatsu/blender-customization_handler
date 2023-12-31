from . import node_assets_append, node_assets_filter_by_labels, node_assets_get_from_collection, node_assets_selector
from . import operators

def register():
    operators.register()
    node_assets_append.register()
    node_assets_filter_by_labels.register()
    node_assets_get_from_collection.register()
    node_assets_selector.register()


def unregister():
    node_assets_selector.unregister()
    node_assets_get_from_collection.unregister()
    node_assets_filter_by_labels.unregister()
    node_assets_append.unregister()
    operators.unregister()
