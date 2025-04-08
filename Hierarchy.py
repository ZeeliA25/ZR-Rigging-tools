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
		

	charaGrp = cmds.group(em=True, name = assetName)
	geoGrp = cmds.group(em = True, name="GEO", parent = charaGrp)
	curvesGrp = cmds.group(em = True, name = "CURVES", parent = charaGrp)
	skinGrp = cmds.group(em = True, name = "SKELETON")
	rigGrp = cmds.group(em = True, name = "RIGGING")
	ctlGrp = cmds.group(em = True, name = "CONTROLLERS")

	cmds.parent(sel, geoGrp)
	sizeValue = cmds.xform(geoGrp, query = 1, bb = 1)
	sizeY = sizeValue[4]-sizeValue[1]


	mainCtl = cmds.circle(name = "C_main_ctl", r = sizeY/3, nr=(0, 1, 0), ch = 0)
	cmds.addAttr(mainCtl[0], ln="GEO_SIZE", attributeType="float", defaultValue = sizeY )


	cmds.parent(mainCtl[0], charaGrp)
	cmds.parent(skinGrp, mainCtl[0])
	cmds.parent(rigGrp, mainCtl[0])
	cmds.parent(ctlGrp, mainCtl[0])

	cmds.addAttr(mainCtl[0], k = True, sn='skn', ln='SKELETON_VISIBILITY', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='rig', ln='RIGGING_VISIBILITY', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='ctlVis', ln='CONTROLLERS_VISIBILITY', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='mshlock', ln='MESH_LOCK', defaultValue=1, minValue=0, maxValue=1 )
	cmds.addAttr(mainCtl[0], k = True, sn='hop', ln='HIDE_ON_PLAYBACK', defaultValue=1, minValue=0, maxValue=1 )

	cmds.connectAttr(mainCtl[0] + ".skn", skinGrp +".visibility")
	cmds.connectAttr(mainCtl[0] + ".rig", rigGrp +".visibility")
	cmds.connectAttr(mainCtl[0] + ".ctlVis", ctlGrp +".visibility")
	cmds.connectAttr(mainCtl[0] + ".mshlock", geoGrp +".overrideEnabled")
	cmds.connectAttr(mainCtl[0] + ".hop", ctlGrp +".hideOnPlayback")

	cmds.setAttr(mainCtl[0] + ".overrideEnabled", 1 )
	cmds.setAttr(mainCtl[0] + ".overrideColor", 17 )