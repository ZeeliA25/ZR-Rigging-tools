#--------------------------------------------------------------#
#                     ZR Make Controller                       #
#                     Author : ZeeliA                          #
#              v.2026-02-06-001/Maya 2023.3.1                  #
#--------------------------------------------------------------#

import maya.cmds as cmds

from PySide2 import QtWidgets
from PySide2 import QtCore

from ZR_nameCon import *
from ZR_controller_shapes import *


#---------------------------------------------------------------
# Function : Creating a controller
#---------------------------------------------------------------

def ZR_make_controler(object, shape) :
    
    # Declare size variable
    sizeValue = 10
    
    # If "main" controller exists, fetch character size
    mainCtrl = ZR_nameCon("", "main", "controller")    
    if cmds.objExists(mainCtrl) == 1 :
        sizeValue = cmds.getAttr(f"{mainCtrl}.GEO_SIZE")
 
    # Create controller
    ctrlBase = chosen_shape(shape)
    
    # Create controller's offset group
    grpBase = cmds.group(ctrlBase)
    
    # MatchTransform group on the chosen object
    cmds.matchTransform(grpBase, object)
    
    # Find controller's shape
    ctrlShape = cmds.listRelatives(ctrlBase, shapes=1)

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
    
    # Rename
    #objectName = object.split("_")

    #if len(objectName) > 1 :
        #newName = objectName[1]

    #else :
        #newName = objectName[0]
    
    ctrl = cmds.rename(ctrlBase, ZR_nameCon(side, object, "controller"))
    grp = cmds.rename(grpBase, ZR_nameCon(side, object, "group"))
    
    # Return the name of the controller and offset group
    return(ctrl, grp)
    

#---------------------------------------------------------------
# Function : Creating a controler on selection
#---------------------------------------------------------------

def ZR_makeControlerSelection(shape) :

    # List selection
    sel = cmds.ls(sl=1)
    
    # Check : Is there a selection ?
    if len(sel) == 0 :
        cmds.error("!!! No object selected. Please select one object or more !!!")
        
    else :   
        # For each selected objects, create a controller
        for object in sel :
            ZR_make_controler(object,shape)
            
#---------------------------------------------------------------
# Window UI to create the controllers on selection
#---------------------------------------------------------------
            
class MakeControllerGui(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget=None):
        super().__init__(parent=None)
        self.init_ui()

        self.setWindowTitle(f"Make Controller {__version__}")
        
    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        shape_list_label = QtWidgets.QLabel("Controller shape")
        main_layout.addWidget(shape_list_label)
        cube_button = QtWidgets.QPushButton("Cube")
        main_layout.addWidget(cube_button)
        sphere_button = QtWidgets.QPushButton("Sphere")
        main_layout.addWidget(sphere_button)
        square_button = QtWidgets.QPushButton("Square")
        main_layout.addWidget(square_button)
        triangle_button = QtWidgets.QPushButton("Triangle")
        main_layout.addWidget(triangle_button)
        stick_button = QtWidgets.QPushButton("Stick")
        main_layout.addWidget(stick_button)
        plus_button = QtWidgets.QPushButton("Plus")
        main_layout.addWidget(plus_button)
        single_arrow_button = QtWidgets.QPushButton("Single Arrow")
        main_layout.addWidget(single_arrow_button)
        cross_arrow_button = QtWidgets.QPushButton("Cross")
        main_layout.addWidget(cross_arrow_button)
        target_circle_button = QtWidgets.QPushButton("Target")
        main_layout.addWidget(target_circle_button)
        circle_button = QtWidgets.QPushButton("Circle")
        main_layout.addWidget(circle_button)
        half_circle_button = QtWidgets.QPushButton("Half-circle")
        main_layout.addWidget(half_circle_button)

        self.setLayout(main_layout)
        
        # Signal/Slots
        
        cube_button.clicked.connect(self.on_cube_button_clicked)
        sphere_button.clicked.connect(self.on_sphere_button_clicked)
        square_button.clicked.connect(self.on_square_button_clicked)
        triangle_button.clicked.connect(self.on_triangle_button_clicked)
        stick_button.clicked.connect(self.on_stick_button_clicked)
        plus_button.clicked.connect(self.on_plus_button_clicked)
        single_arrow_button.clicked.connect(self.on_single_arrow_button_clicked)
        cross_arrow_button.clicked.connect(self.on_cross_arrow_button_clicked)
        target_circle_button.clicked.connect(self.on_target_circle_button_clicked)
        circle_button.clicked.connect(self.on_circle_button_clicked)
        half_circle_button.clicked.connect(self.on_half_circle_button_clicked)        
    
    def on_cube_button_clicked(self):
        shape = cube
        ZR_makeControlerSelection(shape)
        
    def on_sphere_button_clicked(self):
        shape = sphere_shape
        ZR_makeControlerSelection(shape)
        
    def on_square_button_clicked(self):
        shape = square
        ZR_makeControlerSelection(shape)

    def on_triangle_button_clicked(self):
        shape = triangle
        ZR_makeControlerSelection(shape)

    def on_stick_button_clicked(self):
        shape = stick
        ZR_makeControlerSelection(shape)
        
    def on_plus_button_clicked(self):
        shape = plus_shape
        ZR_makeControlerSelection(shape)
        
    def on_single_arrow_button_clicked(self):
        shape = single_arrow
        ZR_makeControlerSelection(shape)

    def on_cross_arrow_button_clicked(self):
        shape = cross_arrow
        ZR_makeControlerSelection(shape)

    def on_target_circle_button_clicked(self):
        shape = target_circle
        ZR_makeControlerSelection(shape)

    def on_circle_button_clicked(self):
        shape = circle_shape
        ZR_makeControlerSelection(shape)  

    def on_half_circle_button_clicked(self):
        shape = half_circle
        ZR_makeControlerSelection(shape)  


def create_controller_window() :
    __version__ = 3.0
    d = MakeControllerGui()
    d.show()
