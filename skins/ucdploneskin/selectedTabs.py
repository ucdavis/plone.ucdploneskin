## Script (Python) "selectedTabs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=default_tab, obj=None, portal_tabs=[]
##title=
##
from AccessControl import Unauthorized

valid_actions = []

# hack job - the tab will only be selected if we're viewing that page
# not sure what the first arg to append does, but this seems to work

valid_actions.append((1, context.id))

return {'portal':valid_actions[-1][1]}
