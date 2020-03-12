from django.http import HttpResponse
from django.shortcuts import render
import operator
def homepage(request):

    return render(request,'home.html')
def count(request):
    fulltext=request.GET['fulltext']
    wordcount=fulltext.split()
    worddictionary={}
    for word in wordcount:
        if word in worddictionary:
            worddictionary[word]+=1
        else:
            worddictionary[word]=1
    wordsorte=sorted(worddictionary.items(),key=operator.itemgetter(1),reverse=True)
    return render(request,'count.html',{'fulltext':fulltext,'count':len(wordcount),{'worddictionary':wordsorte})
def about(request):
    return render(request,'about.html')
