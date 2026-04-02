#--------------------------------------------------------------#
#                      ZR Matrix Constraint                    #
#                       Author : ZeeliA                        #
#                       v.2026-04-02-001                       #
#--------------------------------------------------------------#

import maya.cmds as cmds

# -------------------------------------------------------------------------------------------
# Function : Matrix Constraint
# -------------------------------------------------------------------------------------------

def ZR_matrix_constraint(master, slave) :

    # Find slave's parent
    parentSlave = cmds.listRelatives( slave, p=True )
    
    cmds.addAttr(master, longName = "offset", dataType = "matrix")
    
    # Calculate the offset
    multMatrixTemp = cmds.createNode("multMatrix")

    if parentSlave :
        cmds.connectAttr(f"{parentSlave[0]}.worldMatrix[0]", f"{multMatrixTemp}.matrixIn[0]")
    cmds.connectAttr(f"{master}.worldInverseMatrix[0]", f"{multMatrixTemp}.matrixIn[1]")

    offsetMatrixData = cmds.getAttr(f"{multMatrixTemp}.matrixSum")
    cmds.delete(multMatrixTemp)

    # Multiply matrices
    
    multMatrixNode = cmds.createNode("multMatrix")

    cmds.setAttr(f"{multMatrixNode}.matrixIn[0]", offsetMatrixData, type="matrix")
    cmds.connectAttr(f"{master}.worldMatrix[0]", f"{multMatrixNode}.matrixIn[1]")
    
    if parentSlave :
        cmds.connectAttr(f"{parentSlave[0]}.worldInverseMatrix[0]", f"{multMatrixNode}.matrixIn[2]")
    cmds.connectAttr(f"{multMatrixNode}.matrixSum", f"{slave}.offsetParentMatrix")

# -------------------------------------------------------------------------------------------
# Function : Constraint the selection
# -------------------------------------------------------------------------------------------
    
def ZR_matrixConstraintSelection ():
    
    sel = cmds.ls(sl = True) 
    
    if len(sel) != 2 :
        cmds.error("Two objects needed !") 
        
    else :
        ZR_matrix_constraint(sel[0], sel[1])
        

# -------------------------------------------------------------------------------------------
# Function : Viewport window 
# -------------------------------------------------------------------------------------------

def createConstraintWindow():
    if cmds.window('ZR_Matrix_constraints', exists=True):
        cmds.deleteUI('ZR_Matrix_constraints')
    cmds.window('ZR_Matrix_constraints', w=250)
    
    cmds.columnLayout(rowSpacing=2, columnWidth=250, bgc=[0.3,0.3,0.3], adjustableColumn = True)
    cmds.button(l='Parent constraint with offset', w= 100, c= 'ZR_matrixConstraintSelection ()')
    
    
    cmds.showWindow('ZR_Matrix_constraints')
    

