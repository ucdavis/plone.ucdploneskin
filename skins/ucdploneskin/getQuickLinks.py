class QuickLink:
    # we're using this like a c-style struct
    pass
     

# loop through each quicklink in the properties, add to list

qlList = []

for currItem in context.portal_properties.ucdploneskin_properties.propertyItems():

    if currItem[0].startswith("quicklink"):

        tokens = currItem[1].split(',')
   
        ql = QuickLink()

        ql.text = tokens[0]
        ql.url = tokens[1]

        ql.qlID = currItem[0]

        qlList.append(ql)

return qlList