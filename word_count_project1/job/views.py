from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import operator
import urllib.request as urllib2
from collections import OrderedDict
from .models import Job
import nltk
import urllib
from bs4 import BeautifulSoup

def result(request):
    if request.method=='POST':
        if Job.objects.filter(body=request.POST['fulltext']):
            job=Job.objects.filter(body=request.POST['fulltext'])
            return render(request,'job/error.html',{'job':job})
        else:
            stopwords = ['a','A','about', 'above', 'across', 'after', 'afterwards']
            stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
            stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
            stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and','And','another']
            stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
            stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
            stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
            stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
            stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
            stopwords += ['bottom', 'but', 'by','By', 'call', 'can', 'cannot', 'cant']
            stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
            stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
            stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
            stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
            stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
            stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
            stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
            stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
            stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
            stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
            stopwords += ['herself', 'him', 'himself', 'his', 'how','How', 'however']
            stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
            stopwords += ['interest', 'into', 'is','Is', 'it', 'its', 'itself', 'keep']
            stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
            stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
            stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
            stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
            stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
            stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of','Of']
            stopwords += ['off', 'often', 'on','On','once', 'one', 'only', 'onto', 'or']
            stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
            stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
            stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
            stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
            stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
            stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
            stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
            stopwords += ['ten', 'than', 'that', 'the','The', 'their', 'them', 'themselves']
            stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
            stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
            stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
            stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
            stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
            stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
            stopwords += ['us', 'very', 'via', 'was', 'we','We', 'well', 'were', 'what']
            stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
            stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
            stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
            stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
            stopwords += ['within', 'without', 'would', 'yet', 'you','You', 'your']
            stopwords += ['yours', 'yourself', 'yourselves']
            url=request.POST['fulltext']
            #req = urllib2.Request(url)
            #wordcount = urllib2.urlopen(url).read()
            #wordcount=wordcount.text
            #wordcount=urllib.urlopen(request.POST['fullltext']).read()
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html)

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            wordcount=text.split()
            count=0
            jobs=Job()
            job=Job.objects
            worddictionary={}
            for word in wordcount:
                if word not in stopwords:
                    count+=1
                    if word in worddictionary:
                        worddictionary[word]+=1
                    else:
                        worddictionary[word]=1
            wordsorte=sorted(worddictionary.items(),key=operator.itemgetter(1),reverse=True)[:10]
            worddictionary = OrderedDict(sorted(worddictionary.items(), key=lambda x: x[1],reverse=True))
            temp=0
            database={}
            for word in worddictionary.keys():
                if temp<10:
                    database[word]=worddictionary[word]
                    temp+=1
            jobs.counts=count
            jobs.body=url
            jobs.topwords=database
            jobs.save()
            return render(request,'job/count.html',{'fulltext':text,'count':count,'worddictionary':wordsorte})
    else:
        return redirect('frequency')
def frequency(request):
    return render(request,'job/home.html')
def error(request):
    return render(request,'job/error.html')
