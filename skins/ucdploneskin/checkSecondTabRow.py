## Script (Python) "checkSecondTabRow"
##bind context=context

# called in ploneCustom.css.dtml to decide how to style tabs

from Products.CMFCore.utils import getToolByName

# get the portal object
container = context.aq_inner.aq_parent

atool = getToolByName(context, 'portal_actions')
actions = atool.listFilteredActionsFor(container)
portal_tabs_view = container.restrictedTraverse('@@portal_tabs_view')

tabs = portal_tabs_view.topLevelTabs(actions)

secondTabRow = context.portal_properties.ucdploneskin_properties.secondTabRow
secondTabRowAr = secondTabRow.split(',')

# we have stuff in the second row

if secondTabRow:

  # loop through the list of portal tabs, if any one tab isn't in the second
  # row, then we we have two rows

  for tab in tabs:
    if tab['id'] not in secondTabRowAr:
      return 1

return 0