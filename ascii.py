import time,sys
if sys.argv[4]=='0':
	z=open('l','r').read()
else:
	z=open('/tmp/l','r').read()
if sys.argv[3]=='0' and ord(z[int(sys.argv[1])])<=int(sys.argv[2]):
	time.sleep(int(sys.argv[5]))
if sys.argv[3]=='1' and ord(z[int(sys.argv[1])])==int(sys.argv[2]):
	time.sleep(int(sys.argv[5]))
