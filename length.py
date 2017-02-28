import time,sys
if sys.argv[3]=='0':
	z=open('l','r').read()
else:
	z=open('/tmp/l','r').read()
if sys.argv[2]=='0' and len(z)<=int(sys.argv[1]):
	time.sleep(int(sys.argv[4]))
if sys.argv[2]=='1' and len(z)==int(sys.argv[1]):
	time.sleep(int(sys.argv[4]))
