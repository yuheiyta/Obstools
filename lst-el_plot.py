import astropy.units as u
from astropy.time import Time,TimeDelta
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

#########################
# Observatories
hitachi = EarthLocation(lat=(36 + 41/60 + 40/3600)*u.deg, lon=(140 + 41/60 + 44/3600)*u.deg, height=60*u.m)
mizusawa = EarthLocation(lon=(141 + 7./60. + 57.199/3600.)*u.deg,lat = (39 + 8./60. + 00.726/3600.)*u.deg,height=75.7*u.m)
iriki = EarthLocation(lon=(130 + 26/60 + 23.593/3600)*u.deg,lat = (31 + 44/60. + 52.437/3600.)*u.deg,height=541.6*u.m)
yamaguchi = EarthLocation(lon=(131 + 33/60 + 26/3600)*u.deg, lat = (34 + 12/60 + 58/3600)*u.deg,height = 144*u.m)

gmrt= EarthLocation(lon=(74. + 3./60. + 0./3600.)*u.deg,lat=(19. + 5./60. + 48./3600.)*u.deg,height=650.0*u.m)
meerkat = EarthLocation(lon=(21 + 26/60 + 35/3600)*u.deg, lat=-1.*(30 + (42/60) + (48/3600))*u.deg,height=1052*u.m)

#########################
# The part you have to change
location = meerkat # Need to be selected from the one in the above.
#objnames = ["Sgr A*"]
#coords = ["17h45m40.03599s -29d00m28.1699s"]
objnames = ["HD 35502"]
coords = ["05h25m01.2041767248s -02d48m55.690705872s"]
ellist =[15.] # Elevation list (degree), for illustrating elevation limit
#########################

c = SkyCoord(coords,frame="icrs")# You need to change if the coordinate is different from icrs (e.g., Galactic)

start_time = Time('2023-04-01T00:00:0.0',location=location) # not important for LST calculation
time_length = 24.
num=200
dt=time_length*3600./num

#sec, time bin
dt_time = TimeDelta(dt, format='sec')
antspeed=0.21 #deg/sec, antenna speed 
#########################
# Functions
def trans_azel(coordinate,obstime,loc):
    altaz=coordinate.transform_to(AltAz(obstime=obstime, location=loc))
    return altaz,altaz.az.deg,altaz.alt.deg

# (2) Transform time list ([yy, doy, hhmmss]) to astropy Time object
def trans_timelist(timelist):
    return Time("20"+timelist[0]+":"+timelist[1]+":"+timelist[2][0:2]+":"+timelist[2][2:4]+":"+timelist[2][4:6]+".000",format="yday")

def calc_lst(location, datetime_):
    localtime = Time(datetime_, format='datetime', location=location)
    return localtime.sidereal_time('apparent')
#########################


j=0
timelist = []

plt.rcParams['font.size'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

fig=plt.figure(figsize=(8,6))
ax=fig.add_subplot()

for index in range(len(objnames)):
    time_el = []
    obstime = start_time
    for i in range(int(time_length*60*60/dt)):
        altaz,az,el=trans_azel(c[index],obstime,location)
        time_el.append([el])
        if(j==0):
            lsttime=obstime.sidereal_time('apparent')
            timelist.append(lsttime.to_value())
        obstime = obstime+dt_time
    ax.scatter(timelist, time_el,label=objnames[index])
    j+=1
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
# ax.set_title("Start Time: "+str(start_time.utc))
#ax.set_title(objname[0])
ax.set_xlabel("Time (LST)")
ax.set_ylabel("Elevation (deg)")
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
if(len(ellist)>=1):
    for el in ellist:
        ax.axhline(y=el,color="black",ls="--")
ax.set_xlim(-0.1,24.1)
ax.set_ylim(0,)
ax.legend()
fig.tight_layout()
#plt.savefig(objnames[0]+"_elplot.jpeg")
plt.show()
