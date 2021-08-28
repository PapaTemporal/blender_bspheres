# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
 
bl_info = {
    'name': 'bSpheres',
    'category': 'All',
    'author': 'Abinadi Cordova',
    'version': (0, 0, 3),
    'blender': (2, 93, 3),
    'location': '3D_Viewport window -> N-Panel > bSpheres',
    'description': 'bSpheres'
}

def add_box(width, height, depth):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = [
        (+1.0, +1.0, -1.0),
        (+1.0, -1.0, -1.0),
        (-1.0, -1.0, -1.0),
        (-1.0, +1.0, -1.0),
        (+1.0, +1.0, +1.0),
        (+1.0, -1.0, +1.0),
        (-1.0, -1.0, +1.0),
        (-1.0, +1.0, +1.0),
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 0, 3, 7),
    ]

    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces
 
 
class applyBSphereModifiers(bpy.types.Operator):
    bl_idname = 'tcg.apply_bsphere_modifiers'
    bl_label = 'Apply bSphere Modifiers'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        if bpy.app.version < (2, 93, 0):
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
        else:
            bpy.ops.object.modifier_apply(modifier="Mirror")
            bpy.ops.object.modifier_apply(modifier="Skin")
            bpy.ops.object.modifier_apply(modifier="Subdivision")
        context.space_data.shading.show_xray = False
        obj = context.object
        bpy.ops.object.mode_set(mode=bpy.data.scenes['Scene']['previous_mode'])
        bpy.data.meshes[obj.name].remesh_voxel_size = 0.01
        bpy.ops.object.voxel_remesh()
        return {"FINISHED"}
    
from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)


class AddBMesh(bpy.types.Operator):
    """Add a bSphere"""
    bl_idname = "mesh.primitive_bsphere_add"
    bl_label = "Add bSphere"
    bl_options = {'REGISTER', 'UNDO'}

    width: FloatProperty(
        name="Width",
        description="Box Width",
        min=0.01, max=100.0,
        default=1.0,
    )
    height: FloatProperty(
        name="Height",
        description="Box Height",
        min=0.01, max=100.0,
        default=1.0,
    )
    depth: FloatProperty(
        name="Depth",
        description="Box Depth",
        min=0.01, max=100.0,
        default=1.0,
    )
    layers: BoolVectorProperty(
        name="Layers",
        description="Object Layers",
        size=20,
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    # generic transform props
    align_items = (
            ('WORLD', "World", "Align the new object to the world"),
            ('VIEW', "View", "Align the new object to the view"),
            ('CURSOR', "3D Cursor", "Use the 3D cursor orientation for the new object")
    )
    align: EnumProperty(
            name="Align",
            items=align_items,
            default='WORLD',
            update=AddObjectHelper.align_update_callback,
            )
    location: FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
    )
    rotation: FloatVectorProperty(
        name="Rotation",
        subtype='EULER',
    )

    def execute(self, context):

        bpy.data.scenes['Scene']['previous_mode'] = context.mode

        verts_loc, faces = add_box(
            self.width,
            self.height,
            self.depth,
        )

        mesh = bpy.data.meshes.new("bSphere")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)
        
        obj = context.scene.objects[mesh.name]
        for v in obj.data.vertices:
            v.select = True
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.object.modifier_add(type='SKIN')
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Skin"].use_x_symmetry = False
        bpy.context.object.modifiers["Skin"].use_y_symmetry = False
        bpy.context.object.modifiers["Skin"].use_z_symmetry = False
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        bpy.context.object.modifiers["Subdivision"].levels = 3
        bpy.context.object.modifiers["Subdivision"].quality = 3
        
        bpy.ops.object.mode_set(mode='EDIT')
        context.space_data.shading.show_xray = True
        
        bpy.ops.object.skin_root_mark()

        return {'FINISHED'}
 
 
class BSpheresPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_bSpheres_Panel'
    bl_label = 'bSpheres'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'bSpheres'
 
    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        split = layout.split()
        col = split.column()
        col.label(text="Create bSphere Mesh")
        sub = col.column(align=True)
        sub.operator("mesh.primitive_bsphere_add", text="Create")
        
        if obj:
            if obj.modifiers:
                for modifier in obj.modifiers:
                    if modifier.type == "MIRROR":
                        axis_text = "XYZ"
                        layout.label(text="Mirror Axis:")
                        row = layout.row()
                        for i, text in enumerate(axis_text):
                            row.prop(modifier, "use_axis", text=text, index=i)
                    if modifier.type == "SUBSURF":
                        layout.label(text="Subdivisions:")
                        split = layout.split()
                        col = split.column()
                        sub = col.column(align=True)
                        sub.prop(modifier, "levels", text="Viewport")
                    if modifier.type == "SKIN":
                        split = layout.split()
                        col = split.column()
                        col.label(text="Selected Vertices:")
                        sub = col.column(align=True)
                        sub.operator("object.skin_loose_mark_clear", text="Mark Loose").action = 'MARK'
                        sub.operator("object.skin_loose_mark_clear", text="Clear Loose").action = 'CLEAR'
                        sub = col.column()
                        sub.operator("object.skin_root_mark", text="Mark Root")
            
                split = layout.split()
                col = split.column()
                col.label(text="Convert to Sculptable Mesh")
                sub = col.column(align=True)
                sub.operator("tcg.apply_bsphere_modifiers", text="Apply")
                layout.label(text="Extrude Vert: E")
                layout.label(text="Scale Vert: Ctrl-A")
                layout.label(text="Add Vert Between Verts: Ctrl-R")
                context.space_data.shading.show_xray = True
            else:
                context.space_data.shading.show_xray = False