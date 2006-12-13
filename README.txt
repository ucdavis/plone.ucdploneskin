Description

  This is a Plone product that implements the UCD web template.

Install

  Extract the archive to your Zope Products directory, then restart Zope.
  Click the 'Preferences' link in Plone, then click the 'Add/Remove Products'
  link.  Select the product, then click the 'Install' button.

  This product is known to work with Plone 2.5.1, but should also work with
  older versions.

Basic Customization

  Click the 'Preferences' link in Plone, scroll down to
  'Add-on Product Configuration', then click 'UCDPloneSkin'.  There you can
  change the portal title and department contact info as well as add, edit
  and remove Quick Links.

Further Customization

  The portal tabs and "In This Section" links are automatically generated.
  Use the "Exclude From Navigation" property of any Plone object if you want
  to prevent it from showing up in those navigation elements.

  You have the option of blue or gold portal_tabs.  If you want to switch to
  blue tabs, open UCDPloneSkin/skins/ucdploneskin/ploneCustom.css.dtml and
  look for the commented portal-globalnav styles.  Maybe we'll add the option
  to have two rows of tabs in the future.

  If you find a need to rename the home page or specify a different object as
  the home page, please use the ZMI to make sure the short name is
  "front-page".  The name is used in a few conditional statements that
  determine how certain skin elements should display, such as the breadcrumbs
  and browser title bar.

  During the installation of this skin an attempt is made at hiding the Join
  link, although it seems to fail occasionaly.  I assume most departments don't
  want to open the portal membership to the general public and will probably
  use alternative authentication, such as CAS.  If you wish to show the Join
  link, remove the files UCDPloneSkin/skins/ucdploneskin/join_form.*.  Also,
  use the ZMI to navigate to portal_registration, find the Join action,
  select Visable and click Save.

  Speaking of CAS, if you use it you should probably customize or delete the
  portlet_login page template.  It causes a login area to display in the left
  nav.  I wonder if this skin product can override it with some sort of reverse
  inheritance?

Credits

  Author: Charles McLaughlin, cmclaughlin@ucdavis.edu
  Feedback and questions are welcome.

  Thanks to University Communications for designing the web template.  Refer
  to their website for information about the original html template:

    http://ucomm.ucdavis.edu/pubguide/web_templates.html

  Thanks to Brian Gingold for testing this product.

  This skin was initially created with the Plone Skin Dump product:
    http://quintagroup.com/services/plone-development/products/skin-dump


Known Issues
  
  Hover problem near page title/up one level

  The spacing doesn't exactly match the original template

  There is a very small gap in between the portal tabs and the bottom border

  There is a 1px gap between Quick Links and In This Section <li> elements

  RSS is hiden, but not turned off

  The uninstaller doesn't reset all settings, such as time format 
