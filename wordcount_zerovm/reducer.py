#!/python

import os
import json
from datetime import datetime
total_stats = {
    "books": 0,
    "words": 0,
    "wordlist": {}
}


def systime():
    hr()
    print('Current time: %s' % datetime.utcnow())


#print('start time: %s' % datetime.utcnow())

#debug("reducer",os.environ['SCRIPT_NAME'])
#systime()
#debug("server name",os.environ['SERVER_NAME'])

#count = 0
for filename in os.listdir('/dev/in'):
    with open(os.path.join('/dev/in', filename), 'r') as f:
        stats = json.loads(f.read())
#        print f
#        print stats

    total_stats['words'] += stats['words']
    total_stats['books'] += 1
    
    for word in stats['wordlist'].keys():
        total_stats['wordlist'][word] = total_stats['wordlist'].get(word, 0) + stats['wordlist'][word]
#input_file = '/dev/in/wordcount-mapper-'+ str(os.environ['SCRIPT_NAME'][18:])
#print input_file

#with open(input_file,'r') as f:
#    stats = json.loads(f.read())
#    print f
#    print stats

#total_stats['words'] += stats['words']
#total_stats['books'] += 1


print 'Total books: %d' % total_stats['books']
print 'Total words: %d' % total_stats['words']

for wordpair in sorted(total_stats['wordlist'].items(), key=lambda(k,v): v, reverse=True)[:100]:
    print '%7d %s' % (int(wordpair[1]), wordpair[0])

#print('End time: %s' % datetime.utcnow())
#systime()
