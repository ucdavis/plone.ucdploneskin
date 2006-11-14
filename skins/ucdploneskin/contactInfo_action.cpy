from Products.CMFCore.utils import getToolByName


deptName = context.REQUEST.get('deptName', None)
address1 = context.REQUEST.get('address1', None)
address2 = context.REQUEST.get('address2', None)
address3 = context.REQUEST.get('address3', None)
address4 = context.REQUEST.get('address4', None)
phone1 = context.REQUEST.get('phone1', None)
phone2 = context.REQUEST.get('phone2', None)
fax1 = context.REQUEST.get('fax1', None)
fax2 = context.REQUEST.get('fax2', None)


portal = context.portal_url.getPortalObject()
pp = getToolByName(portal, 'portal_properties')
pp_ucd_props = pp.ucdploneskin_properties


# set provided values
portal.manage_changeProperties(title=deptName)
pp_ucd_props.manage_changeProperties(address1=address1)
pp_ucd_props.manage_changeProperties(address2=address2)
pp_ucd_props.manage_changeProperties(address3=address3)
pp_ucd_props.manage_changeProperties(address4=address4)
pp_ucd_props.manage_changeProperties(phone1=phone1)
pp_ucd_props.manage_changeProperties(phone2=phone2)
pp_ucd_props.manage_changeProperties(fax1=fax1)
pp_ucd_props.manage_changeProperties(fax2=fax2)


# return to form w/ status msg

state.setNextAction('redirect_to:string:ucdploneskin_config')

state.setKwargs({'portal_status_message':'Your changes were saved.'})

return state

