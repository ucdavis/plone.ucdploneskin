## Script (Python) "checkExcludeFromNav"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=path
##title=
##


# could have done this check in portlet_nav_tree macro, but
# we need to handle content types that don't have the
# excludeFromNav field

try:
  return(context.restrictedTraverse(path).getExcludeFromNav())
except:
  return 0

