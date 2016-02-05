# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 01:00:09 2016

Blender Addon to generate png blend maps for a given mapping target & configured projectors

@author: alex
"""

bl_info = {
    "name": "Blender_Generate_Blend_Maps", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 76, 1),
    "description": "Blender Map Addon to generate blend maps",
    "category": "Object",
}

import bpy

class GenerateBlendMap(bpy.types.Operator):
    bl_idname = "object.blender_generate_blend_map"
    bl_label = "Generate Blend Maps"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        #Called by blender when the addon is run
        
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
def menu_func(self, context):
    self.layout.operator(GenerateBlendMap.bl_idname) 
        
def register():
    bpy.utils.register_class(GenerateBlendMap)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(GenerateBlendMap)
    
if __name__ == "__main__":
    register()