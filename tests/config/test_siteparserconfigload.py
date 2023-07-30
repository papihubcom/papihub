import os

from papihub.config.siteparserconfigloader import SiteParserConfigLoader


def test_load_parser():
    configs = SiteParserConfigLoader(os.path.join(os.path.dirname(os.path.realpath('.')), 'conf', 'parser')).load()
    assert len(configs) > 0
    return configs
