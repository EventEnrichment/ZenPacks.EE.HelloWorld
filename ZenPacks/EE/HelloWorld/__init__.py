##############################################################################
#
# GPLv2
#
# You should have received a copy of the GNU General Public License
# along with this ZenPack. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import logging
LOG = logging.getLogger('zen.ZenPacks.EE.HelloWorld')

import os
import Globals

from Products.ZenModel.Device import Device
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory
from Products.CMFCore.DirectoryView import registerDirectory
from Products.Zuul.interfaces import ICatalogTool
from Products.ZenUtils.Utils import unused, zenPath

unused(Globals)

# Test Logging
LOG.info('Hello World!\n')


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

ZENPACK_NAME = 'ZenPacks.EE.HelloWorld'

# Define new device relations.
NEW_DEVICE_RELATIONS = (
    )

NEW_COMPONENT_TYPES = (
    )

# Add new relationships to Device if they don't already exist.
for relname, modname in NEW_DEVICE_RELATIONS:
    if relname not in (x[0] for x in Device._relations):
        Device._relations += (
            (relname, ToManyCont(
                ToOne,
                '.'.join((ZENPACK_NAME, modname)),
                '%s_host' % modname)),
            )

# Useful to avoid making literal string references to module and class names
# throughout the rest of the ZenPack.
MODULE_NAME = {}
CLASS_NAME = {}

_PACK_Z_PROPS = [
    ('zEEProperty', 'Hello World', 'string'),
    ]

setzPropertyCategory('zEEProperty', 'None')

_plugins = (
    )


class ZenPack(ZenPackBase):
    packZProperties = _PACK_Z_PROPS

    def install(self, app):
        super(ZenPack, self).install(app)
        LOG.info('Adding ZenPacks.EE.HelloWorld relationships to existing devices')

        self._buildDeviceRelations()
        self.symlink_plugins()

    def symlink_plugins(self):
        libexec = os.path.join(os.environ.get('ZENHOME'), 'libexec')
        if not os.path.isdir(libexec):
            # Stack installs might not have a $ZENHOME/libexec directory.
            os.mkdir(libexec)

        for plugin in _plugins:
            LOG.info('Linking %s plugin into $ZENHOME/libexec/', plugin)
            plugin_path = zenPath('libexec', plugin)
            os.system('ln -sf "%s" "%s"' % (self.path(plugin), plugin_path))
            os.system('chmod 0755 %s' % plugin_path)

    def remove_plugin_symlinks(self):
        for plugin in _plugins:
            LOG.info('Removing %s link from $ZENHOME/libexec/', plugin)
            os.system('rm -f "%s"' % zenPath('libexec', plugin))

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            self.remove_plugin_symlinks()

            LOG.info('Removing ZenPacks.EE.HelloWorld components')
            cat = ICatalogTool(app.zport.dmd)

            # Search the catalog for components of this zenpacks type.
            if NEW_COMPONENT_TYPES:
                for brain in cat.search(types=NEW_COMPONENT_TYPES):
                    component = brain.getObject()
                    component.getPrimaryParent()._delObject(component.id)

            # Remove our Device relations additions.
            Device._relations = tuple(
                [x for x in Device._relations
                    if x[0] not in NEW_DEVICE_RELATIONS])

            LOG.info('Removing ZenPacks.EE.HelloWorld relationships from existing devices')
            self._buildDeviceRelations()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def _buildDeviceRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            d.buildRelations()
