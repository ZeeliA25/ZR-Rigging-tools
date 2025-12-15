#--------------------------------------------------------------#
#                     ZR Make Controler                        #
#                     Author : ZeeliA                          #
#                     v.2025-12-15-001                         #
#--------------------------------------------------------------#

from ZR_nameCon import *
import maya.cmds as cmds

#---------------------------------------------------------------
# Function : Creating a controler
#---------------------------------------------------------------

def ZR_makeControler(object) :
    
    # Declare size variable
    sizeValue = 10
    
    # If "main" controller exists, fetch character size
    mainCtrl = ZR_nameCon("", "main", "controller")    
    if cmds.objExists(mainCtrl) == 1 :
        sizeValue = cmds.getAttr(f"{mainCtrl}.GEO_SIZE")
 
    # Create controller
    ctrlBase = cmds.circle(radius=sizeValue, normal=(1, 0, 0), constructionHistory=0)
    
    # Create controller's offset group
    grpBase = cmds.group(ctrlBase[0])
    
    # MatchTransform group on the chosen object
    cmds.matchTransform(grpBase, object)
    
    # Find controller's shape
    ctrlShape = cmds.listRelatives(ctrlBase[0], shapes=1)

    # Enable display override
    cmds.setAttr(f"{ctrlShape[0]}.overrideEnabled", 1)
    
    # Find X position of the controller
    spacePosition = cmds.xform(grpBase, query=1, translation=1, worldSpace=1)
    side = ""
        
    # If X is positive, overrideColor = 6 (Blue)
    if spacePosition[0] > 0.01 :
        cmds.setAttr(f"{ctrlShape[0]}.overrideColor", 6)
        side = "left"
    
    # If X is negative, overrideColor = 13 (Red)
    elif spacePosition[0] < -0.01 :
        cmds.setAttr(f"{ctrlShape[0]}.overrideColor", 13)
        side = "right"
        
    # Else, overrideColor = 17 (Yellow)
    else :
        cmds.setAttr(f"{ctrlShape[0]}.overrideColor", 17)
    
    # If "CONTROLLERS" group exists, store controller
    if cmds.objExists("CONTROLLERS") == 1 :
        cmds.parent(grpBase, "CONTROLLERS")
    
    # Renommer
    #objectName = object.split("_")

    #if len(objectName) > 1 :
        #newName = objectName[1]

    #else :
        #newName = objectName[0]
    
    ctrl = cmds.rename(ctrlBase[0], ZR_nameCon(side, object, "controller"))
    grp = cmds.rename(grpBase, ZR_nameCon(side, object, "group"))
    
    # Return the name of the controller and offset group
    return(ctrl, grp)
    

#---------------------------------------------------------------
# Function : Creating a controler on selection
#---------------------------------------------------------------

def ZR_makeControlerSelection() :

    # List selection
    sel = cmds.ls(sl=1)
    
    # Check : Is there a selection ?
    if len(sel) == 0 :
        cmds.error("!!! No object selected. Please select one object or more !!!")
        
    else :   
        # For each selected objects, create a controller
        for object in sel :
            ZR_makeControler(object)