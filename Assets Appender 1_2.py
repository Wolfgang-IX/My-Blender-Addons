bl_info = {
    "name": "Assets Appender",
    "author": "Nanomanpro, Wolfgang.IX",
    "version": (1, 2),
    "blender": (4, 4, 3),
    "location": "Asset Browser > Right-Click Menu",
    "description": "Appends selected assets from their source .blend files and removes asset tag",
    "category": "Import-Export",
}

import bpy

class ASSET_OT_append_selected(bpy.types.Operator):
    bl_idname = "asset.append_selected"
    bl_label = "Append Selected Asset(s)"
    bl_description = "Append selected assets (Object, Collection, Action, Material, Node Tree) from their original .blend files"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER' and context.space_data.browse_mode == 'ASSETS'

    def execute(self, context):
        selected_assets = context.selected_assets
        if not selected_assets:
            self.report({'WARNING'}, "No assets selected.")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        id_map = {
            'OBJECT': ('objects', bpy.context.collection.objects.link),
            'COLLECTION': ('collections', bpy.context.scene.collection.children.link),
            'MATERIAL': ('materials', None),
            'ACTION': ('actions', None),
            'NODETREE': ('node_groups', None),
            'WORLD': ('worlds', None),
            'MESH': ('meshes', None),
            'CURVE': ('curves', None),
            'TEXT': ('texts', None),
            'GPENCIL': ('grease_pencils', None),
            'IMAGE': ('images', None),
            'BRUSH': ('brushes', None),
            'FREESTYLELINESTYLE': ('linestyles', None),
            'TEXTURE': ('textures', None),
            'SPEAKER': ('speakers', bpy.context.collection.objects.link),
            'LIGHT_PROBE': ('light_probes', bpy.context.collection.objects.link),
            'VOLUME': ('volumes', bpy.context.collection.objects.link),
            'CAMERA': ('cameras', None),
            'LIGHT': ('lights', None),
        }

        for asset in selected_assets:
            asset_name = asset.name
            asset_type = asset.id_type
            blend_path = bpy.path.abspath(asset.full_library_path)

            print(f"🔍 Asset: {asset_name} (type: {asset_type}) from file {blend_path}")

            if asset_type not in id_map:
                self.report({'WARNING'}, f"Unsupported asset type: '{asset_type}'")
                continue

            data_attr, link_func = id_map[asset_type]

            try:
                with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                    source_list = getattr(data_from, data_attr, None)
                    if not source_list or asset_name not in source_list:
                        self.report({'WARNING'}, f"'{asset_name}' not found in '{data_attr}'")
                        continue
                    setattr(data_to, data_attr, [asset_name])

                loaded_data = getattr(data_to, data_attr)
                for item in loaded_data:
                    if item is None:
                        continue
                    if item.asset_data:
                        item.asset_clear()
                    if link_func and hasattr(item, "name") and not bpy.data.objects.get(item.name):
                        link_func(item)
                    print(f"✅ Imported {asset_type} '{item.name}' (asset tag removed)")

                    # Select and set active object if applicable
                    if asset_type == 'OBJECT':
                        item.select_set(True)
                        bpy.context.view_layer.objects.active = item
                    elif asset_type == 'COLLECTION':
                        for obj in item.objects:
                            obj.select_set(True)
                        if item.objects:
                            bpy.context.view_layer.objects.active = item.objects[0]

            except Exception as e:
                self.report({'ERROR'}, f"Error during import: {e}")


        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ASSET_OT_append_selected.bl_idname, icon='APPEND_BLEND')


classes = [ASSET_OT_append_selected]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.ASSETBROWSER_MT_context_menu.append(menu_func)

def unregister():
    bpy.types.ASSETBROWSER_MT_context_menu.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
