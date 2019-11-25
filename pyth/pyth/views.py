from django.shortcuts import render
import requests
import sys
import pyth.rewrite
import pyth.spell
import pyth.gram_check
import pyth.empty
from subprocess import run,PIPE
from django.http import JsonResponse
import json

def home(request):
    return render(request,'/home/yash/Kids Next Door/RedPencil/pyth/templates/home_new.html')

def answer_me(request):
    field = request.GET.get('inputValue')
    state = int(request.GET.get('state'))
    # print(state)
    # print(field)
    # answer = syn.rewrite(field)

    # out= run([sys.executable,'/home/yash/django/pyth/master.py',field],shell=False,stdout=PIPE)
    # answer = str(out.stdout)
    answer = {}
    if (state==2):
    	print("Rewriter Call : ",field)
    	answer2 = pyth.rewrite.rewrite(field)
    	for k in answer2.keys():
    		if (len(answer2[k])!=0):
    			answer[k] = ["green"]
    			answer[k] += answer2[k]
    		else:
    			answer[k] = []
    
    elif (state==0):
    	print("SpellCheck Call : ",field)
    	answer0 = pyth.spell.outp(field)
    	for k in answer0.keys():
    		if (len(answer0[k])!=0):
	    		answer[k] = ["red"]
	    		answer[k] += answer0[k]
	    	else:
    			answer[k] = []
    
    elif (state==1):
    	print("Grammer Call : ",field)
    	answer1 = pyth.gram_check.outp(field)
    	for k in answer1.keys():
    		if (len(answer1[k])!=0):
    			answer[k] = ["blue"]
    			answer[k] += answer1[k]
    		else:
    			answer[k] = []
    else:
    	print("The End",field)
    	answer3 = pyth.empty.outp(field)
    	for k in answer3.keys():
    		if (len(answer3[k])!=0):
    			answer[k] = ["blue"]
    			answer[k] += answer3[k]
    		else:
    			answer[k] = []
    
    
    
    # print(answer1)
    # print(answer2)
    # print(answer3)
    
    # for k in answer2.keys():
    # 	if(len(answer3[k])!=0):
    # 		answer[k] = ["blue"]
    # 		answer[k] += answer3[k]
    # 	elif(len(answer2[k])!=0):
    # 		answer[k] = ["red"]
    # 		answer[k] += answer2[k]
    # 	elif (len(answer1[k])!=0):
    # 		answer[k] = ["green"]
    # 		answer[k] += answer1[k]
    # 	else:
    # 		answer[k] = []
    print(answer)
    # answer = json.dumps(answer)
    # print(answer)
    # answer = json.loads(answer)
    # print(answer)
    # data = {
    #     'respond': answer
    #         }
    return JsonResponse(answer)