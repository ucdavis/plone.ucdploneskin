from Products.CMFCore.utils import getToolByName


searchbox = context.REQUEST.get('searchbox', None)
copyright = context.REQUEST.get('copyright', None)
privacyStatement = context.REQUEST.get('privacyStatement', None)
showAccessibility = context.REQUEST.get('showAccessibility', None)
bgImage = context.REQUEST.get('bgImage', None)
deleteBgImage = context.REQUEST.get('deleteBgImage', None)


portal = context.portal_url.getPortalObject()
pp = getToolByName(portal, 'portal_properties')
pp_ucd_props = pp.ucdploneskin_properties


# set provided values
pp_ucd_props.manage_changeProperties(searchbox=searchbox)
pp_ucd_props.manage_changeProperties(copyright=copyright)
pp_ucd_props.manage_changeProperties(privacyStatement=privacyStatement)
pp_ucd_props.manage_changeProperties(showAccessibility=showAccessibility)


if deleteBgImage:
  pp.manage_delObjects(['ucdploneskin-bgImage'])


if bgImage:

  try:
    pp.manage_delObjects(['ucdploneskin-bgImage'])
  except:
    pass # ignore error in case img doesn't exist

  pp.manage_addImage('ucdploneskin-bgImage', bgImage)



# return to form w/ status msg

state.setNextAction('redirect_to:string:ucdploneskin_config')

state.setKwargs({'portal_status_message':'Your changes were saved.'})

return state

