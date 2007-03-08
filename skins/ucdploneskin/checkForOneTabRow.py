## Script (Python) "checkSecondTabRow"
##bind context=context

# called in ploneCustom.css.dtml to decide how to style tabs
# returns true if any one tab isn't in the second row

secondTabRow = context.portal_properties.ucdploneskin_properties.secondTabRow
secondTabRowAr = secondTabRow.split(',')

for tab in context.plone_utils.createTopLevelTabs():
  if tab['id'] not in secondTabRowAr:
    return 1

return 0
