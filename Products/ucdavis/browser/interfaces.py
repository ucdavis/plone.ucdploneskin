from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from plonetheme.classic.browser.interfaces import IThemeSpecific as IClassicTheme

class IThemeSpecific(IClassicTheme):
    """theme-specific layer"""

class IPortalBarHeader(IViewletManager):
    """Marker interface for view manager above content
       and right column.
    """