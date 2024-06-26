import bpy

class CustoProperty:
	def is_compatible_label_combinaison(self, label_combinaison1, label_combinaison2):
		scene_label_category = bpy.context.scene.custo_handler_settings.custo_label_categories
		compatible = {}
		
		if label_combinaison1 is None or label_combinaison2 is None:
			return True

		for lc, l in label_combinaison1.items():
			compatible[lc] = False
			if lc not in label_combinaison2.keys():
				compatible[lc] = False
				break
			else:
				combinaison1_labels = [ll.name for ll in label_combinaison1[lc].values()]
				combinaison2_labels = [ll.name for ll in label_combinaison2[lc].values()]

				# Skipping if valid_any
				if scene_label_category[lc].valid_any is not None:
					if scene_label_category[lc].valid_any.name in combinaison1_labels or scene_label_category[lc].valid_any.name in combinaison2_labels:
						compatible[lc] = True
						continue

				if l == label_combinaison2[lc].values():
					compatible[lc] = True
					continue

				for label in l:

					for label2 in label_combinaison2[lc].values():
						if label.name == label2.name:
							compatible[lc] = True
							continue

		result = True
		for c in compatible.values():
			result = result and c

		return result