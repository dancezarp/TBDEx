# TBDEx
Time Based Data Exfiltration Tool

usage: timebased.py [-h] [-url URL] [-post POST] [-threads THREADS]
                    [-cookie COOKIE_FILE] [-file HEADER_FILE] [-retry RETRY]
                    [-timeout TIMEOUT] [-time AVGTIME] [-os OS]
                    [-payload_limit LIMIT] [-force_write] [-tmp]

Time Based Data Exfiltration

optional arguments:
  -h, --help            show this help message and exit
  -url URL              URL
  -post POST            POST
  -threads THREADS      Threads
  -cookie COOKIE_FILE   Cookie File
  -file HEADER_FILE     Burp request file
  -retry RETRY          Retry request N times in case of network errors
  -timeout TIMEOUT      General timeout request
  -time AVGTIME         Added timeout to request
  -os OS                OS type (U unix/linux , W windows)
  -payload_limit LIMIT  If there is any command length limitation
  -force_write          Force writing auxiliary files
  -tmp                  Writing auxiliary files in tmp folder
