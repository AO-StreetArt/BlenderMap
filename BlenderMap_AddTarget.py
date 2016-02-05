# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 23:26:37 2015

Blender Add-On to allow adding a mapping target to the scene
To be used with Blender Map-Map integration

Adds a target list to the blender context which can be accessed to view the target
configured

@author: alex
"""

bl_info = {
    "name": "Blender_Map_Target", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 76, 1),
    "description": "Blender Map Addon to add a mapping target object to the scene",
    "category": "Object",
}

import bpy

class TargetList():
    trgt_list = [];
    
class MappingTarget():
    
    def __init__(self, obj):
        self.object = obj
    

class AddMappingTarget(bpy.types.Operator):
    bl_idname = "object.blender_map_target"
    bl_label = "Add Mapping Target"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        #Called by blender when the addon is run
        
        #Add a plane
        bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False,\
            location=(0.0, 0.0, 0.0), layers=(True, False, False, False, False, False,\
                False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        
        #Pull the Target List down from the context
        t_list = bpy.context.scene.target_list.trgt_list
        
        #Pull the created object down
        obj = bpy.data.objects['Plane']
        n = 'Target'
        
        for p in t_list:
            if p.object.name == n:
                n= '%s.0' % (n)
                
        obj.name = n
        
        #Create the Projector Object and push it to the projector list in the blender context
        tar = MappingTarget(obj)
        t_list.append(tar)
        
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
def menu_func(self, context):
    self.layout.operator(AddMappingTarget.bl_idname) 
        
def register():
    bpy.utils.register_class(AddMappingTarget)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.Scene.target_list = TargetList()
    
def unregister():
    del bpy.types.Scene.target_list
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(AddMappingTarget)
    
if __name__ == "__main__":
    register()