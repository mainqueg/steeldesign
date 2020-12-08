'''Example 4.5 C-wlps neutral axis. 

Cold-Formed steel design - Chen, Helen. 

import importlib
importlib.reload(sd)

'''
import steeldesign as sd
from steeldesign.modules.functions import adjustNeutralAxis

p1 = sd.c_w_lps_profile(H= 10.0, B= 3.5, D=0.72, t= 0.075, r_out= (0.075+3/32) )
p1.calculate()

s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')

p1_half = sd.c_w_lps_profile_half(H= 10.0, B= 3.5, D=0.72, t= 0.075, r_out= (0.075+3/32) )
p1_half.calculate()



adjustNeutralAxis(p1.Ix, p1.A, )