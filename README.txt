Description

  This is a Plone product that implements the UCD web template.

Install

  Extract the archive to your Zope Products directory, then restart Zope.
  Click the 'Preferences' link in Plone, then click the 'Add/Remove Products'
  link.  Select the product, then click the 'Install' button.

  This product is known to work with Plone 2.5.1, but should also work with
  older versions.

  Please note that Plone 2.5.1 has a security flaw and the hotfix should be
  applied. See http://plone.org/products/plone-hotfix/releases/20061031/

  See https://svn.cse.ucdavis.edu/trac/UCDPloneSkin/wiki/Install for the
  latest installation instructions.

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

  If you choose to turn off the "Automatically generate tabs" option and use
  portal_actions instead, be very careful that the action Id that you specify 
  matches the short name of the object that the tab should link to.  The tab Id
  needs to match the object Id so we can determine which tab is currently
  selected, compare, and dim the selected tab.

  Also regarding the portal_tabs, if you have a "content item selected as
  default view" in one of the folders that represents a portal_tab, it should
  have the same short name as the folder.  For instance, let's say I have a
  portal tab with an Id of foo.  It links to a folder with a short name of foo.
  If I create a page to serve as the default for that folder, it's short name
  should also be foo.  If not, the tab won't be dimmed properly.

  During the installation of this skin an attempt is made at hiding the Join
  link, although it seems to fail occasionaly.  I assume most departments don't
  want to open the portal membership to the general public and will probably
  use alternative authentication, such as CAS.  If you wish to show the Join
  link, remove the files UCDPloneSkin/skins/ucdploneskin/join_form.*.  Also,
  use the ZMI to navigate to portal_registration, find the Join action,
  select Visable and click Save.

  Speaking of CAS, if you use install PloneCASLogin after installing this skin,
  it will add a portlet_login item to the left slot.  To remove this, go to the
  ZMI and go to your plone site's property tab.  There you can clear the left
  slot.

  Also, if you use CAS you should consider turning off member folder creation
  in portal_membership.  If you don't, random CAS users will have valid member
  folders where they can create content.

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

  RSS is hidden, but not turned off, to see it: add "/RSS" to the end of a
  smart folder

  The uninstaller doesn't reset all settings, such as time format 
