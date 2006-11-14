from Products.CMFCore.utils import getToolByName

qlText = context.REQUEST.get('qlText', None)
qlURL = context.REQUEST.get('qlURL', None)



# loop thru existing quicklinks, get highest id number
# quick link will be named +1

i = 0

for currItem in context.portal_properties.ucdploneskin_properties.propertyItems():
  if currItem[0].startswith("quicklink"):
    if int(currItem[0].lstrip('quicklink')) > i:
      i = int(currItem[0].lstrip('quicklink'))

i += 1


# prep work

propName = 'quicklink' + str(i)
propVal = qlText + ',' + qlURL


# add given values

portal_url  = getToolByName(context, 'portal_url')
portal      = portal_url.getPortalObject()
pp = getToolByName(portal, 'portal_properties')
pp_ucd_props = pp.ucdploneskin_properties
pp_ucd_props.manage_addProperty(propName, propVal, 'string')


# return to form w/ status msg

state.setNextAction('redirect_to:string:ucdploneskin_config')

state.setKwargs({'portal_status_message':'Your changes were saved.'})

return state

