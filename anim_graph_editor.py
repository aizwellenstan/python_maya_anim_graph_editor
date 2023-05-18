
import math
import maya.cmds as cmds
import maya.mel as mel
import glob
import os,sys
from functools import partial, reduce

iconFolder = ".\icons"
def execute(*args):
	toValue = cmds.radioButtonGrp('applytoVorT',q=1,sl=1)
	amount  = cmds.floatField( 'amount_Strength', q=1, v=1)
	
	if toValue == 1:
		keyframe = lambda x, crv, **kwargs: cmds.keyframe( crv, vc=x, **kwargs )
	elif toValue == 2:
		keyframe = lambda x, crv, **kwargs: cmds.keyframe( crv, tc=x, **kwargs )
	else:
	    pass
	iteration = int(math.floor( amount ) )
	weight = amount - float( iteration )
	asList=[]
	
	sel = cmds.selectionConnection( 'keyframeList', q=1, obj=1 )
	if str(sel) == 'None':
	    cmds.confirmDialog(title = "Error",message = "please SELECT some keys",button='ok')
	else:
	    pass
	    
	for all in cmds.selectionConnection( 'keyframeList', q=1, obj=1 ):
	    asList.append(all)
	    
	for crv in asList:
		lastKey = cmds.keyframe( crv, q=1, kc=1 ) - 1
		selKeys = [ cmds.keyframe( crv, q=1, iv=1, t=( x, ) )[0]  for x in cmds.keyframe( crv, q=1, sl=1 ) ]
		vals    = []
		for all in keyframe( 1, crv, q=1, index=( 0, lastKey ) ):
		    vals.append(all)
		vals0   = vals[:]
		
		for n in range( iteration + 1 ):
			for key in selKeys:
				if key == 0:
					vs = vals[0:1]
				elif key == lastKey:
					vs = vals[key-1:key+1]
				else:
					vs = vals[key-1:key+2]
				vals[key] = reduce( lambda x, y: x+y, vs ) / len( vs )
			if n == iteration - 1:
				vals0 = vals[:]
		for key in selKeys:
			v = vals0[key] * ( 1.0-weight ) + vals[key] * weight
			keyframe( v, crv, a=1, index=( key, key ) )

def smoothapply_callback(input):
    strength = float(input)
    pass

def getAttrFilter_attr():
    result= []
    queryList =['translateFilterBtn','rotateFilterBtn','scaleFilterBtn']
    
    for all in queryList:
        if cmds.iconTextCheckBox(all,q=1,exists=1):
            if cmds.iconTextCheckBox(all,q=1,value=1):
                result.append(all.replace('FilterBtn',''))
            else:
                pass
        else:
            pass
    return result
        
def getAttrFilter_axis():
    result= []
    queryList =['XFilterExcuteBtn','YFilterExcuteBtn','ZFilterExcuteBtn']
    for all in queryList:
        if cmds.iconTextCheckBox(all,q=1,exists=1):
            if cmds.iconTextCheckBox(all,q=1,value=1):
                result.append(all.replace('FilterExcuteBtn',''))
            else:
                pass
        else:
            pass
    return result
  
def attrFilterBtnChanged(axisInput,which,*args):
    getAttrFilter_attr()
    axisList = ['X','Y','Z']
    axisList_on = getAttrFilter_axis()
    axisList_off = list(set(axisList)-set(axisList_on))

    if len(getAttrFilter_attr()) == 0:
        trsList = ['translate', 'rotate', 'scale']
        
    else:
        trsList = getAttrFilter_attr()
        trsList_off = list(set(['translate', 'rotate', 'scale'])-set(trsList))
        
    if which == 0:
        for all in trsList:
            trsaxis = all+axisInput
            mel.eval('filterUISelectAttributesCheckbox %s 0 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
        if len(getAttrFilter_attr()) == 0:
            print("pass")
            pass
        else :
            for on in trsList:
                axisList_left = getAttrFilter_axis()
                if len(axisList_left) == 0:
                    for ax in axisList:
                        trsaxis_on = on + ax
                        mel.eval('filterUISelectAttributesCheckbox %s 1 GE_ui_scriptedPanelOutlineEd;' %trsaxis_on)
                else:
                    pass
        
    if which == 1:
        if len(trsList) == 3:
            for all in trsList:
                trsaxis = all + axisInput
                mel.eval('filterUISelectAttributesCheckbox %s 1 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
        else:
            for all in trsList:
                trsaxis = all + axisInput
                mel.eval('filterUISelectAttributesCheckbox %s 1 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
            for all in trsList:
                for axisoff in axisList_off:
                    trsaxis = all + axisoff
                    mel.eval('filterUISelectAttributesCheckbox %s 0 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
   
def trsFilterBtnChanged(trsInput,which,*args):
    getAttrFilter_axis()
    trsList = ['translate', 'rotate', 'scale']
    if len(getAttrFilter_axis()) == 0:
        axisList = ['X','Y','Z']
    else:
        axisList = getAttrFilter_axis()
        trsList_on = getAttrFilter_attr()
        trsList_off = list(set(trsList)-set(trsList_on))
    if which == 0:
        for all in axisList:
            trsaxis = trsInput+all
            mel.eval('filterUISelectAttributesCheckbox %s 0 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
        if len(getAttrFilter_axis()) == 0:
            pass
        else:
            for on in axisList:
                trs_left = getAttrFilter_attr()
                if len(trs_left) == 0:
                    for trs in trsList:
                        trsaxis_on = trs + on
                        mel.eval('filterUISelectAttributesCheckbox %s 1 GE_ui_scriptedPanelOutlineEd;' %trsaxis_on)
                else:
                    pass
            
    if which == 1:
        if len(axisList) == 3:
            for all in axisList:
                trsaxis = trsInput+all
                mel.eval('filterUISelectAttributesCheckbox %s 1 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
        else:
            for all in axisList:
                trsaxis = trsInput+all
                mel.eval('filterUISelectAttributesCheckbox %s 1 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
            for all in axisList:
                for trsoff in trsList_off:
                    trsaxis = trsoff + all
                    mel.eval('filterUISelectAttributesCheckbox %s 0 GE_ui_scriptedPanelOutlineEd;' %trsaxis)
                    
     
def clearattrFilterBtn(*args):
    attrFilterBtnList=['translateFilterBtn','rotateFilterBtn','scaleFilterBtn','XFilterExcuteBtn','YFilterExcuteBtn','ZFilterExcuteBtn']
    for all in attrFilterBtnList:
        cmds.iconTextCheckBox(all,e=1,value=0)
    trsList = ['translate', 'rotate', 'scale']
    axisList= ['X','Y','Z']    
    for trs in trsList:
        for axis in axisList:
            temp = trs + axis
            mel.eval('filterUISelectAttributesCheckbox %s 0 GE_ui_scriptedPanelOutlineEd;' %temp)  
    mel.eval('filterUIClearFilter GE_ui_scriptedPanelOutlineEd;')
    
def run():
    view = "GE_ui_window"

    if cmds.window("GE_ui_window", exists=True):
        cmds.deleteUI("GE_ui_window")
        
    cmds.window("GE_ui_window", title="NAS-Anim Graph Editor")

    cmds.frameLayout("GE_ui_frameLayout", p="GE_ui_window", lv=False, bv=False ) 

    if cmds.scriptedPanel("GE_ui_scriptedPanel", exists=True):
        cmds.deleteUI("GE_ui_scriptedPanel")
        
    cmds.scriptedPanel("GE_ui_scriptedPanel", unParent=True, type="graphEditor")
    cmds.scriptedPanel("GE_ui_scriptedPanel", e=True, parent="GE_ui_window|GE_ui_frameLayout") #parent the scripted panel to your frame layout

    cmds.showWindow("GE_ui_window")

    MasterformLayout = cmds.layout("GE_ui_window|GE_ui_frameLayout|GE_ui_scriptedPanel",query=True, childArray=True)[0]

    ge_row = cmds.layout(MasterformLayout,query=True, childArray=True)[0]
    ge_pane = cmds.layout(MasterformLayout,query=True, childArray=True)[1]

    smoothRowLayout=cmds.rowLayout(numberOfColumns=6,columnWidth6=(100,188,60,45,15,50),h=36, p = MasterformLayout) #Create a Smooth row layout 
    cmds.optionMenu(p=smoothRowLayout)#  changeCommand=printNewMenuItem,
    cmds.menuItem( label='Smooth' )
    cmds.radioButtonGrp('applytoVorT',label="Apply to : ",cl3=["left","left","left"],labelArray2=['Value','Time'],columnWidth3=[60,60,80],numberOfRadioButtons=2,sl=1,p=smoothRowLayout)
    cmds.text(label="Strength : ",p=smoothRowLayout)
    cmds.floatField( 'amount_Strength', min=0, v=0.5, pre=1, w=50 )
    cmds.separator(style="single",p=smoothRowLayout)
    cmds.button(label = " Apply ", p=smoothRowLayout,command=execute)
    cmds.formLayout(MasterformLayout, edit=True, af=[ \
                (ge_pane, "bottom", 0), \
                (smoothRowLayout, "left", 0),  \
                (ge_row, "top", 0),  \
                (ge_pane, "left", 0),  \
                (ge_row, "right", 0)],  \
                ac=[(smoothRowLayout, "top", 0, ge_row), \
                (ge_pane, "top", 0, smoothRowLayout)])

    channelLayout = cmds.formLayout("GE_ui_scriptedPanelOutlineEdForm", query=True, ca=True)[0]
    filterLayout  = cmds.formLayout("GE_ui_scriptedPanelOutlineEdForm", query=True, ca=True)[1]
    filterAttrRowLayout=cmds.rowLayout(numberOfColumns=7, h=36,p="GE_ui_scriptedPanelOutlineEdForm")
    cmds.button(label=" AttrFilter Reset ",p=filterAttrRowLayout,command=clearattrFilterBtn)
    cmds.iconTextCheckBox('translateFilterBtn',label="T",i = iconFolder + '\\AttrFilterTranslate.png',w=20,h=26, p=filterAttrRowLayout,onc=partial(trsFilterBtnChanged, 'translate', 1),ofc=partial(trsFilterBtnChanged, 'translate', 0))
    cmds.iconTextCheckBox('rotateFilterBtn'  ,label="R",i = iconFolder + '\\AttrFilterRotate.png',w=20,h=26, p=filterAttrRowLayout,onc=partial(trsFilterBtnChanged, 'rotate', 1),ofc=partial(trsFilterBtnChanged, 'rotate', 0))
    cmds.iconTextCheckBox('scaleFilterBtn'   ,label="S",i = iconFolder + '\\AttrFilterScale.png',w=20,h=26, p=filterAttrRowLayout,onc=partial(trsFilterBtnChanged, 'scale', 1),ofc=partial(trsFilterBtnChanged, 'scale', 0))
    cmds.iconTextCheckBox('XFilterExcuteBtn' ,label="X",i = iconFolder + '\\AttrFilterX.png',w=20,h=26, p=filterAttrRowLayout,onc=partial(attrFilterBtnChanged, 'X', 1),ofc=partial(attrFilterBtnChanged, 'X', 0))
    cmds.iconTextCheckBox('YFilterExcuteBtn' ,label="Y",i = iconFolder + '\\AttrFilterY.png',w=20,h=26, p=filterAttrRowLayout,onc=partial(attrFilterBtnChanged, 'Y', 1),ofc=partial(attrFilterBtnChanged, 'Y', 0))
    cmds.iconTextCheckBox('ZFilterExcuteBtn' ,label="Z",i = iconFolder + '\\AttrFilterZ.png',w=20,h=26, p=filterAttrRowLayout,onc=partial(attrFilterBtnChanged, 'Z', 1),ofc=partial(attrFilterBtnChanged, 'Z', 0))

    cmds.formLayout("GE_ui_scriptedPanelOutlineEdForm", edit=True, af=[ \
                (channelLayout, "bottom", 0), \
                (channelLayout, "right", 0),  \
                (filterLayout, "top", 0),  \
                (filterAttrRowLayout, "left", 0),  \
                (filterAttrRowLayout, "right", 0)],  \
                ac=[(filterAttrRowLayout, "top", 0, filterLayout), \
                (channelLayout, "top", 0, filterAttrRowLayout)])
