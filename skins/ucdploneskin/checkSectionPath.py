if len(context.getPhysicalPath()) == 2:
    #  we're in the portal root (includes viewing special pages, such as the 
    #  login/out page)
    return(0)

if len(context.getPhysicalPath()) == 3:
    if context.is_folderish():
        # we're viewing a sub folder listing
        return(1)
    else:
        # we're in the portal root viewing normal pages
        return(0)

else:
    if len(context.getPhysicalPath()) >= 4:
        # we're in a subfolder viewing a page
        return(1)