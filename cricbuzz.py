# -*- coding: utf-8 -*-
import scrapy
import re
class CricbuzzSpider(scrapy.Spider):
    name = 'cricbuzz'
    #allowed_domains = ['cricbuzz.com']
    start_urls = ['https://www.cricbuzz.com/cricket-scores/18857/ind-vs-aus-2nd-odi-australia-tour-of-india-2017']

    def parse(self, response):
        x=response.xpath('//span[@class="cb-col cb-col-8 text-bold"]/text()').extract()
        y=response.xpath('//p[contains(@class,"cb-col cb-col-90 cb-com-ln")]').extract()
         
        for i in range(len(y)):
            runs=re.findall(r'[\w ]+ to [\w ]+, [\w]+ r[\w]+,',y[i])
            runs_str=' '.join(str(x) for x in runs)
            boundary=re.findall(r'[\w ]+ to [\w ]+, <b>[\w]+</b>+,',y[i])
            boundary_str=' '.join(str(x) for x in boundary)
            out=re.findall(r'[\w ]+ to [\w ]+, <b>[\w]+</b>+ ',y[i])
            out_str=' '.join(str(x) for x in out)
            legbyes= re.findall(r'[\w ]+ to [\w ]+, [\w]+ by[\w]+, [\w] r[\w]+,',y[i])
            legbyes_str=' '.join(str(x) for x in legbyes)
            legbyesboundary=re.findall(r'[\w ]+ to [\w ]+, [\w]+ by[\w]+, <b>[\w]*</b>',y[i])
            legbyesboundary_str=' '.join(str(x) for x in legbyesboundary)
            
            count=[len(runs),len(boundary),len(out),len(legbyes),len(legbyesboundary)]
            for length in range(len(count)):
                if count[length]==1:
                    index=length
            if index==0:
                y[i]= re.split(' to |, |, |,',runs_str)
                
            elif index==1:
                y[i]=re.split(' to |, |, |,',boundary_str)
                bold=y[i][2]
                bold_text=re.split('<b>|</b>',bold)
                y[i][2]=bold_text[1]
                
                
            elif index==2:
                y[i]=re.split(' to |, |, |,',out_str)
                y[i]=re.split(' to |, |, |,',out_str)
                bold=y[i][2]
                bold_text=re.split('<b>|</b>',bold)
                y[i][2]=bold_text[1]
            elif index==3:
                y[i]= re.split(' to |, |, |,',legbyes_str)
            elif index==4:
                y[i]=re.split(' to |, |, |,',legbyesboundary_str)
        x.reverse()
        y.reverse()
        
            
        for item in zip(x,y):
            
            info={
                'Ball': item[0],
                'Bowler' : item[1][0],
                'Batsman': item[1][1],
                'Runs': ' ',
                'Status': item[1][2],
                'Remarks':' '
            }
            if info['Status']=='leg byes':
                
                info['Remarks']='Leg byes'
                info['Status']=item[1][3]
                
            if info['Status']=='FOUR':
                info['Runs']=4
            elif info['Status']=='SIX':
                info['Runs']=6
            elif info['Status']=='out':
                info['Runs']=0
                info['Remarks']='OUT'
            elif info['Status']=='1 run':
                info['Runs']=1
            elif info['Status']=='2 runs':
                info['Runs']=2
            elif info['Status']=='3 runs':
                info['Runs']=3
            elif info['Status']=='no run':
                info['Runs']=0
            elif info['Status']=='wide':
                info['Runs']=1
                info['Remarks']='Extra Run'
            yield info
