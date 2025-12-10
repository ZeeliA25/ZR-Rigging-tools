#--------------------------------------------------------------#
#                     ZR Render Setup                          #
#                     Author : ZeeliA                          #
#                     v.2025-08-14-001                         #
#--------------------------------------------------------------#

import maya.cmds as cmds
from PySide6 import QtWidgets
from PySide6 import QtCore

#---------------------------------------------------------------
# Function : Rendering tools for project "Grumeaux"
#---------------------------------------------------------------


def set_catmull_clark():
    """
    Set all selected objects rman_subdiv to True
    """
    sel = cmds.ls(selection=True)
    for obj in sel :
        cmds.setAttr(f"{obj}.rman_subdivScheme", True)

def set_camera_visibility():
    sel = cmds.ls(sl = True)

    for obj in sel :
        visibilityValue = cmds.getAttr(f"{obj}.rman_visibilityCamera")

        if visibilityValue == 0 :
            cmds.setAttr(obj + ".rman_visibilityCamera", 1)
        
        elif visibilityValue == 1 :                
            cmds.setAttr(f"{obj}.rman_visibilityCamera", 0)

def set_indirect_visibility():
    sel = cmds.ls(sl = True)

    for obj in sel :
        indirectValue = cmds.getAttr(f"{obj}.rman_visibilityIndirect")

        if indirectValue == 0 :
            cmds.setAttr(f"{obj}.rman_visibilityIndirect", 1)
        
        elif indirectValue == 1 :                
            cmds.setAttr(f"{obj}.rman_visibilityIndirect", 0)

def set_transmission_visibility():
    sel = cmds.ls(sl = True)

    for obj in sel :
        transmissionValue = cmds.getAttr(f"{obj}.rman_visibilityTransmission")

        if transmissionValue == 0 :
            cmds.setAttr(f"{obj}.rman_visibilityTransmission", 1)
        
        elif transmissionValue == 1 :                
            cmds.setAttr(f"{obj}.rman_visibilityTransmission", 0)

def neutralize_lights():
    sel = cmds.ls(sl = True)

    for obj in sel :
        cmds.setAttr((f"{obj}.lightColor"), 1.0,1.0,1.0, type = 'double3')
        cmds.setAttr(f"{obj}.enableTemperature", 0)

def hide_selection():
    sel = cmds.ls(sl = True)

    for obj in sel :
        visibilityValue = cmds.getAttr(f"{obj}.visibility")

        if visibilityValue == 0 :
            cmds.setAttr(f"{obj}.visibility", 1)
        
        elif visibilityValue == 1 :                
            cmds.setAttr(f"{obj}.visibility", 0)

def check_boxes():
    cameraCheck = cmds.checkBox(l='Camera')
    indirectCheck = cmds.checkBox(l='Indirect')
    transmissionCheck = cmds.checkBox(l='Transmission')
    viewportCheck = cmds.checkBox(l='Viewport')
    cameraValue = cmds.checkBox(cameraCheck, query=True, value=True)
    indirectValue = cmds.checkBox(indirectCheck, query=True, value=True)
    transmissionValue = cmds.checkBox(transmissionCheck, query=True, value=True)
    viewportValue = cmds.checkBox(viewportCheck, query=True, value=True)
    
def set_visibility():
    if cameraValue:
        set_camera_visibility()
    if indirectValue:
        set_indirect_visibility()
    if transmissionValue:
        set_transmission_visibility()
    if viewportValue:
        hide_selection()
        
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
    cmds.button(l='Catmull Clark', w= 100, c= 'set_catmull_clark()',  bgc=[0.4,0.4,0.4])
   
    separator02 = cmds.separator(height=10)
    cmds.text(label='Selection visibility :', align='left' )
    visibilityLayout = cmds.columnLayout(adjustableColumn=1)
    #check_boxes()
    #cmds.button(l='Set visibility', w= 100, c= 'set_visibility()')
    cmds.button(l='Camera visibility', w= 100, c= 'set_camera_visibility()',  bgc=[0.4,0.4,0.4])
    cmds.button(l='Indirect visibility', w= 100, c= 'set_indirect_visibility()',  bgc=[0.4,0.4,0.4])
    cmds.button(l='Transmission visibility', w= 100, c= 'set_transmission_visibility()',  bgc=[0.4,0.4,0.4])
    cmds.button(l='Viewport visibility', w= 100, c= 'hide_selection()',  bgc=[0.4,0.4,0.4])
    
    separator03 = cmds.separator(height=10)
    
    lightslayout = cmds.rowLayout(adjustableColumn=1, numberOfColumns=2, h=30, bgc=[0.5,0.5,0.5])
    cmds.text( label='Neutralize lights :', align='left' )
    cmds.button(l="Apply", w=150, c="neutralize_lights()", align='right', bgc=[0.4,0.4,0.4])
    
    cmds.showWindow('Render_setup')

    


class RenderSetupGui(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget=None):
        super().__init__(parent=None)
        self.init_ui()

        self.setWindowTitle(f"Render Setup {__version__}")

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        checklist_label = QtWidgets.QLabel("Checklist: ")
        main_layout.addWidget(checklist_label)

        box_labels = [
            "Set project fait", "Scene renommee et enregistree", 
            "Bonne hierarchie", "nameespaces supprimees",
            "Lumieres neutralisees", "Light groups ajoutes", 
            "Render layers faites", "Animation en Catmull-Clark",
            "Textures assignees", "Verifier le file path des exr"
        ]
        self.boxes = {}
        checkbox_layout = QtWidgets.QVBoxLayout()
        for box_label in box_labels:
            cb = QtWidgets.QCheckBox(box_label)
            self.boxes[box_label] = cb
            checkbox_layout.addWidget(cb)
        main_layout.addLayout(checkbox_layout)


        catmull_button = QtWidgets.QPushButton("Catmull Clark")
        main_layout.addWidget(catmull_button)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        bottom_part = QtWidgets.QVBoxLayout()
        selection_visib_label = QtWidgets.QLabel("Selection visibility")
        camera_visib_button = QtWidgets.QPushButton("Camera visibility")
        indirect_visib_button = QtWidgets.QPushButton("Indirect visibility")
        transmission_visib_button = QtWidgets.QPushButton("Transmission visibility")
        viewport_visib_button = QtWidgets.QPushButton("Viewport visibility")
        bottom_part.addWidget(selection_visib_label)
        bottom_part.addWidget(camera_visib_button)
        bottom_part.addWidget(indirect_visib_button)
        bottom_part.addWidget(transmission_visib_button)
        bottom_part.addWidget(viewport_visib_button)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        main_layout.addLayout(bottom_part)

        main_layout.addWidget(separator)
        self.setLayout(main_layout)


        # Signals/Slots
        catmull_button.clicked.connect(self.on_catmull_clark_clicked)

    def on_catmull_clark_clicked(self):
        for label, widget in self.boxes.items():
            status = widget.isChecked()
            print(f"{label} --> {status}")

