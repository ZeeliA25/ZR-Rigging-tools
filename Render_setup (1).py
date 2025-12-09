import maya.cmds as cmds

def setCatmullClark():
    sel = cmds.ls(sl = True)

    for obj in sel :
        cmds.setAttr(obj + ".rman_subdivScheme", 1)

def setCameraVisibility():
    sel = cmds.ls(sl = True)

    for obj in sel :
        visibilityValue = cmds.getAttr(obj + ".rman_visibilityCamera")

        if visibilityValue == 0 :
            cmds.setAttr(obj + ".rman_visibilityCamera", 1)
        
        elif visibilityValue == 1 :                
            cmds.setAttr(obj + ".rman_visibilityCamera", 0)


def setIndirectVisibility():
    sel = cmds.ls(sl = True)

    for obj in sel :
        indirectValue = cmds.getAttr(obj + ".rman_visibilityIndirect")

        if indirectValue == 0 :
            cmds.setAttr(obj + ".rman_visibilityIndirect", 1)
        
        elif indirectValue == 1 :                
            cmds.setAttr(obj + ".rman_visibilityIndirect", 0)


def setTransmissionVisibility():
    sel = cmds.ls(sl = True)

    for obj in sel :
        transmissionValue = cmds.getAttr(obj + ".rman_visibilityTransmission")

        if transmissionValue == 0 :
            cmds.setAttr(obj + ".rman_visibilityTransmission", 1)
        
        elif transmissionValue == 1 :                
            cmds.setAttr(obj + ".rman_visibilityTransmission", 0)

def neutralizeLights():
    sel = cmds.ls(sl = True)

    for obj in sel :
        cmds.setAttr((obj + ".lightColor"), 1.0,1.0,1.0, type = 'double3')
        cmds.setAttr(obj + ".enableTemperature", 0)

def hideSelection():
    sel = cmds.ls(sl = True)

    for obj in sel :
        visibilityValue = cmds.getAttr(obj + ".visibility")

        if visibilityValue == 0 :
            cmds.setAttr(obj + ".visibility", 1)
        
        elif visibilityValue == 1 :                
            cmds.setAttr(obj + ".visibility", 0)

def checkBoxes():
    cameraCheck = cmds.checkBox(l='Camera')
    indirectCheck = cmds.checkBox(l='Indirect')
    transmissionCheck = cmds.checkBox(l='Transmission')
    viewportCheck = cmds.checkBox(l='Viewport')
    cameraValue = cmds.checkBox(cameraCheck, query=True, value=True)
    indirectValue = cmds.checkBox(indirectCheck, query=True, value=True)
    transmissionValue = cmds.checkBox(transmissionCheck, query=True, value=True)
    viewportValue = cmds.checkBox(viewportCheck, query=True, value=True)
    
def setVisibility():
    if cameraValue == True :
        setCameraVisibility()
    if indirectValue == True :
        setIndirectVisibility()
    if transmissionValue == True :
        setTransmissionVisibility()
    if viewportValue == True :
        hideSelection()
        
def checkList():

    projectCheck = cmds.checkBox(l='Set project fait')
    sceneCheck = cmds.checkBox(l='Scene renommee et enregistree')
    hierarchyCheck = cmds.checkBox(l='Bonne hierarchie')
    namespaceCheck = cmds.checkBox(l='Namespace supprimes')
    lightsCheck = cmds.checkBox(l='Lumieres neutralisees')
    lightgroupsCheck = cmds.checkBox(l='Light groups ajoutes')
    layersCheck = cmds.checkBox(l='Render layers faites')
    catmullCheck = cmds.checkBox(l='Animation en Catmull-Clark')
    textureCheck = cmds.checkBox(l='Textures assignees')
    filepathCheck = cmds.checkBox(l='Verifier le file path des exr')

    
def createWindow():
    if cmds.window('Render_setup', exists=True):
        cmds.deleteUI('Render_setup')
    cmds.window('Render setup', w=150)
  
    
    checklistLayout = cmds.columnLayout(adjustableColumn=1,h=30)
    cmds.text(label='Checklist :', align='left',  bgc=[0.4,0.4,0.4], h=30 )
    checkList()
    
    separator01 = cmds.separator(height=10)
    cmds.columnLayout(rowSpacing=2, columnWidth=250, bgc=[0.3,0.3,0.3], adjustableColumn = True)
    cmds.button(l='Catmull Clark', w= 100, c= 'setCatmullClark()',  bgc=[0.4,0.4,0.4])
   
    separator02 = cmds.separator(height=10)
    cmds.text(label='Selection visibility :', align='left' )
    visibilityLayout = cmds.columnLayout(adjustableColumn=1)
    #checkBoxes()
    #cmds.button(l='Set visibility', w= 100, c= 'setVisibility()')
    cmds.button(l='Camera visibility', w= 100, c= 'setCameraVisibility()',  bgc=[0.4,0.4,0.4])
    cmds.button(l='Indirect visibility', w= 100, c= 'setIndirectVisibility()',  bgc=[0.4,0.4,0.4])
    cmds.button(l='Transmission visibility', w= 100, c= 'setTransmissionVisibility()',  bgc=[0.4,0.4,0.4])
    cmds.button(l='Viewport visibility', w= 100, c= 'hideSelection()',  bgc=[0.4,0.4,0.4])
    
    separator03 = cmds.separator(height=10)
    
    lightslayout = cmds.rowLayout(adjustableColumn=1, numberOfColumns=2, h=30, bgc=[0.5,0.5,0.5])
    cmds.text( label='Neutralize lights :', align='left' )
    cmds.button(l="Apply", w=150, c="neutralizeLights()", align='right', bgc=[0.4,0.4,0.4])
    
    cmds.showWindow('Render_setup')
    
createWindow()
