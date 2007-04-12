from Products.UCDPloneSkin.config import *
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Products.CMFCore.DirectoryView import addDirectoryViews
import string


def install(self):
    out=StringIO()
    # Checking base condition for installation
    skinsTool = getToolByName(self, 'portal_skins')

    # Checking for BASE_SKIN_NAME presenting in portal
    skin_names = skinsTool.getSkinSelections()
    if not BASE_SKIN_NAME in skin_names:
        raise AttributeError("Impossible installation without %s skin." % BASE_SKIN_NAME)

    # Checking for presenting lower_SKIN_NAME directory in portal skins
    lower_SKIN_NAME = string.lower(SKIN_NAME)
    if lower_SKIN_NAME in skinsTool.objectIds():
        raise AttributeError("%s skin layer already exist in portal skins. Installation Impossible." % lower_SKIN_NAME)

    out.write("%s generated product" % GENERATOR_PRODUCT)
    return out.getvalue()


# For prevent quickInstaller's intervention 
# in uninstall process - use afterInstall
def afterInstall(self,product,reinstall):
    out=StringIO()
    
    # get all needed tools and some portal's core objects
    portal = self.portal_url.getPortalObject()
    pp = getToolByName(portal, 'portal_properties')
    portal_css = getToolByName(portal, 'portal_css', None)

    prepareInstallation(portal, pp, product, out)
    pp_up = pp.uninstall_properties

    installSkin(portal, pp_up, out)
    
    if portal_css:
        registerCSS(pp_up, portal_css, out)
    
    if LEFT_SLOTS or RIGHT_SLOTS:
        customizeSlots(portal, pp_up, out)


    # customizations

    # set time format & hide join link
    pp.site_properties.manage_changeProperties(localTimeFormat='%B %d, %Y')
    pp.site_properties.manage_changeProperties(localLongTimeFormat='%Y-%m-%d %I:%M %p')


    # set role so only managers can add users (disables join link)
    pr = getToolByName(portal, "portal_registration")
    for action in pr.listActions():
        if action.id == "join":
            action.visible = 0


    # turn off byline for anon users
    pp.site_properties.manage_changeProperties(allowAnonymousViewAbout=0)


    # add dept info properties

    if not ('ucdploneskin_properties' in pp.objectIds()):
      pp.addPropertySheet(id='ucdploneskin_properties', title= 'ucdploneskin_properties')

    pp_ucd_props = pp.ucdploneskin_properties

    if not pp_ucd_props.hasProperty('address1'):
      addProperty(pp_ucd_props, 'address1', 'Room# Building', 'string', out)

    if not pp_ucd_props.hasProperty('address2'):
      addProperty(pp_ucd_props, 'address2', 'University of California, Davis', 'string', out)

    if not pp_ucd_props.hasProperty('address3'):
      addProperty(pp_ucd_props, 'address3', 'One Shields Avenue', 'string', out)

    if not pp_ucd_props.hasProperty('address4'):
      addProperty(pp_ucd_props, 'address4', 'Davis, CA 95616', 'string', out)

    if not pp_ucd_props.hasProperty('phone1'):
      addProperty(pp_ucd_props, 'phone1', '(530) 752-9999', 'string', out)

    if not pp_ucd_props.hasProperty('phone2'):
      addProperty(pp_ucd_props, 'phone2', '', 'string', out)

    if not pp_ucd_props.hasProperty('fax1'):
      addProperty(pp_ucd_props, 'fax1', '(530) 752-9999', 'string', out)

    if not pp_ucd_props.hasProperty('fax2'):
      addProperty(pp_ucd_props, 'fax2', '', 'string', out)
 
    if not pp_ucd_props.hasProperty('searchbox'):
      addProperty(pp_ucd_props, 'searchbox', '', 'boolean', out)

    if not pp_ucd_props.hasProperty('showAccessibility'):
      addProperty(pp_ucd_props, 'showAccessibility', '1', 'boolean', out)

    if not pp_ucd_props.hasProperty('copyright'):
      addProperty(pp_ucd_props, 'copyright', 'Copyright &copy; The Regents of the University of California, Davis campus 2005-06. All Rights Reserved.', 'string', out)

    if not pp_ucd_props.hasProperty('privacyStatement'):
      addProperty(pp_ucd_props, 'privacyStatement', 'http://manuals.ucdavis.edu/ppm/310/310-70a.htm', 'string', out)

    if not pp_ucd_props.hasProperty('bgImageNoRepeat'):
      addProperty(pp_ucd_props, 'bgImageNoRepeat', '', 'boolean', out)

    if not pp_ucd_props.hasProperty('showPrivacyStatement'):
      addProperty(pp_ucd_props, 'showPrivacyStatement', '', 'boolean', out)

    if not pp_ucd_props.hasProperty('secondTabRow'):
      addProperty(pp_ucd_props, 'secondTabRow', '', 'string', out)


    # navigation settings
    pp.portal_properties.navtree_properties.manage_changeProperties(includeTop=0)
    pp.portal_properties.navtree_properties.manage_changeProperties(topLevel=1)
    pp.portal_properties.navtree_properties.manage_changeProperties(currentFolderOnlyInNavtree=1)



    # add quicklink examples if none exist

    if not ('quicklink1' in pp_ucd_props.propertyIds()):
      addProperty(pp_ucd_props, 'quicklink1', 'University Library,http://www.lib.ucdavis.edu/', 'string', out)
      addProperty(pp_ucd_props, 'quicklink2', 'MyUCDavis,http://my.ucdavis.edu', 'string', out)
      addProperty(pp_ucd_props, 'quicklink3', 'Search,search_form', 'string', out)


    # check if configlet exists

    portal_conf=getToolByName(self,'portal_controlpanel')

    addConfiglet = 1

    for action in portal_conf.listActions():
      if action.id == "UCDPloneSkin":
        addConfiglet = 0


    # add configlet if this is a first-time install (not an upgrade)

    if addConfiglet:
      portal_conf.registerConfiglet( 'UCDPloneSkin'
               , 'UCDPloneSkin'      
               , 'string:${portal_url}/ucdploneskin_config' 
               , ''                 # a condition   
               , 'Manage portal'    # access permission
               , 'Products'         # section to which the configlet should be added: 
                                    #(Plone,Products,Members) 
               , 1                  # visibility
               , 'UCDPloneSkin'                                        
               , 'secondary_mark_2.gif' # icon in control_panel, put your own icon in the 
                                        # /skins folder of your product and change 
                                        # 'site_icon.gif' to 'yourfile'
               , ''
               , None
                                   )



def prepareInstallation(portal, pp, product, out):
    # Check for success installation
    checkSuccessInstall(product)

    # Uninstall presenting skin-products
    uninstallOtherSkinProducts(portal)

    # Add uninstall_properties to portal_properties
    if not ('uninstall_properties' in pp.objectIds()) :
        pp.addPropertySheet(id='uninstall_properties', title= 'uninstall_properties')
        out.write("Created 'portal_properties.uninstall_properties' ProperySheet (UP) for backup purpose\n")


def checkSuccessInstall(product):
    seek_str = "%s generated product" % GENERATOR_PRODUCT
    transcript = getattr(product,'transcript',None)
    if transcript:
        msg = str(transcript[0]['msg'])
        if msg.find(seek_str) < 0 :
            raise
    

def uninstallOtherSkinProducts(portal):
    qi=getToolByName(portal, 'portal_quickinstaller', None)
    if not qi:
        raise Exception("Can't work without QuickInstaller tool.")
    # Get installed products
    installed_products = [getattr(qi, p_dict['id']) \
                          for p_dict in qi.listInstalledProducts()
                          if p_dict['id'] != PRODUCT_NAME]
    seek_str = "%s generated product" % GENERATOR_PRODUCT
    installed_skin_products = []
    # Looking for installed skin-products
    for p in installed_products:
        transcript = getattr(p,'transcript',None)
        if transcript:
            msg = str(transcript[0]['msg'])
            if msg.find(seek_str) >= 0 :
                installed_skin_products.append(p.getId())
    # Uninstall found skin-products
    if installed_skin_products:
        qi.uninstallProducts(products=installed_skin_products)


def installSkin(portal, pp_up, out):
    # Checking for presense SKIN_NAME in portal_skins directory view or among Skin Names
    skinsTool = getToolByName(portal, 'portal_skins')
    
    # Get unique product_skin_name and remember it in case of differ from SKIN_NAME.
    product_skin_name = SKIN_NAME
    skin_names = skinsTool.getSkinSelections()
    if product_skin_name in skin_names:
        idx = 0
        while product_skin_name in skin_names:
            product_skin_name = SKIN_NAME + str(idx)
            idx += 1
        addProperty(pp_up, 'q_actual_skin_name', product_skin_name, 'string', out)

    # Add directory views
    layer_skin_name = string.lower(SKIN_NAME)
    addDirectoryViews(skinsTool, 'skins', SKIN_GLOBALS)
    out.write( "- added '%s' directory views to portal_skins.\n" % layer_skin_name)

    # Get Default skin and remember it for backup on uninstallig
    default_skin = skinsTool.getDefaultSkin()
    addProperty(pp_up, 'q_default_skin', default_skin, 'string', out)

    # Building list of layers for NEW SKIN
    base_path = skinsTool.getSkinPath(BASE_SKIN_NAME)
    new_path = map( string.strip, string.split(base_path,',') )
    if layer_skin_name in new_path :
        out.write("- %s layer already present in '%s' skin\n" % (layer_skin_name, BASE_SKIN_NAME))
        # Remove layer_skin_name from current position.
        del new_path[new_path.index(layer_skin_name)]
    # Add layer_skin_name just after 'custom' position
    try: 
        new_path.insert(new_path.index('custom')+1, layer_skin_name)
    except ValueError:
        new_path.append(layer_skin_name)
    new_path = string.join(new_path, ', ')

    # Add NEW Skin and set it as dafault
    skinsTool.addSkinSelection(product_skin_name, new_path, make_default=1)
    out.write("Added %s skin, bassed on %s and set as default\n" % (product_skin_name, BASE_SKIN_NAME) )


def addProperty(p_sheet, p_id, p_value, p_type, out):
    if p_sheet.hasProperty(p_id):
        p_sheet._delProperty(p_id)
    p_sheet._setProperty(p_id, p_value, p_type)
    out.write("... added %s ProperySheet to %s \n" % (p_id, p_sheet) )


def registerCSS(pp_up, portal_css, out):
    # Get original registered css-es
    portal_css_srings = []
    for r in portal_css.getResources():
        r_data = [ r.getId(), r.getExpression(), r.getEnabled() or '', r.getCookable() or '',\
                   r.getMedia() or '', r.getRel(), r.getTitle() or '', r.getRendering() ]
        r_string = ";".join([str(r) for r in r_data])
        portal_css_srings.append(r_string)
    addProperty(pp_up, 'q_registered_css', portal_css_srings, 'lines', out)

    # Tune CSS registry according to new skin needs
    unexistent = [] # list of default css resources, 
                    # which present in Skin-product, BUT absent in portal
    portal_css_ids = portal_css.getResourceIds()
    for css_id, css_enabled in SKIN_CSS_REGDATA:
        if css_id not in portal_css_ids:
            # It's interesting - CSS Registry allow adding unexistent css - use this
            portal_css.registerStylesheet(css_id, media='all', enabled=css_enabled)
            if css_id not in CSS_LIST:
                unexistent.append(css_id)
        else:
            resource = portal_css.getResource(css_id)
            if resource.getEnabled() != css_enabled:
                pos = portal_css.getResourcePosition(css_id)
                res = {'id': css_id,
                       'expression': resource.getExpression(),
                       'enabled': css_enabled,
                       'cookable' : resource.getCookable(),
                       'media': resource.getMedia(),
                       'rel' : resource.getRel(),
                       'title': resource.getTitle(), 
                       'rendering' : resource.getRendering()
                      }
                portal_css.unregisterResource(css_id)
                portal_css.registerStylesheet(**res)
                portal_css.moveResource(css_id, pos)
    if unexistent:
        out.write("!!! - BAD: your CSS Regestry have'nt %s css(es), which may lead to some problem\n" % unexistent)
    out.write("Completed tuning CSS registry for new skin needs")


def customizeSlots(portal, pp_up, out):
    # Get original Site's column lists
    orig_left_slots = list(portal.left_slots)
    orig_right_slots = list(portal.right_slots)

    # Save original Site's LEFT and RIGHT slots
    addProperty(pp_up, 'q_left_slots', orig_left_slots, 'lines', out)
    addProperty(pp_up, 'q_right_slots', orig_right_slots, 'lines', out)

    # blend-with-site - to portal's slots adding only new one from skin-porduct
    # blend-with-skin - portal slots forming in the following manner: 
    #                   first adding skin-porduct's slots, than new one from portal
    # replace - to portal's slots forming only from the skin-porduct's slot list
    if SLOT_FORMING == "blend_with_skin":
        left_column, right_column = formSlotsColumn(LEFT_SLOTS, RIGHT_SLOTS, 
                                                    orig_left_slots, orig_right_slots, MAIN_COLUMN)
    elif SLOT_FORMING == "blend_with_site":
        left_column, right_column = formSlotsColumn(orig_left_slots, orig_right_slots,
                                                    LEFT_SLOTS, RIGHT_SLOTS, MAIN_COLUMN )
    elif SLOT_FORMING == "replace":
        left_column, right_column = formSlotsColumn(LEFT_SLOTS, RIGHT_SLOTS, [], [], MAIN_COLUMN)

    # REPLACE SITE's column slots
    portal.left_slots = tuple(left_column)
    portal.right_slots = tuple(right_column)
    out.write("Complited portal slots customization ...\n")


# main_column ("left" / "right" / "both") mean which of the MAIN column is favour
def formSlotsColumn(main_left, main_right, slave_left=[], slave_right=[], main_column="both"):
    result_left = main_left
    result_right = main_right

    if main_column == "left":
    # 1) APPEND to MAIN_LEFT list *new for main_left column* slots from slave_left list 
    # 2) APPEND to MAIN_RIGHT list *new for both main columns* slots from slave_right
    # 3) REMOVE slots from MAIN_RIGHT list, which are *doubled* in MAIN_LEFT
        [result_left.append(slot) for slot in slave_left if slot not in result_left]
        [result_right.append(slot) for slot in slave_right \
                                   if slot not in result_right and slot not in result_left]
        [result_right.remove(slot) for slot in result_left if slot in result_right]

    elif main_column == "right":
    # 1) APPEND to MAIN_LEFT list *new for main_right column* slots from slave_left list 
    # 2) APPEND to MAIN_RIGHT list *new for both main columns* slots from slave_right
    # 3) REMOVE slots from MAIN_LEFT list, which are *doubled* in MAIN_RIGHT
        [result_right.append(slot) for slot in slave_right if slot not in result_right]
        [result_left.append(slot) for slot in slave_left \
                                  if slot not in result_left and slot not in result_right]
        [result_left.remove(slot) for slot in result_right if slot in result_left]

    elif main_column == "both":
    # 1) APPEND to MAIN_LEFT list *new for both main columns* slots from slave_left list 
    # 2) APPEND to MAIN_RIGHT list *new for both main columns* slots from slave_right
        [result_left.append(slot) for slot in slave_left \
                                  if slot not in result_left and slot not in result_right]
        [result_right.append(slot) for slot in slave_right \
                                   if slot not in result_right and slot not in result_left]
    return [result_left, result_right]

############################################################################
#                                uninstall                                 #
############################################################################
def uninstall(self):
    # get all needed tools and some portal's core objects
    portal = self.portal_url.getPortalObject()
    skinsTool = getToolByName(portal, 'portal_skins')
    pp = getToolByName(portal, 'portal_properties')
    portal_css = getToolByName(portal, 'portal_css', None)
    qi = getToolByName(portal, 'portal_quickinstaller', None)

    # Get all properies, saving during installation, for uninstalling
    actual_skin_name = getPropery(pp, 'uninstall_properties', 'q_actual_skin_name',default=SKIN_NAME)
    initial_skin = getPropery(pp, 'uninstall_properties', 'q_default_skin',default="")
    original_css_list = getPropery(pp, 'uninstall_properties', 'q_registered_css')
    orig_left_slots = getPropery(pp, 'uninstall_properties','q_left_slots')
    orig_right_slots = getPropery(pp, 'uninstall_properties','q_right_slots')

    # Remove 'uninstall_properties' from portal_properties
    if 'uninstall_properties' in pp.objectIds() :
        pp.manage_delObjects(ids=['uninstall_properties',])

    # Get 'portal_skins' object and list available skin names
    # And remove SKIN_NAME from available skins, if it present
    skin_names = skinsTool.getSkinSelections()
    if actual_skin_name in skin_names :
        skinsTool.manage_skinLayers(chosen=(actual_skin_name,), del_skin=1, REQUEST=None)
        skin_names.remove(actual_skin_name)

    # Remove product skin directory from skins tool 
    # AND Remove skin-product layer from available skins
    skin_layer = SKIN_NAME.lower()
    if skin_layer in skinsTool.objectIds():
        skinsTool.manage_delObjects(skin_layer)
    for skin_name in skin_names:
        path = skinsTool.getSkinPath(skin_name)
        path = [i.strip() for i in  path.split(',')]
        if skin_layer in path:
            path.remove(skin_layer)
            path = ','.join(path)
            skinsTool.addSkinSelection(skin_name, path)

    # If current default skin == actual_skin_name
    # Set default skin in initial one (if initial skin still exist) 
    # or in 1st from available skin names list.
    current_default_skin = skinsTool.getDefaultSkin()
    if current_default_skin == actual_skin_name:
        if initial_skin in skin_names :
            skinsTool.manage_properties(default_skin=initial_skin, REQUEST=None)
        elif len(skin_names)>0 :
            skinsTool.manage_properties(default_skin=skin_names[0], REQUEST=None)

    # Unregister skin's CSS-es from portal_css. Only for Plone 2.1+
    if portal_css:
        # Prepare CSS Registry data for backup to original state
        original_css_regestry = {}
        for r in original_css_list:
            r_list = r.split(";")
            original_css_regestry[r_list[0]] = {'expression': r_list[1],
                                                'enabled': r_list[2],
                                                'cookable' : r_list[3],
                                                'media': r_list[4],
                                                'rel' : r_list[5],
                                                'title': r_list[6], 
                                                'rendering' : r_list[7]
                                               }
        # Work up actual CSS Registry
        css_dict = portal_css.getResourcesDict()
        for css_id in css_dict.keys():
            # Remove from CSS Registry Skin product's css resources
            if css_id in CSS_LIST \
               and css_id not in original_css_regestry.keys():
                portal_css.unregisterResource(css_id)
                continue
            # Backup 'enabled' property Registry's resourses to it's original state
            if original_css_regestry.has_key(css_id):
                act_Enabled_state = css_dict[css_id].getEnabled
                orig_Enabled_state = original_css_regestry[css_id]['enabled']
                if act_Enabled_state != orig_Enabled_state:
                    pos = portal_css.getResourcePosition(css_id)
                    resource = css_dict[css_id]
                    res = {'id': css_id,
                           'expression': resource.getExpression(),
                           'enabled': orig_Enabled_state,
                           'cookable' : resource.getCookable(),
                           'media': resource.getMedia(),
                           'rel' : resource.getRel(),
                           'title': resource.getTitle(), 
                           'rendering' : resource.getRendering()
                          }
                    portal_css.unregisterResource(css_id)
                    portal_css.registerStylesheet(**res)
                    portal_css.moveResource(css_id, pos)
            
    # Return site's column slots list unless Skin product installation
    if orig_left_slots:
        portal.left_slots = tuple(orig_left_slots)
    if orig_right_slots:
        portal.right_slots = tuple(orig_right_slots)


    # remove ucdploneskin configlet

    portal_conf=getToolByName(portal,'portal_controlpanel')
    portal_conf.unregisterConfiglet('UCDPloneSkin')

def getPropery(pp, ps, id, default=[]):
    res = default
    if ps in pp.objectIds() and pp[ps].hasProperty(id):
        res = pp[ps].getProperty(id, default)
    return res
