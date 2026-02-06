#--------------------------------------------------------------#
#                     ZR Hierarchy                             #
#                     Author : ZeeliA                          #
#                     v.2026-02-06-001                         #
#--------------------------------------------------------------#

import maya.cmds as cmds

#---------------------------------------------------------------
# Function : Creating a hierarchy for a new rig
#---------------------------------------------------------------


def Hierarchy() :

	import maya.cmds as cmds

	sel = cmds.ls(sl=True)

	if len(sel) == 0 :
		cmds.error("No object selected dude")
	else :
		print(len(sel))

	result = cmds.promptDialog(
		title = "Rename asset",
		message = "Enter asset name",
		text = "CHARACTER",
		button = ("OK","Cancel"),
		defaultButton = "OK",
		cancelButton = "Cancel",
		dismissString = "Cancel")

	if result == "OK" :
		assetName = cmds.promptDialog(query = True, text = True)

	else :
		cmds.error("Nothing entered")
		

	chara_grp = cmds.group(em=True, name = assetName)
	geo_grp = cmds.group(em = True, name="GEO", parent = chara_grp)
	curves_grp = cmds.group(em = True, name = "CURVES", parent = chara_grp)
	skin_grp = cmds.group(em = True, name = "SKELETON")
	rig_grp = cmds.group(em = True, name = "RIGGING")
	ctl_grp = cmds.group(em = True, name = "CONTROLLERS")

	cmds.parent(sel, geo_grp)
	sizeValue = cmds.xform(geo_grp, query = 1, bb = 1)
	sizeY = sizeValue[4]-sizeValue[1]


	mainCtl = cmds.circle(name = "C_main_ctl", r = sizeY/3, nr=(0, 1, 0), ch = 0)
	cmds.addAttr(mainCtl[0], ln="GEO_SIZE", attributeType="float", defaultValue = sizeY )


	cmds.parent(mainCtl[0], chara_grp)
	cmds.parent(skin_grp, mainCtl[0])
	cmds.parent(rig_grp, mainCtl[0])
	cmds.parent(ctl_grp, mainCtl[0])

	cmds.addAttr(mainCtl[0], k = True, sn='skn', ln='SKELETON_VISIBILITY', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='rig', ln='RIGGING_VISIBILITY', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='ctlVis', ln='CONTROLLERS_VISIBILITY', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='mshlock', ln='MESH_LOCK', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='hop', ln='HIDE_ON_PLAYBACK', defaultValue=1, minValue=0, maxValue=1 )

	cmds.connectAttr(f"{mainCtl[0]}.skn", f"{skin_grp}.visibility")
	cmds.connectAttr(f"{mainCtl[0]}.rig", f"{rig_grp}.visibility")
	cmds.connectAttr(f"{mainCtl[0]}.ctlVis", f"{ctl_grp}.visibility")
	cmds.connectAttr(f"{mainCtl[0]}.mshlock", f"{geo_grp}.overrideEnabled")
	cmds.connectAttr(f"{mainCtl[0]}.hop", f"{ctl_grp}.hideOnPlayback")

	cmds.setAttr(f"{mainCtl[0]}.overrideEnabled", 1 )
	cmds.setAttr(f"{mainCtl[0]}.overrideColor", 17 )