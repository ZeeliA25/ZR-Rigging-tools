import maya.cmds as cmds

sel = cmds.ls(sl=True)
counter = 1

result = cmds.promptDialog(
		title = "Rename asset",
		message = "Enter asset name",
		text = "bodyPart",
		button = ("OK","Cancel"),
		defaultButton = "OK",
		cancelButton = "Cancel",
		dismissString = "Cancel")

if result == "OK" :
    assetName = cmds.promptDialog(query = True, text = True)

else :
    cmds.error("Nothing entered")
    
for each in sel :
	new_name = assetName + str(counter) + '_ribbonFollicle'
	cmds.rename(each, new_name)
	cmds.select(cl=True)
	new_joint = cmds.joint(n=assetName + str(counter) + '_bind', p=[0,0,0], radius=0.1)
	new_loc = cmds.spaceLocator(n=assetName + str(counter) + '_loc')
	new_offset = cmds.group(n=assetName + str(counter) + '_offset', em=True)
	cmds.parent(new_joint,new_loc[0])
	cmds.parent(new_loc[0], new_offset)
	cmds.matchTransform(new_offset, new_name)
	cmds.parent(new_offset, new_name)
	for each_attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
		cmds.setAttr(new_loc[0] + '.'+ each_attr, 0)
	counter = counter + 1