#&nbsp;TBDEx
Time Based Data Exfiltration Tool<br />

usage:&nbsp;timebased.py&nbsp;[-h]&nbsp;[-url&nbsp;URL]&nbsp;[-post&nbsp;POST]&nbsp;[-threads&nbsp;THREADS]<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-cookie&nbsp;COOKIE&nbsp;FILE]&nbsp;[-file&nbsp;HEADER&nbsp;FILE]&nbsp;[-retry&nbsp;RETRY]<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-timeout&nbsp;TIMEOUT]&nbsp;[-time&nbsp;AVGTIME]&nbsp;[-os&nbsp;OS]<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-payload&nbsp;limit&nbsp;LIMIT]&nbsp;[-force&nbsp;write]&nbsp;[-tmp]<br />

Time Based Data Exfiltration Tool<br />

optional&nbsp;arguments:<br />
&nbsp;&nbsp;-h,&nbsp;--help&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show&nbsp;this&nbsp;help&nbsp;message&nbsp;and&nbsp;exit<br />
&nbsp;&nbsp;-url&nbsp;URL&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;URL<br />
&nbsp;&nbsp;-post&nbsp;POST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;POST<br />
&nbsp;&nbsp;-threads&nbsp;THREADS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Threads<br />
&nbsp;&nbsp;-cookie&nbsp;COOKIE&nbsp;FILE&nbsp;&nbsp;&nbsp;Cookie&nbsp;File<br />
&nbsp;&nbsp;-file&nbsp;HEADER&nbsp;FILE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Burp&nbsp;request&nbsp;file<br />
&nbsp;&nbsp;-retry&nbsp;RETRY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Retry&nbsp;request&nbsp;N&nbsp;times&nbsp;in&nbsp;case&nbsp;of&nbsp;network&nbsp;errors<br />
&nbsp;&nbsp;-timeout&nbsp;TIMEOUT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;General&nbsp;timeout&nbsp;request<br />
&nbsp;&nbsp;-time&nbsp;AVGTIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Added&nbsp;timeout&nbsp;to&nbsp;request<br />
&nbsp;&nbsp;-os&nbsp;OS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;OS&nbsp;type&nbsp;(U&nbsp;unix/linux&nbsp;,&nbsp;W&nbsp;windows)<br />
&nbsp;&nbsp;-payload&nbsp;limit&nbsp;LIMIT&nbsp;&nbsp;If&nbsp;there&nbsp;is&nbsp;any&nbsp;command&nbsp;length&nbsp;limitation<br />
&nbsp;&nbsp;-force&nbsp;write&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Force&nbsp;writing&nbsp;auxiliary&nbsp;files<br />
&nbsp;&nbsp;-tmp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Writing&nbsp;auxiliary&nbsp;files&nbsp;in&nbsp;tmp&nbsp;folder<br />
```python
For this to work pycurl must be installed:
pip install pycurl
or
apt-get install pycurl
or
apt-get install python-pycurl
```
