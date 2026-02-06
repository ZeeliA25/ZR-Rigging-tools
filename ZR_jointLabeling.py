#--------------------------------------------------------------#
#                     ZR Joint Labeling                        #
#                     Author : ZeeliA                          #
#                     v.2026-02-06-001                         #
#--------------------------------------------------------------#

import maya.cmds as cmds

#---------------------------------------------------------------
# Function : Label joints according to name
#---------------------------------------------------------------

def ZR_jointLabeling(obj) :
    sel = cmds.ls(sl = True) 

    for each in sel :
        name = each.split("_")
        spacePosition = name[0]
        side = 0
        if spacePosition == "L":
            side = 1
        elif spacePosition == "R":
            side = 2
        else:
            side = 0 

        cmds.setAttr( each + ".side", side)
        cmds.setAttr(each + ".type", 18)
        cmds.setAttr(each + ".otherType", name[1], type = "string")
        