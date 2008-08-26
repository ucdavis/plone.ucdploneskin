Introduction
============

Installation for development

    UC davis development team advises to use buildout for your projects, built with Plone
    3.x.
    
    The buildout way:
    
        1. download skin from svn repository in your src directory of your plone instance
        	$cd {path to your src of your plone instance}
        	$svn co svn co https://svn.cse.ucdavis.edu/repo/UCDPloneSkin/trunk Products.ucdavis.ucdskin
        	
        2. Edit your buildout.cfg and add the following information::
    
            [buildout]
            ...
            # Reference any eggs you are developing here, one per line
            # e.g.: develop = src/my.package
            develop =
                src/Products.ucdavis.ucdskin
            ...
            [instance] section (or [client1] if zeo)
	    ...
	    # If you want Zope to know about any additional eggs, list them here.
	    # This should include any development eggs you listed in develop-eggs above,
	    # e.g. eggs = ${buildout:eggs} ${plone:eggs} my.package
	   eggs =
	       ${buildout:eggs}
	       ${plone:eggs}
	       Products.ucdavis.ucdskin

    
        If another package depends on the Products.ucdavis.ucdskin egg or includes
        its zcml directly you do not need to specify anything in the buildout
        configuration: buildout will detect this automatically.

        After updating the configuration you need to run the ''bin/buildout'',
        which will take care of updating your system.

    Go to the 'Site Setup' page in the Plone interface and click on the
    'Add/Remove Products' link.
    
    Choose the product (check its checkbox) and click the 'Install' button.
    
    Uninstall -- This can be done from the same management screen, but only
    if you installed it from the quick installer.

    Note: You may have to empty your browser cache to see the effects of the
    product installation.

Credits
    Lets put our credits here