from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter


class LogoViewlet(ViewletBase):
    index = ViewPageTemplateFile('logo.pt')

    def update(self):
        super(LogoViewlet, self).update()

        self.navigation_root_url = self.portal_state.navigation_root_url()

        portal = self.portal_state.portal()
        logoName = portal.restrictedTraverse('base_properties').logoName
        self.logo_tag = portal.restrictedTraverse(logoName).tag()

        self.portal_title = self.portal_state.portal_title()

class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('path_bar.pt')

    def update(self):
        super(PathBarViewlet, self).update()

        self.navigation_root_url = self.portal_state.navigation_root_url()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()
        

class GlobalSectionsViewlet(ViewletBase):
    index = ViewPageTemplateFile('sections.pt')

    def update(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions()
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)

        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('index_html',
                                          self.context,
                                          self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']

        # support for double-row globalsections with second row specification
        # drawn from ucdploneskin_properties.secondTabRow
        ucdprops = getattr(self.context, 'ucdploneskin_properties', None)
        if ucdprops is not None:
          secondTabRow = getattr(ucdprops, 'secondTabRow', '').split(',')
          row1 = []
          row2 = []
          for tab in self.portal_tabs:
            if tab['id'] in secondTabRow:
              row2.append(tab)
            else:
              row1.append(tab)
          self.portal_tab_rows = []
          self.portal_tab_styles = ['portal-globalnav-2']
          if len(row1):
            self.portal_tab_rows.append(row1)
          if len(row2):
            self.portal_tab_rows.append(row2)
            self.portal_tab_styles = ['portal-globalnav-1','portal-globalnav-2']


