def nameCon(objSpace, objName, objType):

	objTypeName = ""

	if objType == "controller" :
		objTypeName = "ctl"

	elif objType == "locator" :
		objTypeName = "loc"

	elif objType == "skin" :
		objTypeName = "sk"

	elif objType == "rig":
		objTypeName = "ik"

	elif objType == "joint" :
		objTypeName = "jnt"
	
	elif objType == "group" :
		objTypeName = "grp"

	elif objType == "curve" :
		objTypeName = "crv"

	elif objType == "mesh" :
		objTypeName = "msh"

	elif objType == "cluster" :
		objTypeName = "clst"

	elif objType == "handle" :
		objTypeName = "hdl"

	objSpaceName = ""

	if objSpace == "" :
		objSpaceName = ""
		return (objName + "_" + objTypeName)

	else :

		if objSpace == "left" :
			objSpaceName = "L"

		elif objSpace == "right" :
			objSpaceName = "R"

		elif objSpace == "center" :
			objSpaceName = "C"

		elif objSpace == "top" :
			objSpaceName = "Tip"

		elif objSpace == "bottom" :
			objSpaceName = "Root"

		elif objSpace == "middle" :
			objSpaceName = "Mid"

		return (objSpaceName + "_" + objName + "_" + objTypeName)
		
	