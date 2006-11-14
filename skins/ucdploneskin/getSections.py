## Script (Python) "getSections"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=basePath,levels=None,types=None,getLen=None,current=None,filter={}
##title=Creates the list of sections to show in the "in this section" navigation
##
from Products.CMFCore.utils import getToolByName

# basePath: The path to the parent of the sections to find. Should be relative
#   to the portal root and start with a /. As a special case, pass '.' to get
#   use the context as the path.
# levels: How deep to go. Get all content if not given.
# types: What portal types to search for. Leave as None to search for all types
# getLen: if 1, return the length of the array
# current: The current item - will get 'current' set to True. Defaults to 
#   context.
# filter: A dict with catalog query parameters to filter the result set.
#           
# Returns a recursive list of sections and their sub-sections. Each section
# is represented as a dict with the keys:
#
#   id       : the id of this item
#   item     : a catalog brain for this item
#   current  : True if this is the current item
#   children : a list of children, each a dict with the same keys as this one

urltool = getToolByName(context, 'portal_url')

if basePath == '.':
    if context.is_folderish():
        basePath = '/'.join(context.getPhysicalPath())
    else:
        basePath = '/'.join(context.aq_inner.aq_parent.getPhysicalPath())
else:
    basePath = urltool.getPortalPath() + basePath

if current is None:
    current = context

catalog = getToolByName(context, 'portal_catalog')

query = filter
query['sort_on'] = 'getObjPositionInParent'

if levels is not None and levels > 0:
    query['path'] = {'query' : basePath, 'depth' : levels}
else:
    query['path'] = basePath
    
if types:
    query['portal_type'] = types

results = catalog.searchResults(query)


def insertElement(toc, item, current, basePath):

    # The query gives us a flat list of results. Each item has a path. We take
    # away the first part of this path, basePath, and are left with the
    # parts of the path (sub-folders of basePath and the item itself) that
    # will go into the TOC. For each item, we then process each part of this
    # path, inserting it into the recursive toc structure. Along the way, we
    # may need to insert placeholders if a child item arrives before its
    # parent.

    subpath = item.getPath()[len(basePath) + 1:]
    pathElements = subpath.split('/')
    currentList = toc

    # Yes, this is slightly wasteful, but we're talking about at most a
    # few items in tocList, and I like the prettiness of these 
    # constructs. If you don't like it, refactor at your own risk. :)

    hasItem = lambda tocList, item: item in [t['id'] for t in tocList]
    itemIndex = lambda tocList, item: [t['id'] for t in tocList].index(item)

    # Check if this is the current item or a parent thereof
    if current:
        currentPath = '/'.join(current.getPhysicalPath())
        itemPath = item.getPath()
        if currentPath.startswith(itemPath):
            isCurrent = True
        else:
            isCurrent = False
    else:
        isCurrent = False

    processedParts = 0
    totalParts = len(pathElements)

    # Consider each part of the item's path, i.e. each folder under basePath
    # and the item itself
    for part in pathElements:
        processedParts += 1

        # It is possible that we have placeholder item before (see below)
        # - if so, update it now
        if hasItem(currentList, part):
            idx = itemIndex(currentList, part)
            currentItem = currentList[idx]
            if processedParts == totalParts:
                if currentItem['item'] is None:
                    currentItem['item']      = item
                    currentItem['current']   = isCurrent
                
        elif processedParts != totalParts:
            # If this is not the last part of pathElements, then we
            # have gotten a child of the current part before the part
            # itself. Thus, insert a placeholder, and update later
            idx = len(currentList)
            currentList.append({'id'        : part,
                                'item'      : None,
                                'current'   : None,
                                'active'    : None,
                                'children'  : []})

        else:
            # We are at the end item, and we don't have it in the list,
            # so add a new item
            idx = len(currentList)
            currentList.append({'id'        : part,
                                'item'      : item,
                                'current'   : isCurrent,
                                'active'    : None,
                                'children'  : []})
                                
        if isCurrent:
            currentList[idx]['active'] = True

        currentList = currentList[idx]['children']

toc = []
for r in results:
    # Query will return the base path as well as all children, so filter this
    if r.getURL() != basePath and not r.exclude_from_nav:
        insertElement(toc, r, current, basePath)

if getLen:
    return len(toc);

return toc
