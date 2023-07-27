#!/usr/bin/env python3
import ipaddress
import json
import macaddress
import sys

from copy import deepcopy
from munch import DefaultMunch
from datetime import datetime
from ixnetwork_restpy import SessionAssistant, BatchUpdate

sys.path.append(r"/home/mircea/dpugen/dpugen")                       #Put path to a dflt_params file from which dash or sai config was generated.
from dflt_params import dflt_params as df




p = DefaultMunch.fromDict(df)
ipa = ipaddress.ip_address
maca = macaddress.MAC

cp = {}
for ip in ['IP_STEP1','IP_STEP_ENI','IP_STEP_NSG','IP_STEP_ACL','IP_STEPE','IP_L_START','IP_R_START','PAL','PAR']:
    cp[ip] = int(ipa(df[ip]))
for mac in ['MAC_L_START','MAC_R_START','ACL_NSG_MAC_STEP','ACL_POLICY_MAC_STEP','ENI_MAC_STEP']:
    cp[mac] = int(maca(df[mac]))
cp = DefaultMunch.fromDict(cp)


TESTBED = {
    'stateless': [
        {
            'server': [{'addr': '10.36.78.203', 'rest': 11009}],                                                    #IxNetwork API Server IP and Rest Port, if IxNetwork WEB , use default port 443
            'tgen':    [
                {
                    'type': 'keysight',
                            'interfaces': [
                                            {'location':'10.36.79.165;11;1','fec':True,'an':True,'ieee':True},      #ChassisIP;cardId;PortNumber
                                            {'location':'10.36.79.165;11;2','fec':True,'an':True,'ieee':True},
                                            {'location':'10.36.79.165;11;3','fec':True,'an':True,'ieee':True},
                                            {'location':'10.36.79.165;11;4','fec':True,'an':True,'ieee':True},
                                            {'location':'10.36.79.165;11;5','fec':True,'an':True,'ieee':True},
                                            {'location':'10.36.79.165;11;6','fec':True,'an':True,'ieee':True},
                                            {'location':'10.36.79.165;11;7','fec':True,'an':True,'ieee':True},
                                            {'location':'10.36.79.165;11;8','fec':True,'an':True,'ieee':True},
                                            ],
                }]}]
       }



test_data = {
    "enis": {
        "eth": {
                    "mac": {
                                "start_value":str(maca(cp.MAC_L_START + cp.ENI_MAC_STEP)).replace('-', ':'),
                                "step_value":'00:00:00:60:00:00',
                                "increments":[(p.ENI_MAC_STEP, 3,[])],                                          # p.ACL_NSG_COUNT +-*?  insted of 3?
                                "ng_step":"00:00:01:80:00:00"
                            },
                    "vlanid":{
                                "start_value":p.ENI_START+1,
                                "step_value":4,
                                "increments":[(1, 3,[])],                                                       # p.ACL_NSG_COUNT +-*?  insted of 3?
                                "ng_step":16                                                                    # p.IP_ROUTE_DIVIDER_PER_ACL_RULE   16?
                            }
                },
        "ipv4": {
                    "ip":  {
                            "start_value":str(ipa(cp.IP_L_START + cp.IP_STEP_ENI)), 
                            "step_value":'1.0.0.0', 
                            "increments":[(p.IP_STEP_ENI, 3,[])],                                               # p.ACL_NSG_COUNT +-*?  insted of 3?
                            "ng_step":"4.0.0.0"
                            }, 
                    "gip": {
                            "start_value":str(ipa(cp.IP_R_START + cp.IP_STEP_ENI)), 
                            "step_value":'1.0.0.0', 
                            "increments":[(p.IP_STEP_ENI, 3,[])],                                               # p.ACL_NSG_COUNT +-*?  insted of 3?
                            "ng_step":"4.0.0.0"
                            }, 
                    "mac": "08:C0:EB:20:38:2C",                                                                 #DPU MAC
                    "prefix":32
                    },
        },
    "clients": {
        "eth": {
                    "mac": {
                                "start_value":str(maca(cp.MAC_R_START + cp.ENI_MAC_STEP)).replace('-', ':'),
                                "step_value":'00:00:00:60:00:00',
                                "increments":[(p.ENI_MAC_STEP, 3,[])],                                          # p.ACL_NSG_COUNT +-*?  insted of 3?
                                "ng_step":"00:00:01:80:00:00"
                            },

                    "vlanid":{
                                "start_value":p.ENI_START+p.ENI_L2R_STEP+1,
                                "step_value":4,
                                "increments":[(1, 3,[])],
                                "ng_step":16                                                                    # p.IP_ROUTE_DIVIDER_PER_ACL_RULE   16?
                            }
                },

        "ipv4": {
                    "ip":  {
                            "start_value":str(ipa(cp.IP_R_START + cp.IP_STEP_ENI)), 
                            "step_value":'1.0.0.0', 
                            "increments":[(p.IP_STEP_ENI, 3,[])],                                               # p.ACL_NSG_COUNT +-*?  insted of 3?
                            "ng_step":"4.0.0.0"
                            },
                    "gip": {
                            "start_value":str(ipa(cp.IP_L_START + cp.IP_STEP_ENI)), 
                            "step_value":'1.0.0.0', 
                            "increments":[(p.IP_STEP_ENI, 3,[])],                                               # p.ACL_NSG_COUNT +-*?  insted of 3? 
                            "ng_step":"4.0.0.0"
                            },
                    "mac": "08:C0:EB:20:38:2C",                                                                 #DPU MAC
                    "prefix":32
                    },
        "rangesa": {
                    "ip":  {
                            "start_value":str(ipa(cp.IP_R_START + cp.IP_STEP_ENI)), 
                            "step_value":"1.0.0.0",  #p.IP_STEP_ENI, 
                            "increments":[(p.IP_STEP_ENI, 3,[(p.IP_STEP_NSG,10,[])])],                          # 1-A 10 is ranges ip Step  and ACL_NSG_COUNT =3 or 5 6 or 10 in all direction
                            "ng_step":(1,"4.0.0.0")
                            },
                    "ip_address_count_4_ranges": 64000,
                    "multiplier": 10,                                                                           # 1- 10 is ranges ip Step Number should match with 1-A
                    "prefix":32,
                    'prefixaddrstep':2
                    },
        "rangesd": {
                    "ip":  {
                            "start_value":str(ipa(cp.IP_R_START + cp.IP_STEP_ENI) -1),
                            "step_value":"1.0.0.0",  #p.IP_STEP_ENI, 
                            "increments":[(p.IP_STEP_ENI, 3,[(p.IP_STEP_NSG,10,[])])],                          # 1-A 10 is ranges ip Step  and ACL_NSG_COUNT =3 or 5 6 or 10 in all direction
                            "ng_step":(1,"4.0.0.0")
                            },
                    "ip_address_count_4_ranges": 128,
                    "multiplier": 10,                                                                           # 1- 10 is ranges ip Step Number should match with 1-A
                    "prefix":32,
                    'prefixaddrstep':2
                    },

    }
}



ixnetwork=None

def hero_ixnetwork_config():
    global ixnetwork
    testbed = TESTBED
    def createTI(name, endpoints, udp_src_port=10000,udp_dst_port=10000):
        trafficItem = ixnetwork.Traffic.TrafficItem.find(Name="^%s$" % name)
        if len(trafficItem) == 0:
            trafficItem = ixnetwork.Traffic.TrafficItem.add(Name=name, TrafficType='ipv4', BiDirectional=False)  # BiDirectional=True

        udp_template = ixnetwork.Traffic.ProtocolTemplate.find(StackTypeId='^udp$')
        print ("Creating %s Traffic" % name)
        print ("*"*5,datetime.now(),"*"*5)
        print ("Creating EP for Each ENI")
        for indx,srcdst in enumerate(endpoints):
            src,dst = srcdst
            trafficItem.EndpointSet.add(Name="ENI-%s" % str(indx+1),ScalableSources=src, ScalableDestinations=dst)

        config_elements_sets = trafficItem.ConfigElement.find()
        print ("*"*5,datetime.now(),"*"*5)
        with BatchUpdate(ixnetwork):
            for ce in config_elements_sets:
                ipv4_template = ce.Stack.find(TemplateName="ipv4-template.xml")[-1]
                ce.TransmissionControl.Type = 'continuous'
                ce.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
                ce.FrameSize.FixedSize = 440
                ce.FrameRate.update(Type='percentLineRate', Rate=0.5)
                inner_udp = ce.Stack.read(ipv4_template.AppendProtocol(udp_template))
                inn_sp = inner_udp.Field.find(DisplayName='^UDP-Source-Port')
                inn_dp = inner_udp.Field.find(DisplayName='^UDP-Dest-Port')
                inn_sp.Auto = False
                inn_dp.Auto = False
                inn_sp.SingleValue = udp_src_port
                inn_dp.SingleValue = udp_dst_port


        trafficItem.Tracking.find()[0].TrackBy = ['trackingenabled0', 'sourceDestEndpointPair0','vlanVlanId0']
        trafficItem.MergeDestinations = False
        print ("*"*5,"Traffic creation finished",datetime.now(),"*"*5)
        return trafficItem


    obj_map = {}
    for k in test_data.keys():obj_map[k] = deepcopy({})
    td = deepcopy(test_data)
    print('connect to a test tool platform')
    tb=testbed['stateless'][0]

    session_assistant = SessionAssistant(IpAddress=tb['server'][0]['addr'], RestPort=tb['server'][0]['rest'], UserName='admin', Password='admin', SessionName="HeroTest", ClearConfig=True)
    ixnetwork = session_assistant.Ixnetwork
    portList = [{'xpath': '/vport[%s]' % str(indx+1), 'name': 'VTEP_0%d' % (indx+1), 'location': p['location']} for indx, p in enumerate(tb['tgen'][0]['interfaces'])]
    ixnetwork.ResourceManager.ImportConfig(json.dumps(portList), False)
    vports = list(ixnetwork.Vport.find())
    l1data = tb['tgen'][0]['interfaces']
    tmp = [{'xpath': '/vport[%d]/l1Config/%s' % (vp.InternalId, vp.Type), "ieeeL1Defaults": l1data[indx]['ieee'] } for indx, vp in enumerate(vports)]
    ixnetwork.ResourceManager.ImportConfig(json.dumps(tmp), False)
    tmp = [{'xpath': '/vport[%d]/l1Config/%s' % (vp.InternalId, vp.Type), "enableAutoNegotiation": l1data[indx]['an']} for indx, vp in enumerate(vports)]
    ixnetwork.ResourceManager.ImportConfig(json.dumps(tmp), False)
    tmp = [{'xpath': '/vport[%d]/l1Config/%s' % (vp.InternalId, vp.Type), "enableRsFec": l1data[indx]['fec'], "autoInstrumentation": "floating"} for indx, vp in enumerate(vports)]
    ixnetwork.ResourceManager.ImportConfig(json.dumps(tmp), False)

    #for ed in ["enis", "clients"]:
    for ed, val in td.items():
        # Was Using #p.ENI_COUNT*2)/len(vports) for multiplier

        obj_map[ed]["bgp"]   = ixnetwork.Topology.add(Ports=vports[:4] if ed=="enis" else vports[4:], Name="TG_%s" % ed)\
                                        .DeviceGroup.add(Name="%s" % ed.upper(), Multiplier=12)\
                                        .Ethernet.add(UseVlans=True).Ipv4.add().BgpIpv4Peer.add()

        obj_map[ed]["ipv4"]             = obj_map[ed]["bgp"].parent
        obj_map[ed]["eth"]              = obj_map[ed]["ipv4"].parent
        obj_map[ed]["bgp"].Active.Single(False)
        obj_map[ed]["ipv4"].Prefix.Single(val["ipv4"]["prefix"])


        if ed=="clients":
            ng    = ixnetwork.Topology.find().DeviceGroup.find(Name=ed.upper()).NetworkGroup.add(Name="Allow", Multiplier=val["rangesa"]["multiplier"])
            obj_map[ed]["rangesa"] = ng.Ipv4PrefixPools.add(NumberOfAddresses=val["rangesa"]["ip_address_count_4_ranges"])
            obj_map[ed]["rangesa"].PrefixLength.Single(val["rangesa"]["prefix"])
            obj_map[ed]["rangesa"].PrefixAddrStep.Single(val["rangesa"]["prefixaddrstep"])

            d_ng    = ixnetwork.Topology.find().DeviceGroup.find(Name=ed.upper()).NetworkGroup.add(Name="Deny", Multiplier=val["rangesd"]["multiplier"])
            obj_map[ed]["rangesd"] = d_ng.Ipv4PrefixPools.add(NumberOfAddresses=val["rangesd"]["ip_address_count_4_ranges"])
            obj_map[ed]["rangesd"].PrefixLength.Single(val["rangesd"]["prefix"])
            obj_map[ed]["rangesd"].PrefixAddrStep.Single(val["rangesd"]["prefixaddrstep"])

    properties = [
        ("eth", "Mac","mac", "start_value", "step_value", "increments", "ng_step"),
        ("eth", "VlanId","vlanid", "start_value", "step_value", "increments", "ng_step"),
        ("ipv4", "Address","ip", "start_value", "step_value", "increments", "ng_step"),
        ("ipv4", "GatewayIp","gip", "start_value", "step_value", "increments", "ng_step"),
        ("rangesa", "NetworkAddress","ip", "start_value", "step_value", "increments", "ng_step"),
        ("rangesd", "NetworkAddress","ip", "start_value", "step_value", "increments", "ng_step")

    ]
    print ("*"*5,"Updating custom Patterns",datetime.now(),"*"*5)

    for ed, val in td.items():
        for prop in properties:
            if prop[0] in ["rangesa", "rangesd"] and ed=="enis":break
            if prop[1]== "VlanId":
                obj = obj_map[ed][prop[0]].Vlan.find().VlanId
            else:
                obj = getattr(obj_map[ed][prop[0]],prop[1])
            tmp = val[prop[0]][prop[2]]
            obj.Custom(start_value=tmp[prop[3]], step_value=tmp[prop[4]], increments=tmp[prop[5]])
            indx,value = 0, tmp[prop[6]]
            if type(tmp[prop[6]]) is tuple:
                indx, value = tmp[prop[6]]
            
            obj.Steps[indx].Enabled = True
            obj.Steps[indx].Step = value

    print ("*"*5,"Finished Updating custom Patterns",datetime.now(),"*"*5)
    print("Create Traffic")
    eni_ips = obj_map['enis']["ipv4"]
    ng_allow = ixnetwork.Topology.find().DeviceGroup.find().NetworkGroup.find(Name="Allow").Ipv4PrefixPools.find()
    ng_deny  = ixnetwork.Topology.find().DeviceGroup.find().NetworkGroup.find(Name="Deny").Ipv4PrefixPools.find()

    endpoints_allow_outbound, endpoints_allow_inbound, endpoints_deny=[], [], []
    step_ip_a = td['clients']["rangesa"]["multiplier"]
    step_ip_d = td['clients']["rangesd"]["multiplier"]
    select_port = 0
    reset_ip_count = 0
    for eni in range(48):               # p.ENI_COUNT               Need to change when ixnwork is using 48 as 16 is used by ixload
        if eni%12==0:                   # Was using int((p.ENI_COUNT*2)/len(vports))
                select_port+=1
                reset_ip_count = 0

        endpoints_allow_outbound.append(
                            (
                            deepcopy([{"arg1": eni_ips.href,"arg2": select_port,"arg3": 1,"arg4": reset_ip_count+1,"arg5": 1  }]),
                            deepcopy([{"arg1": ng_allow.href,"arg2": select_port,"arg3": 1,"arg4": reset_ip_count*step_ip_a+1,"arg5": step_ip_a  }])
                            )
                          )
        endpoints_allow_inbound.append(
                            (
                            deepcopy([{"arg1": ng_allow.href,"arg2": select_port,"arg3": 1,"arg4": reset_ip_count*step_ip_a+1,"arg5": step_ip_a  }]),
                            deepcopy([{"arg1": eni_ips.href,"arg2": select_port,"arg3": 1,"arg4": reset_ip_count+1,"arg5": 1  }])
                            )
                          )
        endpoints_deny.append(
                            (
                            deepcopy([{"arg1": eni_ips.href,"arg2": select_port,    "arg3": 1,    "arg4": reset_ip_count+1,    "arg5": 1  }]),
                            deepcopy([{"arg1": ng_deny.href ,"arg2": select_port,    "arg3": 1,    "arg4": reset_ip_count*step_ip_d-1,    "arg5": step_ip_d  }])
                            )
                          )
        reset_ip_count+=1

    ti_allow_out = createTI("Outbound Allow - All IPs", endpoints_allow_outbound)
    ti_allow_in = createTI("Inbound Allow - All IPs", endpoints_allow_inbound, udp_src_port = 20000, udp_dst_port = 20000)
    
    #ti_deny = createTI("Deny",  endpoints_deny)

hero_ixnetwork_config()
