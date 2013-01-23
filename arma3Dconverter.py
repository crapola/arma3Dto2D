#-------------------------------------------------------------------------------
# Name:			arma3Dconverter
# Purpose:		Tool for Arma 2 mission editing.
#				Converts empty vehicles.objects to 2D editor format. Vehicles in
#				the air get a setpos in their init.
# Usage:		Copy your mission.sqf from 3D editor where the script is, then
#				run it. It will generate a list of items to output.txt that you
#				can	paste in your .sqm under Vehicles. Pay attention to proper
#				item count and numbering etc.
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import re

RX_FLOAT=r"[-+]?(?:(?: \d* \. \d+ )|(?: \d+ \.? ))(?: [Ee] [+-]? \d+ ) ?"

Z_THRESOLD=0.1 # Below this, the object is on the ground
SETTING_DOROUND=True
STARTING_ITEM_NUMBER=0

def roundo(value):
	"""Nearest multiple of 1/16"""
	if SETTING_DOROUND==False: return float(value)
	return (1/16)*round(float(value)/(1/16))

class A2Object:

	item_output_format="""		class Item{}
		{{
			position[]={{{},{},{}}};
			azimut={};
			special="NONE";
			id={};
			side="EMPTY";
			vehicle="{}";
		}};
"""

	item_output_format_with_init="""		class Item{}
		{{
			position[]={{{},{},{}}};
			azimut={};
			special="NONE";
			id={};
			side="EMPTY";
			vehicle="{}";
			init="this setPos [{},{},{}]";
		}};
"""
	def __init__(self):
		self.pos=[0,0,0]
		self.dir=999
		self.name="INVALIDNAME"
	def print(self):
		print(self.name,"POSITION:",self.pos,"DIRECTION:",self.dir)
	def sqm_item_string(self,item_number=0):
		"""Item section"""
		if self.pos[2]==0:
			r=self.item_output_format.format(item_number,
			self.pos[0],
			self.pos[2],
			self.pos[1],
			self.dir,
			1000+item_number,
			self.name)
		else:
			r=self.item_output_format_with_init.format(item_number,
										self.pos[0],
										self.pos[2],
										self.pos[1],
										self.dir,
										1000+item_number,
										self.name,
                                        self.pos[0],
										self.pos[1],
										self.pos[2])
		return r

RX_OBJ=(
'createVehicle \[\"(?P<name>[^"]+)' # Name
'.+?\[(?P<pos>.+?)\], ' # Position
'.+?(?:\}|setDir (?P<dir>[-]?\d*.\d*))' # Direction
)

def main():
	rx=re.compile(RX_OBJ,re.S)
	file=open('mission.sqf','r')
	text=file.read()
	sections=rx.findall(text)
	file.close()

	rx = re.compile(RX_FLOAT,re.VERBOSE)
	objects_list=[]
	for z in sections:
		o=A2Object()

		o.name=z[0]
		postxt=rx.findall(z[1])
		o.pos[0]=roundo(postxt[0])
		o.pos[1]=roundo(postxt[1])
		if len(postxt)>2:
			o.pos[2]=roundo(postxt[2])
			if o.pos[2]<Z_THRESOLD: o.pos[2]=0

		if z[2]!='':
			o.dir=roundo(z[2])
		else:
			o.dir=0

		objects_list.append(o)

	print (len(sections),"items.")

	output_text=''
	for i,o in enumerate(objects_list):
		output_text+=o.sqm_item_string(i+STARTING_ITEM_NUMBER)

	file=open('output.txt','w')
	file.write(output_text)
	file.close()
	print('Done.')

if __name__ == '__main__':
	main()