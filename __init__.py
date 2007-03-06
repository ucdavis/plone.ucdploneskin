from Products.PythonScripts.Utility import allow_module
allow_module('types')

from Products.CMFCore.DirectoryView import registerDirectory
from config import SKIN_GLOBALS

registerDirectory('skins', SKIN_GLOBALS)
