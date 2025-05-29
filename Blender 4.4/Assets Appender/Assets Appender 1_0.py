bl_info = {
    "name": "Assets Appender",
    "author": "Nanomanpro",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "Asset Browser > Right-Click Menu",
    "description": "Appends selected assets from their source .blend files and removes asset tag",
    "category": "Import-Export",
}

import bpy

class ASSET_OT_append_selected(bpy.types.Operator):
    bl_idname = "asset.append_selected"
    bl_label = "Append Selected Asset(s)"
    bl_description = "Append selected assets (Object, Collection, Action) from their original .blend files"
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

        for asset in selected_assets:
            asset_name = asset.name
            asset_type = asset.id_type
            blend_path = bpy.path.abspath(asset.full_library_path)

            print(f"🔍 Asset: {asset_name} (type: {asset_type}) from file {blend_path}")

            if asset_type == 'OBJECT':
                subfolder = "Object"
            elif asset_type == 'COLLECTION':
                subfolder = "Collection"
            elif asset_type == 'ACTION':
                subfolder = "Action"
            elif asset_type == 'MATERIAL':
                subfolder = "Material"
            elif asset_type == 'NODETREE':
                subfolder = "NodeTree"
            else:
                self.report({'WARNING'}, f"Unsupported asset type: '{asset_type}'")
                continue

            try:
                with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                    if asset_type == 'OBJECT' and asset_name in data_from.objects:
                        data_to.objects = [asset_name]
                    elif asset_type == 'COLLECTION' and asset_name in data_from.collections:
                        data_to.collections = [asset_name]
                    elif asset_type == 'ACTION' and asset_name in data_from.actions:
                        data_to.actions = [asset_name]
                    elif asset_type == 'MATERIAL' and asset_name in data_from.materials:
                        data_to.materials = [asset_name]
                    elif asset_type == 'NODETREE' and asset_name in data_from.node_groups:
                        data_to.node_groups = [asset_name]
                    else:
                        self.report({'WARNING'}, f"'{asset_name}' not found in '{subfolder}'")
                        continue

                if asset_type == 'OBJECT':
                    for obj in data_to.objects:
                        if obj and obj.name not in bpy.context.scene.objects:
                            bpy.context.collection.objects.link(obj)
                        if obj.asset_data:
                            obj.asset_clear()
                        obj.select_set(True)
                        bpy.context.view_layer.objects.active = obj
                        print(f"✅ Imported object '{obj.name}' (asset tag removed)")

                elif asset_type == 'COLLECTION':
                    for col in data_to.collections:
                        if col and col.name not in bpy.context.scene.collection.children:
                            bpy.context.scene.collection.children.link(col)
                        if col.asset_data:
                            col.asset_clear()
                        print(f"✅ Imported collection '{col.name}' (asset tag removed)")
                        for obj in col.objects:
                            obj.select_set(True)
                        if col.objects:
                            bpy.context.view_layer.objects.active = col.objects[0]

                elif asset_type == 'ACTION':
                    print(f"✅ Imported Action '{asset_name}' – assign manually")

                elif asset_type == 'MATERIAL':
                    for mat in data_to.materials:
                        if mat.asset_data:
                            mat.asset_clear()
                        print(f"✅ Imported Material '{mat.name}' (asset tag removed)")

                elif asset_type == 'NODETREE':
                    for ng in data_to.node_groups:
                        if ng.asset_data:
                            ng.asset_clear()
                        print(f"✅ Imported Node Group '{ng.name}' (asset tag removed)")


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
