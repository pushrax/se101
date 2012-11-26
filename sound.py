# Sound Module

from myro import *

music = {
	'demo1':
	[
	['E',.5],
	['E',.5],
	['F',.5],
	['G',.5],
	['G',.5],
	['F',.5],
	['E',.5],
	['D',.5],
	['C',.5],
	['C',.5],
	['D',.5],
	['E',.5],
	['E',1],
	['D',.25],
	['D',.25],
	],

	'ffwin':
	[
	['A1',.33],
	['A1',.33],
	['A1',.33],
	['A1',1],
	['F',1],
	['G',1],
	['A1',1],
	['G',.33],
	['A1',1.5],
	]

}

def __init__():
	pass

nodeMap = {
	'A':440,
	'B':493.88,
	'C':523.25,
	'C#':554.37,
	'D':587.33,
	'D#':622.25,
	'E':659.26,
	'F':698.46,
	'F#':739.99,
	'G':783.99,
	'G#':830.61,
}

def playNode(node,time):
	d = node[-1]
	multiplier = 2
	try:
		multiplier *= 2**int(d)
		node = node[:-1]
	except:pass
	beep(time/3.0,nodeMap[node]*multiplier)

def playMusic(m):
	for a,b in music[m]:
		playNode(a,b)

if __name__=='__main__':
	init ('/dev/tty.IPRE6-197927-DevB')

	playMusic('demo1')
	playMusic('ffwin')