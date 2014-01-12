import cbpos
from cbpos.modules import BaseModuleMetadata

class ModuleMetadata(BaseModuleMetadata):
    base_name = 'currency'
    version = '0.1.0'
    display_name = 'Multiple Currencies Module'
    dependencies = (
        ('base', '0.1'),
    )
    config_defaults = tuple()
