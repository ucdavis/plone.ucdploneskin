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

      if(tree['children'][0]['path'] == context.absolute_url_path()
         and context.checkExcludeFromNav(context.absolute_url_path()) ):
        return False
      else:
        return True

    if(root is not None and len(tree['children']) == 0):
      # I don't think this will ever happen because
      # the currently viewed item is a child
      return False

    return True  # if all other cases fail
