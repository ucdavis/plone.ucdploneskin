## Script (Python) "getTabs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=portal_tabs
##title=
##


tabAr1 = []
tabAr2 = []

secondTabRow = context.portal_properties.ucdploneskin_properties.secondTabRow
secondTabRowAr = secondTabRow.split(',')

for tab in portal_tabs:

  if tab['id'] in secondTabRowAr:
    tabAr2.append(tab)

  else:
    tabAr1.append(tab)


tabRows = []

if len(tabAr1):
  tabRows.append(tabAr1)

if len(tabAr2):
  tabRows.append(tabAr2)


return(tabRows)