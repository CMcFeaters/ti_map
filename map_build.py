'''
reads a txt file that contains the TI slices in csv
identifies slices and outputs
allows re-rack of galaxy based on new slice order
produces string for re-use
'use: ./map_build <./map_file_name> <slice order>
where slice order is a string of numbers with a length of the number of players, 
e.g.: 53241 or 634215
'''

import sys
import numpy as np

def create_map_array(mapname):
	'''
	Creates the mape in a 6x6 array of slices, 18 (mecatol) isn't listed and is "assumed" to be in the middel
	returns a 6x6 np array of strings
	'''
	#build the blank slice/map
	slice_arr=np.array([['ybd','tbd','tbd','tbd','tbd','tbd'],
	['ybd','tbd','tbd','tbd','tbd','tbd'],
	['ybd','tbd','tbd','tbd','tbd','tbd'],
	['ybd','tbd','tbd','tbd','tbd','tbd'],
	['ybd','tbd','tbd','tbd','tbd','tbd'],
	['ybd','tbd','tbd','tbd','tbd','tbd']])
	
	#open the map list
	f=open(mapname,'r')
	map_list=np.array(f.read().split(","))
	
	#if the entry contains mec, remove
	if (map_list[0]=='18'):
		map_list=map_list[1:37]
		print(map_list)
	#icreate slices]
	for i in range (0,6):
		if i==0:
			x=35
		else:
			x=3*i+17
		slice_arr[i]=[map_list[i],
		map_list[2*i+6],
		map_list[2*i+7],
		map_list[x],
		map_list[3*i+18],
		map_list[3*i+19]]
	
	print(slice_arr)
	
	return slice_arr
	
def create_map_string(slice_arr):
	'''
	Given a map array (6x6 of strings) creates an output string to be used on the ti4 map generator
	returns a useable URL
	'''
	preamble="https://keeganw.github.io/ti4/?settings=T51104979FFF&tiles=18,"
	tile_string=""
	t_arr=np.array(['tbd','tbd','tbd','tbd','tbd','tbd',
	'tbd','tbd','tbd','tbd','tbd','tbd',
	'tbd','tbd','tbd','tbd','tbd','tbd',
	'tbd','tbd','tbd','tbd','tbd','tbd',
	'tbd','tbd','tbd','tbd','tbd','tbd',
	'tbd','tbd','tbd','tbd','tbd','tbd'])
	
	for ring in range(0,3):
		for i in range(0,6):
			if ring==0: #1 from each
				t_arr[i]=slice_arr[i][0]
			if ring==1: #2 from each
				t_arr[6+(i*2)]=slice_arr[i][1]
				t_arr[6+(i*2)+1]=slice_arr[i][2]
			if ring==2: #3 from each
				t_arr[18+(i*3)]=slice_arr[i][4]
				t_arr[18+(i*3)+1]=slice_arr[i][5]
				#print((i+1)%6)
				#print(slice_arr[(i+1)%6][3])
				t_arr[18+(i*3)+2]=slice_arr[(i+1)%6][3]
		
	tiles=""
	for tile in t_arr:
		tiles+=tile+','
	#tiles.replace("'","")
	addr=preamble+tiles
	#return t_arr
	addr=addr.strip(',')
	#print (addr)
	return addr

def slice_arrange(slice_arr,n_players,slice_order):
	'''
	slice_arr is the nparray slice array genearted above
	n_players is 5 or 6 players.  if 6, just reorg slices, if 5, you have to
	do something special to build the map
	slice_order is an nparray 1x6 array of the slice order e.g. [5,3,4,2,1,6]
	'''
	print(slice_order)
	if n_players==6:
		new_arr=np.array([slice_arr[slice_order[0]-1],
		slice_arr[slice_order[1]-1],
		slice_arr[slice_order[2]-1],
		slice_arr[slice_order[3]-1],
		slice_arr[slice_order[4]-1],
		slice_arr[slice_order[5]-1]])
	else:
		'''
		slice 4 will be trouble
		tile [3][1] needs to swap with tile [2][2] for teh switch
		then post switch, they swap back
		'''
		#swap tiles
		temp=slice_arr[3][1]
		slice_arr[3][1]=slice_arr[2][2]
		slice_arr[2][2]=temp
		
		#this stupid clunky switching so we don't fuck with the hyperlane slice which is always "player 4"
		for i in range(0,5):
			if slice_order[i]==5:
				slice_order[i]=6
			elif slice_order[i]==4:
				slice_order[i]=5
		#re-arrange
		new_arr=np.array([slice_arr[slice_order[0]-1],
		slice_arr[slice_order[1]-1],
		slice_arr[slice_order[2]-1],
		slice_arr[3],
		slice_arr[slice_order[3]-1],
		slice_arr[slice_order[4]-1]])
		
		#swap back
		new_arr[3][1]=new_arr[2][2]
		new_arr[2][2]='88A'
	
	return new_arr

def arr_test(t_arr,mapname):
	f=open(mapname,'r')
	map_list=np.array(f.read().split(","))
	#mec removals
	if (map_list[0]=='18'):
		map_list=map_list[1:37]
		print(map_list)
		
	print("testing...")
	print(t_arr)
	print(map_list)
	if np.array_equal(t_arr,map_list):
		print("success")
	else:
		print("fail")

if __name__=="__main__":
	map=create_map_array(sys.argv[1])
	order=[int(ch) for ch in sys.argv[2]]
	addr=create_map_string(slice_arrange(map,len(order),order))
	#arr_test(t_arr,sys.argv[1])
	print(addr)
	