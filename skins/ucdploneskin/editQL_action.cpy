from Products.CMFCore.utils import getToolByName


# custom sort compare function

def myCmp(x, y):
    return cmp(x[0], y[0])


qlText = context.REQUEST.get('qlText', None)
qlURL = context.REQUEST.get('qlURL', None)
qlID = context.REQUEST.get('qlID', None)
delete = context.REQUEST.get('delete', None)


portal_url  = getToolByName(context, 'portal_url')
portal      = portal_url.getPortalObject()
pp = getToolByName(portal, 'portal_properties')
pp_ucd_props = pp.ucdploneskin_properties


# coudn't figure out how to changeProperty w/ property id as a variable
# so as a work around delete the property and add a new one
# if user specified delete, then we don't re-add

pp_ucd_props.manage_delProperties([qlID])

if not delete:
  prop = qlText + ',' + qlURL
  pp_ucd_props.manage_addProperty(qlID, prop, 'string')


# now that we've done the requested work, delete all 
# saved quicklinks, sort by id, then re-add
# this ensures that the links are sorted by date added
# we could do this in getQuickLinks.py, but that would require
# sorting during every page access - this kinda messy, but it is
# only a one time operation

propList = context.portal_properties.ucdploneskin_properties.propertyItems()

propList.sort(myCmp)

# delete existing quick links
for currItem in propList:
  if currItem[0].startswith("quicklink"):
    pp_ucd_props.manage_delProperties([currItem[0]])

# re-add props
i = 1

for currItem in propList:
  if currItem[0].startswith("quicklink"):
    qlID = 'quicklink' + str(i)
    pp_ucd_props.manage_addProperty(qlID, currItem[1], 'string')
    i += 1


# return to form w/ status msg

state.setNextAction('redirect_to:string:ucdploneskin_config')

state.setKwargs({'portal_status_message':'Your changes were saved.'})

return state

