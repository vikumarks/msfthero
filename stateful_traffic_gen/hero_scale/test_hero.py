import inspect
import json
import sys
import time
from copy import deepcopy

import ipaddress
import macaddress
import pytest
import requests

from hero_helper.hero_helper import HeroHelper
from ixload import IxLoadUtils as IxLoadUtils
from ixnetwork_restpy import SessionAssistant
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant
from tabulate import tabulate
from testdata_hero import testdata,ip_type
from datetime import datetime
from threading import Thread
from future.utils import iteritems
from variables import *

data = []
final_result_data=[]
setup_information=None
ixnetwork=None
config_elements_sets=[]
val_map={}
tiNo = 16
captions = ["Test","PPS", "Tx Frames", "Rx Frames", "Frames Delta", "Loss %","PossibleBoundary"]

class Test_Dpu:

    def test_cps_001(self, create_hero_config):
        """
            Description: Verify ip address can be configured in SVI.
            Topo: DUT02 ============ DUT01
            Dev. status: DONE
        """
        stats_dict = {}
        location = inspect.getfile(inspect.currentframe())

        tcp_cps_settings = deepcopy(create_hero_config['ixl'])
        tcp_bg_settings = deepcopy(create_hero_config['ixl'])

        hero_tcp_cps = HeroHelper(tcp_cps_settings, test_config_type='cps', id=1)
        hero_tcp_bg = HeroHelper(tcp_bg_settings, test_config_type='tcp_bg', id=2)

        ## RUN
        #hero_tcp_cps.run2(hero_tcp_cps)
        #hero_tcp_cps.run2(hero_tcp_bg)

