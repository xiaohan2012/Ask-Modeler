from urllib import urlopen
from pyquery import PyQuery as pq

SEARCH_TEMPLATE_URL='http://www.uniprot.org/uniprot/?sort=score&query=%s'
class Cralwer(object):
    def __init__(self,tar_name_fp='',tar_url_fp=''):
        self.targets=[]
        self.target_urls=[]
        if tar_url_fp:
            self.loadTargetUrls(tar_url_fp)
        elif tar_name_fp:
            self.loadTargets(tar_name_fp)
    def loadTargetUrls(self,fp) :
        with open(fp,'r') as f:
            for l in f.readlines():
                self.target_urls.append(l.strip())
        print self.target_urls

    def loadTargets(self,fp):
        """"""
        with open(fp,'r') as f:
            for l in f.readlines():
                self.targets.append(l.strip())
        print self.targets

    def getTargetPageUrl(self,target_name):
        """ """
        def getSearchUrl(target_name):
            return SEARCH_TEMPLATE_URL %target_name

        doc = pq(urlopen(getSearchUrl(target_name)).read())
        try:
            target_page_url = 'http://www.uniprot.org'+doc.find('#results tr td:eq(1)').children('a').attr('href')
            print target_page_url 
            self.target_urls.append(target_page_url)
            return target_page_url 
        except TypeError:
            return 'not found'


    def crawlTargetUrl(self):
        """"""
        with open('temp_url.dat','a') as f:
            for targ_name in self.targets:
                url = self.getTargetPageUrl(targ_name)
                f.write(url+'\n')
    def crawlTargetStructrInfo(self):
        """"""
        def get_3d_struct_info(target_url):
            """"""
            try:
                doc = pq(urlopen(target_url).read())

                return pq(doc('.subsection h3#section_x-ref_structure').parent().parent().next().children('td')[1]).html()
            except:
                return 'seems no info'

        self.struct_info = {}
        for url in self.target_urls:
            print 'crawling %s'%url
            info = get_3d_struct_info(url)
            self.struct_info[url] = info
            print info
        print self.struct_info
        with open('crawled_result.dat','w') as f:
            for k,v in self.struct_info.items():
                f.write('%s:%s\n' %(k,v))

if __name__ == '__main__':
    crawler=Cralwer(tar_name_fp='',tar_url_fp='temp_url.dat')
    crawler.crawlTargetStructrInfo()
