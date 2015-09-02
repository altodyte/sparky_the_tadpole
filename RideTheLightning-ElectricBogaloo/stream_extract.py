import sys

for line in sys.stdin:
	try:
		if line[0]=='.':
			msg = line.split(',')
			print "x: " + msg[6]
			print "y: " + msg[7]
			print "z: " + msg[8]
	except:
		continue
