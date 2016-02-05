#Welcome to BlenderMap

BlenderMap is a set of tools allowing for calculation of projection maps & blend maps, and then communication of this data to external mapping softwares via OSC.  This is meant to integrate specifically with [MapMap](http://mapmap.info/tiki-index.php), but in theory could be used with many open-source projection mapping softwares with a few modifications.

The general idea is to drive multiple instances of MapMap through a single instance of Blender, using Blender along with other tools to physically map the environment.  These measurements can be transferred to Blender in many different ways, and eventually this toolset will include add-ons to collect this data.  Currently, however, that is out-of-scope.

Once measurements are collected and entered into Blender, maps can be calculated and sent to the external program.

#Install

You can install the Blender Addons in the User Preferences Panel with the 'Import from File' option

##Dependencies
BlenderMap requires python-osc to communicate the generated maps to external programs in real time.  Instructions on installing this in Blender will be forthcoming, but for now you can emulate the instructions for [BlenderSync](https://github.com/AO-StreetArt/BlenderSync) to install 0MQ.
