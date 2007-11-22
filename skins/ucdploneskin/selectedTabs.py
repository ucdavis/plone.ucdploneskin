## Script (Python) "selectedTabs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=default_tab, obj=None, portal_tabs
##title=
##


try:

  if context.aq_inner.aq_parent.getDefaultPage() == 'front-page':
    return {'portal':context.id}

  elif context.aq_inner.aq_parent.getDefaultPage() == context.id:
    return {'portal':context.aq_inner.aq_parent.id}

except:
  pass  # ignore errorsin case we're viewing special pages such as
        #plone_control_panel


return {'portal':context.id}
