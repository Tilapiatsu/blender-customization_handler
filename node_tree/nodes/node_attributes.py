import bpy
from ...operators.properties.custo_asset_properties import CustoAssetProperties
from ...attributes.binary_labels.binary_labels import LabelCombinaison, LabelVariation, LabelCategory, BinaryLabel
from ...attributes.property_override.property_override import PropertyOverride
# from .node_const import NODE_ATTRIBUTE_TARGETS
from dataclasses import dataclass, field

@dataclass
class NodeAttributes:
	labels : dict = field(default_factory=dict)

	# Decorator
	def create_target(func):
		def create(self, *args, **kwargs):
			target = args[0]
			if target not in self.labels.keys():
				self.labels[target] = LabelCombinaison()

			res = func(self, *args, **kwargs)
			return res

		return create

	@create_target
	def add_label(self, target:str, category:str, name:str, value:bool, weight:bool=1.0, valid_any:bool=False, unique:bool=False):
		self.labels[target].add_label(category=category, name=name, value=value, weight=weight, valid_any=valid_any, replace=unique)

	@create_target
	def add_labels(self, target:str, labels:dict, unique:bool=False):
		for lc, l in labels.items():
			self.add_label(target, lc, name=l.name, value=l.value, valid_any=l.valid_any, unique=unique)

	@create_target
	def add_label_combinaison(self, target:str, label_combinaison:LabelCombinaison):
		for lc, l in label_combinaison.items():
			self.add_label(target, lc, l.name, l.value, valid_any=l.valid_any, unique=True)
	
	def get_labels(self, target:str, label_categories:list=None):
		labels = LabelCombinaison()
		
		if target not in self.labels.keys():
			return labels
		
		for lc in self.labels[target].keys():
			if label_categories is not None:
				if lc not in label_categories:
					continue
			labels.add_binary_labels(lc, self.labels[target][lc].values())

		return labels

	def __str__(self):
		return f'Attributes : {self.labels}'
	
	def items(self):
		items = self.labels.items()
		return items
	
	def keys(self):
		return self.labels.keys()
	
	def values(self):
		return self.labels.values()
	
	def __len__(self):
		return len(self.labels.keys())
	
	def __iter__(self):
		yield len(self.labels.values())
		yield from self.labels.values()

	def __getitem__(self, key):
		return self.labels[key]
	
	def __setitem__(self, key, value):
		if isinstance(value, LabelCategory):
			self.categories[key] = value
		elif isinstance(value, BinaryLabel):
			self.add_binary_label(key, value, replace=True)
		else:
			print('Wrong Format Inputed')
		
	def __contains__(self, item:str):
		for l in self.labels.values():
			if l.name == item:
				return True
		return False

@dataclass
class NodeOverride():
	overrides : PropertyOverride = field(default_factory=PropertyOverride)

	def add_override(self, target:str, value_type:str, label:str, name:str, value:any, weight:float=1.0, replace:bool=True):
		self.overrides.add_property(target=target, value_type=value_type, label=label, name=name, value=value, weight=weight, replace=replace)

	def __str__(self):
		return f'Overrides : {self.overrides}'
	
	def remove(self, name):
		self.overrides.remove(name)


	def items(self):
		items = self.overrides.properties.items()
		return items
	
	def keys(self):
		return self.overrides.keys()
	
	def values(self):
		return self.overrides.values()
	
	def __len__(self):
		return len(self.overrides.keys())
	
	def __iter__(self):
		yield len(self.overrides.values())
		yield from self.overrides.values()

	def __getitem__(self, key):
		return self.overrides[key]
		
	def __contains__(self, item:str):
		for o in self.overrides.values():
			if o.target == item:
				return True
		return False


@dataclass
class NodeAsset:
	asset : CustoAssetProperties
	attributes : NodeAttributes = field(default_factory=NodeAttributes)
	overrides : NodeOverride = field(default_factory=NodeOverride)
	
	# Decorator
	def inject_attributes(func):
		def inject(self):
			res = func(self)
			if 'MESHES' in self.attributes.keys():
				res.add_label_combinaison(self.attributes['MESHES'])

			if 'MATERIALS' in self.attributes.keys():
				res.add_label_combinaison(self.attributes['MATERIALS'])
				
			return res

		return inject

	# Properties
	@property
	def name(self):
		return self.asset.name
	
	@property
	def is_empty(self):
		return self.asset.is_empty
	
	@property
	def asset_type(self):
		return self.asset.asset_type
	
	@property
	def asset_id(self):
		return self.asset.asset_id
	
	@property
	def layer(self):
		return self.asset.layer
	
	@property
	def slots(self):
		return self.asset.slots
	
	@property
	def valid_slots(self):
		return [s.name for s in self.asset.slots if s.value]
	
	@property
	def asset_name(self):
		return self.asset.asset_name
	
	@property
	@inject_attributes
	def valid_labels(self):
		return self.asset.valid_labels
	
	@property
	def all_mesh_variations(self):
		return self.asset.all_mesh_variations
	
	@property
	def materials(self)->dict:
		return self.asset.materials
	
	@property
	def material_combinaison(self):
		combinaison = LabelCombinaison()
		
		for lc, l in self.attributes.labels.items():
			if lc not in bpy.context.scene.custo_handler_settings.custo_asset_types_label_categories[self.asset_type.name].materials_label_category:
				continue

			combinaison.add_binary_labels(lc, l)

		return combinaison
	
	def mesh_variation(self, variations:LabelVariation, exclude=[]):
		return self.asset.mesh_variation(variations, exclude=exclude)
	
	def is_valid_mesh(self, ob, variations:LabelVariation):
		return self.asset.is_valid_mesh(ob, variations)

	def has_mesh_with_labels(self, variations:LabelVariation):
		return self.asset.has_mesh_with_labels(variations)

