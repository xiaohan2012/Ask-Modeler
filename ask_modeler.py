import re
import urllib2
from urllib import urlencode,urlopen
from pyquery import PyQuery as pq
import os

def extract_url_from_file(fp,o_fp='modeller_task.dat'):
    with open(fp,'r') as f:
        with open(o_fp,'w') as of:
            for l in f.readlines():
                if "http://salilab.org/modbase-cgi/model_search.cgi" in l:
                    print l
                    uniprot_url = l.split(':<',1)[0]
                    modeller_url = re.findall('http://salilab\.org/modbase-cgi/model_search\.cgi\?searchkw=name&amp;kword=\w*',l.split(':<',1)[1])[0]
                    of.write('%s\n' %(modeller_url))


data_tplt=[('.cgifields','longdope'),
      ('.cgifields','modbase'),
      ('.cgifields','academic'),
      ('.cgifields','dope'),  
      ('modweb_name','ModBaseUpdate'),
      ('email','modbase@salilab.org'),
      ('modellerkey','MODELIRANJE'),
      ('runname','update'),
      ('type','submit'),
      ('submittype','modbaseupdate'),
      ('academic','academic'),
      ('seqfile',''),
      ('dope','MPQS'),
      ('longdope','LONGEST_DOPE'),
      ('search','1337'),
      ('modbase','modbase'),
      ('sequence','')
     ]
header_tplt={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
         'Accept-Encoding':'gzip, deflate',
         'Accept-Language':'zh-cn,zh;q=0.5',
         'Connection':'keep-alive',
         'Cookie':'modbase-academic=modbase_user&anonymous&modbase_passwd&anonymous; __utma=63640115.1990740024.1327732985.1327732985.1327738009.2; __utmz=63640115.1327738009.2.2.utmcsr=salilab.org|utmccn=(referral)|utmcmd=referral|utmcct=/modbase-cgi/model_search.cgi; __utmb=63640115.3.10.1327738009; __utmc=63640115',
         'Host':'modbase.compbio.ucsf.edu',
         'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
         'Referer':'',
        }

def get_modeler_url(tar_name,src_fp='result.csv'):
    with open(src_fp,'r') as f:
        for l in f.readlines():
            if tar_name in l:
                return 'http://salilab.org/modbase-cgi/model_search.cgi?searchkw=name&kword=%s' %(l[-8:-2] )
        return ''

def post_task(url):
    doc=pq(urlopen(url).read())
    if doc.find('#rightside').find('a').parent('p') and \
       'This sequence has not been modeled.' in doc.find('#rightside').find('a').parent('p').html():
        #if not modeled
        seq_url = doc.find('#rightside').find('a').attr('href')
        seq = re.findall('sequence=(\w*)',seq_url)[0]
        data_tplt.pop()#replace the "sequence" part
        data_tplt.append(('sequence',seq))
        header_tplt['Referer'] = seq_url
        req = urllib2.Request('https://modbase.compbio.ucsf.edu/scgi//modweb.cgi',urlencode(data_tplt),header_tplt)
        res = urllib2.urlopen(req)
        return res
    else:
        print 'already modeled'

if __name__ == "__main__":
    with open('modeler_task_target_name.dat','r') as f:
        for l in f.readlines():
            url = get_modeler_url(l.strip())
            print l.strip()
            print url
            print

            res = post_task(url)
            res_fp='model_results/%s.html' %(url[-6:])
            if not os.path.exists(res_fp):
                if res:
                    f=open(res_fp,'w')
                    f.write(res.read())
                    f.close()
            else:
                print '%s exists' %res_fp



