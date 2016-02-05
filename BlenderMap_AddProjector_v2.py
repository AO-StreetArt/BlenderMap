# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 23:26:37 2015

Blender Add-On to allow adding a projector to the scene
To be used with Blender Map-Map integration

Adds a projector list object to the blender context which can be accessed to view
a list of projectors configured

@author: alex
"""

bl_info = {
    "name": "Blender_Map_Projector", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 76, 1),
    "description": "Blender Map Addon to add a projector object to the scene",
    "category": "Object",
}

import bpy

class ProjectorList():
    proj_list = [];
    
class Projector():
    
    def __init__(self, fov, obj, tar):
        self.field_of_view = fov
        self.object = obj
        self.target = tar

class AddMappingProjector(bpy.types.Operator):
    bl_idname = "object.blender_map_projector"
    bl_label = "Add Map Projector"
    bl_options = {'REGISTER', 'UNDO'}
    fieldofview_x = bpy.props.FloatProperty(name="Field of View - X", default=90.0)
    fieldofview_y = bpy.props.FloatProperty(name="Field of View - Y", default=90.0)
    target = bpy.props.StringProperty(name="Target", default="Target")
    
    def execute(self, context):
        
        #Called by blender when the addon is run
        
        #Add an arrow empty
        bpy.ops.object.camera_add(view_align=True, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0),\
            layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        
        #Pull the Projector List down from the context
        p_list = bpy.context.scene.projector_list.proj_list
        
        #Pull the created object down
        obj = bpy.data.objects['Camera']
        n = 'Projector'
        
        for p in p_list:
            if p.object.name == n:
                n= '%s.0' % (n)
                
        obj.name = n
        
        #Create the Projector Object and push it to the projector list in the blender context
        fov = [self.fieldofview_x, self.fieldofview_y]
        proj = Projector(fov, obj, self.target)
        p_list.append(proj)
        
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
def menu_func(self, context):
    self.layout.operator(AddMappingProjector.bl_idname) 
        
def register():
    bpy.utils.register_class(AddMappingProjector)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.Scene.projector_list = ProjectorList()
    
def unregister():
    del bpy.types.Scene.projector_list
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(AddMappingProjector)
    
if __name__ == "__main__":
    register()