from Products.CMFPlone.browser.portlets.navigation import NavigationPortlet
from Products.CMFPlone import utils

class MyNavPortlet(NavigationPortlet):
  def display(self):   
    tree = self.getNavTree()
    root = self.getNavRoot()

    context = utils.context(self)

    if(root is not None and len(tree['children']) > 1):
      return True

    if(root is not None and len(tree['children']) == 1):
      # if current item is marked excludeFromNav
      # and its the only item in the folder
      # then we shouldn't display the entire navtree

      # tree....['path'] returns the path w/o the zope instance
      # this seems hackish (perhaps a catalog look up would be faster)
      # but ensures we compare apples to apples

      path = context.restrictedTraverse(tree['children'][0]['path']).absolute_url_path()

      # need to strip off /instance/portal/ from path

      strippedPath = path

      i = 0

      while i < 3:
        index = strippedPath.find('/')         
        strippedPath = strippedPath[index+1:len(strippedPath)]
        i += 1


      # done with the setup, now decide what to return
      
      if(path == context.absolute_url_path()
         and context.checkExcludeFromNav(strippedPath)):
        return False
      else:
        return True

    if(root is not None and len(tree['children']) == 0):
      # I don't think this will ever happen because
      # the currently viewed item is a child
      return False

    return True  # default
