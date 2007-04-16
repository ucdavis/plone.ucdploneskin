from Products.CMFCore.utils import getToolByName
import string

class QuickLink:
    # we're using this like a c-style struct
    pass
     


qlList = []
portal_url  = getToolByName(context, 'portal_url')


# loop through each quicklink in the properties, add to list

for currItem in context.portal_properties.ucdploneskin_properties.propertyItems():

    if currItem[0].startswith('quicklink'):

        tokens = currItem[1].split(',')
   
        ql = QuickLink()

        ql.text = tokens[0]
        ql.url = tokens[1]
        ql.qlID = currItem[0]


        # look for portal_url variable inside

        startPos = ql.url.find('${portal_url}')
        endPos = ql.url.find('}')

        if startPos > -1 and endPos > -1:

          strippedURL = ql.url[endPos+1:]

          ql.url = portal_url() + strippedURL


        qlList.append(ql)

return qlList