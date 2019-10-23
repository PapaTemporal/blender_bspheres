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

bl_info = {
    'name': 'bSpheres',
    'category': '3D View',
    'author': 'Abinadi Cordova',
    'description': 'This addon takes the blender traditional way of creating base meshes and fleshes it out to seem more like zSpheres',
    'blender': (2, 80, 0),
    'version': (0, 0, 1),
    'location': '3D View > Panels > bSpheres',
}

import bpy
from . bSpheres import *

def register():
    bpy.utils.register_class(AddBMesh)
    bpy.utils.register_class(applyBSphereModifiers)
    bpy.utils.register_class(BSpheresPanel)

def unregister():
    bpy.utils.unregister_class(AddBMesh)
    bpy.utils.unregister_class(applyBSphereModifiers)
    bpy.utils.unregister_class(BSpheresPanel)

if __name__ == '__main__':
    register()