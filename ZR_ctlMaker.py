# Import maya.cmds globally
import maya.cmds as cmds
from nameCon import *

def ZR_ctlMaker(object):
    # Déclarer une variable de taille
    sizeValue = 1

    # Si le controler "main" existe, demander la taille du personnage
    mainCtrl = nameCon("", "main", "controller")
    if cmds.objExists(mainCtrl) == 1:
        sizeValue = cmds.getAttr(mainCtrl + ".GEO_SIZE")

    # Creation du controler
    ctlBase = cmds.circle(radius=sizeValue, ch=0, nr=(1, 0, 0))

    # Creation du groupe de placement du controler
    grpBase = cmds.group(ctlBase[0])

    # MatchTransform du groupe du controler sur l'objet selectionné
    cmds.matchTransform(grpBase, object)

    # Trouver la Shape du controler
    ctlShape = cmds.listRelatives(ctlBase[0], shapes=1)

    # Creation d'un override d'affichage
    cmds.setAttr(ctlShape[0] + ".overrideEnabled", 1)

    # Trouver la position sur X du controler
    spacePosition = cmds.xform(grpBase, query=1, t=1, ws=1)
    side = ""

    # Si X est positif, overrideColor = 6 (Bleu)
    if spacePosition[0] > 0.01:
        cmds.setAttr(ctlShape[0] + ".overrideColor", 6)
        side = "left"

    # Sinon, si X est negatif, overrideColor = 13 (Rouge)
    elif spacePosition[0] < -0.01:
        cmds.setAttr(ctlShape[0] + ".overrideColor", 13)
        side = "right"

    # Sinon, si X = 0, overrideColor = 17 (Jaune)
    else:
        cmds.setAttr(ctlShape[0] + ".overrideColor", 17)

    # Ranger dans le groupe de la hierarchie s'il existe
    if cmds.objExists("CONTROLLERS") == 1:
        cmds.parent(grpBase, "CONTROLLERS")

    # Renommer
    ctl = cmds.rename(ctlBase[0], nameCon(side, object, "controller"))
    grp = cmds.rename(grpBase, nameCon(side, object, "group"))

    # Retourner le nom du controler et du groupe de placement
    return ctl, grp


def ZR_makeCtlSelection():
    # Lister la selection
    sel = cmds.ls(sl=True)
    if len(sel) == 0:
        cmds.error("Nothing is selected dude!")

    else:
        for object in sel:
            ZR_ctlMaker(object)