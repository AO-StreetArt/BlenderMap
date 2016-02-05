# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 01:00:09 2016

Blender Addon to unwrap a mapping target for the configured projectors

@author: alex
"""

bl_info = {
    "name": "Blender_Map_Unwrap_Target", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 76, 1),
    "description": "Blender Map Addon to unwrap the target object for the given projectors",
    "category": "Object",
}

import bpy, bmesh
import bpy_extras
import mathutils
import math

class UnwrapMapTarget(bpy.types.Operator):
    bl_idname = "object.blender_unwrap_map_target"
    bl_label = "Unwrap Map Target"
    bl_options = {'REGISTER', 'UNDO'}
    
    #Unwrap the mapping target mesh element
    #Each separate element in the coverage map should
    #be unwrapped whole, scaled such that the entire
    #UV Map for the target falls within a 2048x2048 pixel square,
    #and such that areas of overlap are maintained
    def find_edges(self, mapping_target, projector):
        #TODO: Store a reference vertex in 3space, use it to align projectors with segments of the UV Map
        print("Unwrap %s for projector %s" % (mapping_target, projector))
        mesh=bmesh.from_edit_mesh(bpy.context.object.data)
        self.update_aspect_ratio(projector)
        vert_list = self.find_intersecting_verts(projector, mapping_target, mesh, True)
        
        #Select all vertices on the edge
        bpy.ops.mesh.region_to_loop()
        #Mark the edges for the projector
        bpy.ops.mesh.mark_seam(clear=False)
    
    #Generate a UV Map for the target
    #The target should be selected & in edit mode
    def generate_coverage_map(self, mapping_target, projector_list):
        #Generate the map
        for projector in projector_list:
        
            #Find the edges on the mesh for the projector
            self.find_edges(mapping_target, projector)
            
            #TODO: build a mapping from the UV to each projector
            
        #TODO: unwrap the target
            
    #Update the aspect ratio of the image for the next projector
    #This must be called before the find_intersecting_verts method to allow for
    #Correct calculation from cameras
    #@param - projector: The projector from the projector list
    def update_aspect_ratio(self, projector):       
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.resolution_x = (projector.field_of_view[0] / projector.field_of_view[1]) * bpy.context.scene.render.resolution_y
        
    #Compute the vertices of a mesh which are covered
    #by a projector's field of view.  This does not perform clipping calculations
    #return a list of vertices that were intersected
    #@param - projector: the camera object being mapped
    #@param - target: The target from the target list being mapped
    #@param - select_results: True to select the resulting vertices, in this case target should be in edit mode prior to running
    def find_intersecting_verts(self, projector, target, target_mesh, select_results):
        
        return_list = []
        mesh=target_mesh
        
        print("Find Intersecting Vertices:")
        
        if select_results == True:
            v_list = mesh.verts
        else:
            v_list = target.data.vertices
        
        #For each vertex in the target, we need to figure out if v falls within the view of the projector
        for v in v_list:
            
            print("Testing vertex <%s, %s, %s>" % (v.co[0], v.co[1], v.co[2]))
            
            #Scene
            scene = bpy.context.scene
            
            #Active Object: Camera (Projector)
            obj = projector.object
            
            #Point being compared
            co = v.co
            
            v_proj_n = bpy_extras.object_utils.world_to_camera_view(scene, obj, co)
            v_p = mathutils.Vector((v_proj_n[0], v_proj_n[1]))
            
            a = mathutils.Vector((0.0, 0.0))
            b = mathutils.Vector((1.0, 0.0))
            c = mathutils.Vector((1.0, 1.0))
            
            #Run the comparison on the rectangle vs the point
            #Algorithm from http://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not

            if 0 <= (b-a).dot(v_p - a) <= (b-a).dot(b-a) and\
                0 <= (c-b).dot(v_p - b) <= (c-b).dot(c-b) and v_proj_n[2] >= 0.0:
                
                return_list.append(v.co)
                print(v.co)
                
                #Select the vertex
                if select_results == True:
                    v.select = True
                    
        if select_results == True:
            # trigger viewport update
            bpy.context.scene.objects.active = bpy.context.scene.objects.active
            
        return return_list
    
    def execute(self, context):
        
        #Called by blender when the addon is run
        
        #Pull the Target List down from the context
        t_list = bpy.context.scene.target_list.trgt_list
        t = bpy.context.scene.objects.active
        
        #Pull the Projector List down from the context
        p_list = bpy.context.scene.projector_list.proj_list
        
        #Declare a list to store the projectors for each target
        projectors = []
            
        #find the projectors associated with the target
        del projectors[:]
        for p in p_list:
            if p.target == t.name:
                projectors.append(p)
                
        #Generate the coverage map for the target
        self.generate_coverage_map(t, projectors)
              
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
def menu_func(self, context):
    self.layout.operator(UnwrapMapTarget.bl_idname) 
        
def register():
    bpy.utils.register_class(UnwrapMapTarget)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(UnwrapMapTarget)
    
if __name__ == "__main__":
    register()