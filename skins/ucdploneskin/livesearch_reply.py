## Script (Python) "livescript_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=q,limit=10
##title=Determine whether to show an id in an edit form

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.PythonScripts.standard import url_quote

ploneUtils = getToolByName(context, 'plone_utils')
pretty_title_or_id = ploneUtils.pretty_title_or_id

portalProperties = getToolByName(context, 'portal_properties')
siteProperties = getattr(portalProperties, 'site_properties', None)
useViewAction = []
if siteProperties is not None:
    useViewAction = siteProperties.getProperty('typesUseViewActionInListings', [])

# SIMPLE CONFIGURATION
USE_ICON = True
USE_RANKING = False
MAX_TITLE = 29
MAX_DESCRIPTION = 93

# generate a result set for the query
catalog = context.portal_catalog

friendly_types = ploneUtils.getUserFriendlyTypes()

def quotestring(s):
    return '"%s"' % s

def quote_bad_chars(s):
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, quotestring(char))
    return s

# for now we just do a full search to prove a point, this is not the
# way to do this in the future, we'd use a in-memory probability based
# result set.
# convert queries to zctextindex

# XXX really if it contains + * ? or -
# it will not be right since the catalog ignores all non-word
# characters equally like
# so we don't even attept to make that right.
# But we strip these and these so that the catalog does
# not interpret them as metachars
##q = re.compile(r'[\*\?\-\+]+').sub(' ', q)
for char in '?-+*':
    q = q.replace(char, ' ')
r=q.split()
r = " AND ".join(r)
r = quote_bad_chars(r)+'*'
searchterms = url_quote(r.replace(' ','+'))

results = catalog(SearchableText=r, portal_type=friendly_types)

RESPONSE = context.REQUEST.RESPONSE
RESPONSE.setHeader('Content-Type', 'text/xml;charset=%s' % context.plone_utils.getSiteEncoding())

# replace named entities with their numbered counterparts, in the xml the named ones are not correct
#   &darr;      --> &#8595;
#   &hellip;    --> &#8230;
legend_livesearch = _('legend_livesearch', default='LiveSearch &#8595;')
label_no_results_found = _('label_no_results_found', default='No matching results found.')
label_advanced_search = _('label_advanced_search', default='Advanced Search&#8230;')
label_show_all = _('label_show_all', default='Show all&#8230;')

ts = getToolByName(context, 'translation_service')

if not results:
    print '''<fieldset class="livesearchContainer">'''
    print '''<legend id="livesearchLegend">%s</legend>''' % ts.translate(legend_livesearch)
    print '''<div class="LSIEFix">'''
    print '''<div id="LSNothingFound">%s</div>''' % ts.translate(label_no_results_found)
    print '''<div class="LSRow">'''
    print '<a href="search_form" style="font-weight:normal">%s</a>' % ts.translate(label_advanced_search)
    print '''</div>'''
    print '''</div>'''
    print '''</fieldset>'''

else:
    print '''<fieldset class="livesearchContainer">'''
    print '''<legend id="livesearchLegend">%s</legend>''' % ts.translate(legend_livesearch)
    print '''<div class="LSIEFix">'''
    print '''<ul class="LSTable">'''
    for result in results[:limit]:

        itemUrl = result.getURL()
        if result.portal_type in useViewAction:
            itemUrl += '/view'

        print '''<li class="LSRow">''',
        print '''<img src="%s"/>''' % result.getIcon,
        full_title = pretty_title_or_id(result)
        if len(full_title) >= MAX_TITLE:
            display_title = ''.join((full_title[:MAX_TITLE],'...'))
        else:
            display_title = full_title
        print '''<a href="%s" title="%s">%s</a>''' % (itemUrl, full_title, display_title)
        print '''<span class="discreet">[%s%%]</span>''' % result.data_record_normalized_score_
        display_description = result.Description
        if len(display_description) >= MAX_DESCRIPTION:
            display_description = ''.join((display_description[:MAX_DESCRIPTION],'...'))
        print '''<div class="discreet" style="margin-left: 2.5em;">%s</div>''' % (display_description)
        print '''</li>'''
        full_title, display_title, display_description = None, None, None

    print '''<li class="LSRow">'''
    print '<a href="%s/search_form" style="font-weight:normal">%s</a>' % (container.portal_url(), ts.translate(label_advanced_search))
    print '''</li>'''

    if len(results)>limit:
        # add a more... row
        print '''<li class="LSRow">'''
        print '<a href="%s" style="font-weight:normal">%s</a>' % (container.portal_url() + '/search?SearchableText=' + searchterms, ts.translate(label_show_all))
        print '''</li>'''
    print '''</ul>'''
    print '''</div>'''
    print '''</fieldset>'''

return printed

