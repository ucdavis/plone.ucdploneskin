## Script (Python) "checkBgImage"
##bind context=context

# called in ploneCustom.css.dtml to decide if we should use
# a bg image in the css 

if 'ucdploneskin-bgImage' in context.portal_properties.keys():
  return 1

else:
  return 0