#!/usr/bin/python
import ConfigParser
import io
import random
import matplotlib.pyplot as plt

configfile="sim59.conf"

#Pull the Configuration in
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read(configfile)

#Set the global values
piAttackTimer=config.getint('global', 'piAttackTimer')
equal_chance_hit=config.getint('global', 'equal_chance_hit')
regentime=config.getint('global','regentime')
maxwins=config.getint('global','maxwins')
minhits=config.getint('global','minhits')
debug=config.getint('global','debug')
runlabel=config.get('global','runlabel')

#Set Player A values
paMaxHitpoints=config.getint('playera', 'piMaxHitpoints')
paResists=config.getint('playera', 'piResists')
paDamageReduce=config.getint('playera', 'piDamageReduce')
paResists=config.getint('playera', 'piResists')
paActround=config.getint('playera', 'actround')
paMindam=config.getint('playera', 'mindam')
paMaxdam=config.getint('playera', 'maxdam')
paOffense=config.getint('playera','offense')
paDefense=config.getint('playera','defensebonus')
paSpell=config.getint('playera','aspell')
paAgility=config.getint('playera','piAgility')
paDodge=config.getint('playera','piDodge')
paBlock=config.getint('playera','piBlock')
paParry=config.getint('playera','piParry')


#Set Player B values
pbSimulatorRange=config.getint('playerb','piSimulatorRange')
pbMaxHitpoints=config.getint('playerb', 'piMaxHitpoints')
pbResists=config.getint('playerb', 'piResists')
pbDamageReduce=config.getint('playerb', 'piDamageReduce')
pbResists=config.getint('playerb', 'piResists')
pbActround=config.getint('playerb', 'actround')
pbMindam=config.getint('playerb', 'mindam')
pbMaxdam=config.getint('playerb', 'maxdam')
pbOffense=config.getint('playerb','offense')
pbDefense=config.getint('playerb','defensebonus')
pbSpell=config.getint('playerb','aspell')
pbAgility=config.getint('playerb','piAgility')
pbDodge=config.getint('playerb','piDodge')
pbBlock=config.getint('playerb','piBlock')
pbParry=config.getint('playerb','piParry')

pbTopHitpointsConf=pbMaxHitpoints

def checkhit(Offense, Defense):
	pachancetohit=(Offense * 55) / Defense
	if pachancetohit < 15:
		pachancetohit = 15
	elif pachancetohit > 95:
		pachancetohit = 95

	if pachancetohit >=random.randint(1,100):
		return 1
	else:
		return 0

def checkdamage(Mindam,Maxdam,aspell,damagereduce,maxhps):
	if aspell == 0:
		damcheck=random.randint(Mindam,Maxdam)-random.randint(damagereduce/3,damagereduce)
		if damcheck<=(maxhps/minhits): 
			return damcheck
		else: return (maxhps/minhits)
	if aspell == 1:
		damcheck=random.randint(Mindam,Maxdam)
		if damcheck<=(maxhps/minhits):
			return damcheck
		else: return (maxhps/minhits)
	if aspell == 2:
		damagereduce = damagereduce * 2 / 3
		damcheck=random.randint(Mindam,Maxdam)-random.randint(damagereduce/3,damagereduce)
		if damcheck<=(maxhps/minhits):
			return damcheck
		else: return (maxhps/minhits)

i=1
paGainRound=paMaxHitpoints/regentime
pbGainRound=pbMaxHitpoints/regentime
awins=0
bwins=0
roundcount=0
paTopHitpoints=paMaxHitpoints
pbTopHitpoints=pbMaxHitpoints
paDefense=(paAgility*4)+(paDodge*3)+(paParry*2)+(paBlock)+(paMaxHitpoints*3/2)
pbDefense=(pbAgility*4)+(pbDodge*3)+(pbParry*2)+(pbBlock)+(pbMaxHitpoints*3/2)
if paDefense>=1000: paDefense=1000
if pbDefense>=1000: pbDefense=1000

def havearound(roundcount):
	global pbMaxHitpoints
	global paMaxHitpoints
	global debug

	if roundcount >=paActround:
		pahitbit=checkhit(paOffense,pbDefense)
		if pahitbit==1:
			damagedone=checkdamage(paMindam,paMaxdam,paSpell,pbDamageReduce,pbTopHitpoints)
			if debug==1: print "Player _A_ hits Player _B_ (", damagedone,")"
			pbMaxHitpoints-=damagedone
		else: 
			if debug==1: print "Player _A_ misses Player _B_"

	if pbMaxHitpoints <=0: 
		if debug==1: print "player B died"
		return 1

	if roundcount >=pbActround:
		pbhitbit=checkhit(pbOffense,paDefense)
		if pbhitbit==1:
			damagedone=checkdamage(pbMindam,pbMaxdam,pbSpell,paDamageReduce,paTopHitpoints)
			paMaxHitpoints-=damagedone
			if debug==1: print "Player _B_ hits Player _A_ (", damagedone,")"
		else: 
			if debug==1: print "Player _B_ misses Player _A_"

	if paMaxHitpoints <=0:
		if debug==1: print "player A died"
		return 0
	
	if (paGainRound*i) % 1 ==0:  
		paMaxHitpoints+=1
	if (pbGainRound*i) % 1 ==0:  
		pbMaxHitpoints+=1

	return 2
#A Bounds Checking
myAwins=[]
myBwins=[]
myAhps=[]
a=0
while(a<=pbSimulatorRange):
	pbTopHitpoints=pbTopHitpointsConf+a 
	while(i):
		status=havearound(roundcount)
		if status==2:
	  	 if debug==1: print "nobody wins yet. (",roundcount,")"
	  	 roundcount+=1
		elif status==0:
	  	 paMaxHitpoints=paTopHitpoints
	  	 pbMaxHitpoints=pbTopHitpoints
	  	 bwins=bwins+1
	  	 roundcount=0
		elif status==1:	
	 	 paMaxHitpoints=paTopHitpoints
	 	 pbMaxHitpoints=pbTopHitpoints
	 	 awins=awins+1
	 	 roundcount=0
		if awins >=maxwins:
	 	 break
		if bwins >=maxwins:
		 break
	a+=1
	myAwins.append([100*awins/(awins+bwins)])
	myBwins.append([100*bwins/(awins+bwins)])
	myAhps.append([pbTopHitpoints])
	awins=0
	bwins=0
runlabelsave=runlabel+".png"
plt.plot(myAhps,myBwins)
plt.ylabel('Player B Win Chance (%)')
plt.xlabel('Player B Hitpoints')
plt.suptitle(runlabel)
plt.savefig(runlabelsave)
