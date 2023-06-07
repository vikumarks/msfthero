import importlib
import json
import os
import sys
from pprint import pprint as pp

import pytest
from ixload import IxLoadTestSettings as TestSettings
from ixload import IxLoadUtils as IxLoadUtils
from ixload import IxRestUtils as IxRestUtils

targets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "targets"))
sys.path.insert(0, targets_dir)


@pytest.fixture(scope="session")
def tbinfo(request):
    """Create and return testbed information"""
    from credentials import CREDENTIALS as CR
    from testbed import TESTBED as TB
    TB["CR"] = CR
    return TB

@pytest.fixture
def create_hero_config(tbinfo):
    hero_config_dict = {}
    ixload_settings = {}

    tb_ixn = tbinfo
    hero_config_dict['ixn'] = tb_ixn

    tb = tbinfo['stateful'][0]
    tg = {
        'server': tb['server'],
        'tgen':  tb['tgen'],
    }

    # Helper Functions
    def create_test_settings():
        # TEST CONFIG
        test_settings = TestSettings.IxLoadTestSettings()
        test_settings.gatewayServer = tbinfo['stateful'][0]['server'][0]['addr']
        test_settings.gatewayPort = "8080"
        test_settings.httpRedirect = True
        test_settings.apiVersion = "v0"
        #test_settings.ixLoadVersion = "9.20.115.79"
        test_settings.ixLoadVersion = "9.30.0.331"

        client_side = tg['tgen'][0]['interfaces'][::2]
        server_side = tg['tgen'][0]['interfaces'][1::2]
        no_of_cards = len(client_side)

        if no_of_cards == 4:
            test_settings.portListPerCommunity = {
                # format: { community name : [ port list ] }
                "Traffic1@Network1": [(1, client_side[0][1], client_side[0][2]),
                                      (1, client_side[1][1], client_side[1][2]),
                                      (1, client_side[2][1], client_side[2][2]),
                                      (1, client_side[3][1], client_side[3][2]),
                                      ],
                "Traffic2@Network2": [(1, server_side[0][1], server_side[0][2]),
                                      (1, server_side[1][1], server_side[1][2]),
                                      (1, server_side[2][1], server_side[2][2]),
                                      (1, server_side[3][1], server_side[3][2]),
                                      ]
            }
        elif no_of_cards == 8:
            test_settings.portListPerCommunity = {
                # format: { community name : [ port list ] }
                "Traffic1@Network1": [(1, client_side[0][1], client_side[0][2]),
                                      (1, client_side[1][1], client_side[1][2]),
                                      (1, client_side[2][1], client_side[2][2]),
                                      (1, client_side[3][1], client_side[3][2]),
                                      (1, client_side[4][1], client_side[4][2]),
                                      (1, client_side[5][1], client_side[5][2]),
                                      (1, client_side[6][1], client_side[6][2]),
                                      (1, client_side[7][1], client_side[7][2]),
                                      ],
                "Traffic2@Network2": [(1, server_side[0][1], server_side[0][2]),
                                      (1, server_side[1][1], server_side[1][2]),
                                      (1, server_side[2][1], server_side[2][2]),
                                      (1, server_side[3][1], server_side[3][2]),
                                      (1, server_side[4][1], server_side[4][2]),
                                      (1, server_side[5][1], server_side[5][2]),
                                      (1, server_side[6][1], server_side[6][2]),
                                      (1, server_side[7][1], server_side[7][2]),
                                      ]
            }

        chassisList = tg['tgen'][0]['interfaces'][0][0]
        test_settings.chassisList = [chassisList]

        return test_settings, no_of_cards

    def create_session(test_settings):
        connection = IxRestUtils.getConnection(
            test_settings.gatewayServer,
            test_settings.gatewayPort,
            httpRedirect=test_settings.httpRedirect,
            version=test_settings.apiVersion
        )

        return connection

    test_settings, no_of_cards = create_test_settings()
    connection = create_session(test_settings)
    connection.setApiKey(test_settings.apiKey)

    ixload_settings['connection'] = connection
    ixload_settings['test_settings'] = test_settings

    hero_config_dict['ixl'] = ixload_settings
    hero_config_dict['num_of_cards'] = no_of_cards

    yield hero_config_dict
