#!/usr/bin/python
import os
import time
import bs4
import sys
import datetime
import urllib2
from bs4 import BeautifulSoup
sys.path.append('./')
import indexpage as ip

def dumpDataFromURL(url,datestr,out1,out2):
	parser=ip.PageParser()
	page=1
	pageMax=1
	while True:
		doUrl=url%(str(page),)
		print 'general\t',doUrl
		sys.stdout.flush()
		time.sleep(3)
		soup=parser.parseURL(doUrl)
		if soup.tbody is not None:
			#data is not published
			if ''.join(soup.stripped_strings).find(u'\u6570\u636e\u6682\u672a\u516c\u5e03')>=0:
				break
			if page==1:
				pageMax=soup.find(attrs={'id':'m_page'})
				if pageMax is not None:
					pageMax=pageMax.span.string
					pageMax=int(pageMax[pageMax.rfind('/')+1:])
			generalInfo=parser.getGeneralInfo(soup)
			for info in generalInfo:
				out1.write('\001'.join(info).encode('utf8','ignore')+'\001'+datestr+'\n')
				out1.flush()
				print 'detail\thttp://data.10jqka.com.cn/market/lhbcjmx/code/%s/date/%s/ajax/1'%(info[0],datestr)
				sys.stdout.flush()
				time.sleep(5)
				soup2=parser.parseURL('http://data.10jqka.com.cn/market/lhbcjmx/code/%s/date/%s/ajax/1'%(info[0],datestr))
				if soup2.tbody is not None:
					detailInfo=parser.getDetailedInfo(info[0],soup2)
					for detail in detailInfo:
						out2.write('\001'.join(detail).encode('utf8','ignore')+'\001'+datestr+'\n')
						out2.flush()
		page+=1
		if page>pageMax:
			break

if __name__=='__main__':
	if len(sys.argv)<5:
		print 'Usage:COMMAND <out1> <out2> <date> <len>'
		sys.exit(1)

	if os.path.exists(sys.argv[1]):
		print '%s file exists'%(sys.argv[1])
		sys.exit(1)

	if os.path.exists(sys.argv[2]):
		print '%s file exists'%(sys.argv[2])
		sys.exit(1)

	out1=file(sys.argv[1],'w')
	out2=file(sys.argv[2],'w')
	startDate=datetime.datetime.fromtimestamp(time.mktime(time.strptime(sys.argv[3],"%Y-%m-%d")))
	for x in range(0,int(sys.argv[4])):
		delta=datetime.timedelta(-1*x)
		cDate=startDate+delta
		url='http://data.10jqka.com.cn/market/longhu/cate/ALL/field/REMARK/page/%s/date/'+cDate.strftime('%Y-%m-%d')+'/order/asc/ajax/1/&host=data.10jqka.com.cn'
		dumpDataFromURL(url,cDate.strftime('%Y-%m-%d'),out1,out2)
	out1.close()
	out2.close()
