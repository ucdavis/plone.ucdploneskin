## Script (Python) "checkBgImageNoRepeat"
##bind context=context

# called in ploneCustom.css.dtml to decide if we should
# repeat the optional bg image

if context.portal_properties.ucdploneskin_properties.bgImageNoRepeat == 1:
  return 1

else:
  return 0 