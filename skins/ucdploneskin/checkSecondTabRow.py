## Script (Python) "checkSecondTabRow"
##bind context=context

# called in ploneCustom.css.dtml to decide how to style tabs

if context.portal_properties.ucdploneskin_properties.secondTabRow:
  return 1

else:
  return 0