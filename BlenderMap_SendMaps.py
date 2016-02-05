# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 01:00:09 2016

Blender Addon to send a series of messages to Instances of MapMap via OSC

@author: alex
"""

bl_info = {
    "name": "Blender_Map_Send_Maps", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 76, 1),
    "description": "Blender Map Addon to send mapping data to MapMap via OSC",
    "category": "Object",
}

from pythonosc import osc_message_builder
from pythonosc import udp_client
import bpy
import mathutils
from math import sin, cos, tan

class vect():
    
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
    

class BlendMap():
    pass

class OSC_Client():
    
    #Initialize the OSC Client
    #param: server_ip - the IP Address of the Server being connected to
    #param: server_port - The Port the OSC Server is listening on
    def __init__(self, server_ip, server_port):
        self.client = udp_client.UDPClient(str(server_ip), int(float(server_port)))

    #Send a message to the OSC Server
    #param: address - The address for the message
    #param: argument_types - The argument types in the format ',xxx' ie ',is'
    #param: argument_list - a list of the arguments for the message
    def send_message(self, addr, argument_types, argument_list):
        msg = osc_message_builder.OscMessageBuilder(address = addr)
        i=1
        for argument in argument_list:
            type_string = str(argument_types)
            if type_string[i] == 'i':
                arg = int(float(argument))
            elif type_string[i] == 'f':
                arg = float(argument)
            elif type_string[i] == 's':
                arg = str(argument)
            else:
                arg = argument
            msg.add_arg(arg, type_string[i])
            i+=1
        msg = msg.build()
        self.client.send(msg)
        
class SendMappingData(bpy.types.Operator):
    bl_idname = "object.blender_send_maps"
    bl_label = "Send Mapping Data"
    bl_options = {'REGISTER', 'UNDO'}
    ip_address = bpy.props.StringProperty(name="IP Address", default="127.0.0.1")
    port = bpy.props.IntProperty(name="Port", default=5005)
    
    #Compute the perspective projection of a 3d point
    #Algorithm from Wikipedia: https://en.wikipedia.org/wiki/3D_projection
    #@param - a: 3D position of a point A that is to be projected
    #@param - c: 3D position of a point C representing the camera
    #@param - r: 3D Euler angle for orientation from the camera
    #@param - e: 3D position of the viewer relative to the display surface, which goes through the camera
    def perspective_projection(a, c, r, e):
        
        #Rotation Matrices
        rot_x = mathutils.Matrix.Rotation(math.radians(r[0]), 4, 'X')
        rot_y = mathutils.Matrix.Rotation(math.radians(r[1]), 4, 'Y')
        rot_z = mathutils.Matrix.Rotation(math.radians(r[2]), 4, 'Z')
        
        #Define Position of A in local coordinates wrt camera
        d = mathutils.Vector((0.0, 0.0, 0.0))
        d = rot_z * rot_y * rot_x * (a - c)
        
        #Return vector
        b = mathutils.Vector((((e[2] / d[2]) * d[0]) - e[0], ((e[2] / d[2]) * d[1]) - e[1]))
        return b
    
    #Take the 2D projection of the target through
    #each projector, associated to one element of the
    #UV Map to form the mapmap mappings
    
    #Take the maps generated and create OSC Message parameters in the form of a list
    def create_map_message(self, orig_map, dest_map):
        map_message = []
        
        #TODO: Create the message
        
        return map_message
    
    #Generate a map from a projector and a target element
    #return a list of OSC Message parameters
    def gen_map(self, target, projector):
        
        origin_map = []
        destination_map = []
        
        #TODO: Calculate the origin and destination map
        
        #Create the return list
        return self.create_map_message(origin_map, destination_map)
        
    def create_blend_map_message(self, blendmap):
        pass
    
    def map_blend_map_message(self, blendmap):
        pass
        
    #Generate a Blend Map based on the UV Map and the areas of overlap in 3 space
    #according to the Blend Function
    def generate_blend_map(self, target_list, origin_map, destination_map):
        pass
    
    def execute(self, context):
        
        #Called by blender when the addon is run
        
        #Start the OSC Client
        client = OSC_Client(self.ip_address, self.port)
        
        #Now we can use the client to send various messages to mapmap to control it's behavior
        #ie. add mappings, paints, start playback, etc
        
        #Pull the Target List down from the context
        t_list = bpy.context.scene.target_list.trgt_list
        
        #Pull the Projector List down from the context
        p_list = bpy.context.scene.projector_list.proj_list
        
        #Declare a list to store the projectors for each target
        projectors = []

        #------------------------
        #Send the map information
        #------------------------
        
        for t in t_list:
            
            #find the projectors associated with the target
            del projectors[:]
            for p in p_list:
                if p.target == t.object.name:
                    projectors.append(p)
                    
            #Generate the Maps to send to MapMap
            param_list = self.gen_map(t, projectors[0])
            
            #Create the message
            address = param_list[0]
            arg_types = param_list[1]
            param_list.pop(0)
            param_list.pop(0)
            
            #Send the message
            client.send_message(address, arg_types, param_list)
            
        #------------------------------
        #Send the blend map information
        #------------------------------
        
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
def menu_func(self, context):
    self.layout.operator(SendMappingData.bl_idname) 
        
def register():
    bpy.utils.register_class(SendMappingData)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(SendMappingData)
    
if __name__ == "__main__":
    register()