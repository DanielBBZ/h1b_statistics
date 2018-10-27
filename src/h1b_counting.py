# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 21:37:43 2018

@author: Binbin Zhou

required: 
Python3, import sys

In this task, 4 functions are designed, specifically, they will do:
1. load data
2. calculate group count and save into a dictionary
3. calculate percentage based on the count, and combine the percentage with the former dictionary into a list
4. combine former 3 functions and output the data accordingly 
"""

from sys import exit, argv

def get_h1b_data(file):
    """get the h1b data from local csv
    Args
    ----
    file: file location with the file name
    
    Returns
    -------
    data: a python list to include all content from the file
    index_list: a list include two item, index_list[0] is index of State in each line, index_list[1] is index of Job 
    
    use case: data,index_list =get_h1b_data('../insight_testsuite/tests/test_2/input/H1B_input.csv')
    """
    try:
        with open(file,encoding="utf8",mode='r') as f:
            data = []
            for line in f:
                words = line.split(';')
                data.append((words[0], words[1:]))
    except:
        exit("-- Unable to load the file")
    
    #Get the index for the columns we are going to use for counting
    State_loc = data[0][1].index('EMPLOYER_STATE')  #get the index for State
    Job_loc = data[0][1].index('SOC_NAME')          #get the index for Job code
    
    index_list = [State_loc, Job_loc]
    
    return (data, index_list)
	

def count_to_dict(data, location):
    """function to count the frequency of state and job, store into specific dictionaries
    Args
    ----
    data: list to store all loaded content
    location: int, the index for the content need to be counted, in this case, it should be 'state' or 'job'
    
    Returns
    -------
    result: a python dictionary with either job or state as key, and their count as value
    
    use case: Job_count = count_to_dict(data, Job_loc)
    """
    Status_loc = data[0][1].index('CASE_STATUS')    #get the index for case_status
    result = {}
    for i in range(1,len(data)):
        if data[i][1][Status_loc] == 'CERTIFIED':         #only count if the case is certified
            key = data[i][1][location].strip('\"')        #remove " in the str
            if not key in result:
                result[key] = 1
            else:
                result[key] += 1
        else:
            None
   
    return result
	
	
def dict_to_pct(data):
    """calculate percentage of value in dictionary for each key, and store all results in a list
    
    Args
    ----
    data: name of a dictionary, the value is the count of the key 
        
    Returns
    -------
    result: a python list, each item in this list is another list with 3 items, 
            item1 is key name, either a state code or a job code, item2 is the count for the key, 
            and item3 is the percentage for this key. 
            The list will be sorted by percentage descendingly and then by first element alphabatically;
            As the kaggle requires, we only output top10 items here
    
    use case: Job_list = dict_to_pct(Job_D)    
    """
    data1 = data.copy()
    for key, value in data1.items():
        data1[key] = str(round(value*100/(sum(data.values())),1))+'%'
    
    # sort the dictionary by value with ascending, and sort the key with ascending order 
    temp1 = dict(sorted(data.items(), key=lambda kv: kv[0], reverse=False))
    temp2 = dict(sorted(temp1.items(), key=lambda kv: kv[1], reverse=True))
    
    result =[]
    for key, value in temp2.items():
        result.append([key, value, data1[key]])
    
    return result[0:10]
	
	
def get_final_pct(inputfile, outputfile, job_state):
    """combine all former functions, load the input file, do the calculations, and output the data
    Args
    ----
    inputfile: the csv file for input
    outputfile: the output file name to write result into 
    job_state: user should input 'job' or 'state', to tell python which one they wanna statistics
    
    Returns
    -------
    result: a text with the name defined as outputfile, which store the top 10 states or top 10 occupations
    
    use case: get_final_pct('H1B_input.csv','top_10_states.txt', 'state')
    """
    VALID_STATUS = {'job','state'}
    
    data,index_list = get_h1b_data(inputfile)
    
    if job_state == 'state':
        Count_D = count_to_dict(data, index_list[0])
        Count_D_pct = [['TOP_STATES','NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']] + dict_to_pct(Count_D)
    elif job_state == 'job':
        Count_D = count_to_dict(data, index_list[1])
        Count_D_pct = [['TOP_OCCUPATIONS','NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']] + dict_to_pct(Count_D)
    else:
        print("job_state in get_final_pct(inputfile, outputfile, job_state) must be one of %r." % VALID_STATUS)
        raise SystemExit
    
    
    with open(outputfile, 'w') as filehandle:  
        for item in Count_D_pct:
            filehandle.write('%s\n' % ";".join(map( lambda x: str(x), item)))

	
try:
	inputfile = str(argv[1])
	outputfile1 = str(argv[2])
	outputfile2 = str(argv[3])

	get_final_pct(inputfile, outputfile1, 'job')
	get_final_pct(inputfile, outputfile2, 'state')

except IndexError:
	print ('Error: wrong input')
	print ('Example: python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt')
