# msfthero
Hero Test Keysight Traffic Config's
<Contents>

- [msfthero](#msfthero)
  - [Use Cases](#use-cases)
  - [Command-line](#command-line)
- [Instructions](#instructions)
# msfthero

`msfthero` is set of python script to genrate Keysight Traffic config for Hero Test. Its purpose is to generate Keysight traffic stateless and state-full traffic .

## Command-line
`python msfthero\kstraffichero_uhd_udp_bg_traffic_config_generator.py` can be used to generate UDP background traffic for MSFT Hero Test. 

`stateful traffic gen` requires pytest.  To run change directory to stateful_traffic_gen and from there: 
<br> pytest -s hero_scale/test_hero.py


# Instructions
### stateful traffic gen<br>
<ol>
<li>Config is setup to split traffic between TCP CPS and BG config types.</li>
<ol>
<li>To change go to hero_helper/hero_helper.py
line 27 and change 
 <br> 'split_networks': True, <br> to
<br>  'split_networks': False,</li>
<li> this will place all of the stateful network and buid into one test config.  Otherwise CPS and BG will be split 
and saved separately.</li>
</ol>
<li>In testbed.py change to use address of client system:  'server': [{'addr': '10.1.1.1', 'rest': 8080}],</li>
<li>Change interface address to use chassis cards: 'interfaces': [ ['10.1.1.10', 1, 1], ['10.1.1.10', 1, 2],
<ol>card address, slot#, port#</ol></li>
<li>Change the save rxf path inside hero_helper/hero_helper.py line 21
<ol>change to desired location: save_rxf_path = "C:\\automation\\"</ol></li>
</ol>