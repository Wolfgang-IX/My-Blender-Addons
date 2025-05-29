bl_info = {
    "name": "Custom Property Copy/Paste",
    "author": "Wolfgang.IX",
    "version": (1, 1),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Custom Props",
    "description": "Copy and paste custom properties between Objects, Materials, and Meshes",
    "category": "Object",
}

import bpy

# Store copied custom props
copied_props = {
    "object": {},
    "material": {},
    "mesh": {},
    "world": {},
    "light": {},
    "camera": {},
    "collection": {},
}


def copy_custom_props(source, target_type):
    global copied_props
    copied_props[target_type] = {k: v for k, v in source.items() if k not in {'_RNA_UI'}}

def paste_custom_props(target, target_type):
    def recursive_copy(src, dest):
        for k, v in src.items():
            try:
                if hasattr(v, "items"):
                    # Nested custom group
                    if k not in dest:
                        dest[k] = {}
                    recursive_copy(v, dest[k])
                else:
                    dest[k] = v
            except Exception as e:
                print(f"[!] Failed to copy key: {k} — {e}")

    props_to_paste = copied_props.get(target_type, {})
    for k, v in props_to_paste.items():
        try:
            if hasattr(v, "items"):
                if k not in target:
                    target[k] = {}
                recursive_copy(v, target[k])
            else:
                target[k] = v
        except Exception as e:
            print(f"[!] Failed to assign key: {k} — {e}")



# Operator classes
class COPY_OT_ObjectProps(bpy.types.Operator):
    bl_idname = "custom.copy_object_props"
    bl_label = "Copy Object Properties"

    def execute(self, context):
        obj = context.active_object
        if obj:
            copy_custom_props(obj, "object")
            self.report({'INFO'}, "Copied object properties")
        return {'FINISHED'}

class PASTE_OT_ObjectProps(bpy.types.Operator):
    bl_idname = "custom.paste_object_props"
    bl_label = "Paste Object Properties"

    def execute(self, context):
        for obj in context.selected_objects:
            paste_custom_props(obj, "object")
        self.report({'INFO'}, "Pasted object properties")
        return {'FINISHED'}

class COPY_OT_MaterialProps(bpy.types.Operator):
    bl_idname = "custom.copy_material_props"
    bl_label = "Copy Material Properties"

    def execute(self, context):
        mat = context.active_object.active_material if context.active_object else None
        if mat:
            copy_custom_props(mat, "material")
            self.report({'INFO'}, "Copied material properties")
        return {'FINISHED'}

class PASTE_OT_MaterialProps(bpy.types.Operator):
    bl_idname = "custom.paste_material_props"
    bl_label = "Paste Material Properties"

    def execute(self, context):
        for obj in context.selected_objects:
            mat = obj.active_material
            if mat:
                paste_custom_props(mat, "material")
        self.report({'INFO'}, "Pasted material properties")
        return {'FINISHED'}

class COPY_OT_MeshProps(bpy.types.Operator):
    bl_idname = "custom.copy_mesh_props"
    bl_label = "Copy Mesh Properties"

    def execute(self, context):
        mesh = context.active_object.data if context.active_object else None
        if mesh:
            copy_custom_props(mesh, "mesh")
            self.report({'INFO'}, "Copied mesh properties")
        return {'FINISHED'}

class PASTE_OT_MeshProps(bpy.types.Operator):
    bl_idname = "custom.paste_mesh_props"
    bl_label = "Paste Mesh Properties"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.data:
                paste_custom_props(obj.data, "mesh")
        self.report({'INFO'}, "Pasted mesh properties")
        return {'FINISHED'}
class COPY_OT_WorldProps(bpy.types.Operator):
    bl_idname = "custom.copy_world_props"
    bl_label = "Copy World Properties"

    def execute(self, context):
        world = context.scene.world
        if world:
            copy_custom_props(world, "world")
            self.report({'INFO'}, "Copied world properties")
        return {'FINISHED'}

class PASTE_OT_WorldProps(bpy.types.Operator):
    bl_idname = "custom.paste_world_props"
    bl_label = "Paste World Properties"

    def execute(self, context):
        world = context.scene.world
        if world:
            paste_custom_props(world, "world")
            self.report({'INFO'}, "Pasted world properties")
        return {'FINISHED'}

class COPY_OT_LightProps(bpy.types.Operator):
    bl_idname = "custom.copy_light_props"
    bl_label = "Copy Light Properties"

    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'LIGHT':
            copy_custom_props(obj.data, "light")
            self.report({'INFO'}, "Copied light properties")
        return {'FINISHED'}

class PASTE_OT_LightProps(bpy.types.Operator):
    bl_idname = "custom.paste_light_props"
    bl_label = "Paste Light Properties"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'LIGHT':
                paste_custom_props(obj.data, "light")
        self.report({'INFO'}, "Pasted light properties")
        return {'FINISHED'}

class COPY_OT_CameraProps(bpy.types.Operator):
    bl_idname = "custom.copy_camera_props"
    bl_label = "Copy Camera Properties"

    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'CAMERA':
            copy_custom_props(obj.data, "camera")
            self.report({'INFO'}, "Copied camera properties")
        return {'FINISHED'}

class PASTE_OT_CameraProps(bpy.types.Operator):
    bl_idname = "custom.paste_camera_props"
    bl_label = "Paste Camera Properties"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'CAMERA':
                paste_custom_props(obj.data, "camera")
        self.report({'INFO'}, "Pasted camera properties")
        return {'FINISHED'}

class COPY_OT_CollectionProps(bpy.types.Operator):
    bl_idname = "custom.copy_collection_props"
    bl_label = "Copy Collection Properties"

    def execute(self, context):
        coll = context.collection
        if coll:
            copy_custom_props(coll, "collection")
            self.report({'INFO'}, "Copied collection properties")
        return {'FINISHED'}

class PASTE_OT_CollectionProps(bpy.types.Operator):
    bl_idname = "custom.paste_collection_props"
    bl_label = "Paste Collection Properties"

    def execute(self, context):
        for coll in context.selected_ids:
            if isinstance(coll, bpy.types.Collection):
                paste_custom_props(coll, "collection")
        self.report({'INFO'}, "Pasted collection properties")
        return {'FINISHED'}





# UI Panel
class VIEW3D_PT_CustomPropsPanel(bpy.types.Panel):
    bl_label = "Custom Props"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Custom Props'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Object")
        row = layout.row()
        row.operator("custom.copy_object_props", text="Copy")
        row.operator("custom.paste_object_props", text="Paste")

        layout.label(text="Material")
        row = layout.row()
        row.operator("custom.copy_material_props", text="Copy")
        row.operator("custom.paste_material_props", text="Paste")

        layout.label(text="Mesh")
        row = layout.row()
        row.operator("custom.copy_mesh_props", text="Copy")
        row.operator("custom.paste_mesh_props", text="Paste")

        layout.label(text="World")
        row = layout.row()
        row.operator("custom.copy_world_props", text="Copy")
        row.operator("custom.paste_world_props", text="Paste")

        layout.label(text="Light")
        row = layout.row()
        row.operator("custom.copy_light_props", text="Copy")
        row.operator("custom.paste_light_props", text="Paste")

        layout.label(text="Camera")
        row = layout.row()
        row.operator("custom.copy_camera_props", text="Copy")
        row.operator("custom.paste_camera_props", text="Paste")

        layout.label(text="Collection")
        row = layout.row()
        row.operator("custom.copy_collection_props", text="Copy")
        row.operator("custom.paste_collection_props", text="Paste")



# Registration
classes = (
    COPY_OT_ObjectProps, PASTE_OT_ObjectProps,
    COPY_OT_MaterialProps, PASTE_OT_MaterialProps,
    COPY_OT_MeshProps, PASTE_OT_MeshProps,
    COPY_OT_WorldProps, PASTE_OT_WorldProps,
    COPY_OT_LightProps, PASTE_OT_LightProps,
    COPY_OT_CameraProps, PASTE_OT_CameraProps,
    COPY_OT_CollectionProps, PASTE_OT_CollectionProps,
    VIEW3D_PT_CustomPropsPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
