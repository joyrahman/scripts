#!/python 

import json
import os
from datetime import datetime

word_data = {
    "words": 0,
    "wordlist": {}
}


#systime()
#debug("server name",os.environ['SERVER_NAME'])
with open('/dev/input', 'r') as f:
    for line in f.xreadlines():
        for word in [w.lower().strip('\t ,.!\'') for w in line.split()]:
                word_data['words'] += 1
                word_data['wordlist'][word] = word_data['wordlist'].get(word, 0) + 1

toplist = dict(sorted(word_data['wordlist'].items(), key=lambda(k,v): v, reverse=True)[:200])
word_data['wordlist'] = toplist
#print word_data['wordlist']
try:
    with open('/dev/out/reducer', 'a') as f:
#    reducer_file = '/dev/out/wordcount-reducer-'+ str(os.environ['SCRIPT_NAME'][17:])
#    print reducer_file
#    with open(reducer_file, 'a') as f:
        f.write(json.dumps(word_data, encoding="latin_1"))
#        print word_data
except Exception as inst:
   print inst
   print type(inst)
   print inst.args

#print('end time: %s' % datetime.utcnow())
#systime()

