# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#Approach)
3. [RunInstructions](README.md#RunInstructions)

# Problem

The US Department of Labor website contains the yearly history for H-1B(H-1B, H-1B1, E-3) visa application processing document. A newspaper editor want to analyze the H1B data and I helped to create a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script should produce the results in the `output` folder without needing to change the code.

# Approach

The problem is handeled with python(3), and only requires importing sys packages, no requirement for any other packages like pandas or numpy. In this task, 4 functions are designed, specifically, they will do:

1. get_h1b_data(file): load data and get the index for State code and Job tile code, for future reference. This function will search for the index for 'EMPLOYER_STATE' and 'SOC_NAME', not hard coding the position of these columns, so it can tolerate with these columns in different positions accross different input files. 

2. count_to_dict(data, location): calculate group count and save the information into a dictionary. This function will only take those case 'certified' into consideration.

3. dict_to_pct(data): calculate percentage based on the count, and combine the percentage with the former dictionary into a list. In this list, each item is another list with 3 items, during which item1 is key name, either a state code or a job code, item2 is the count for the key, and item3 is the percentage for this key. The list will be sorted by percentage descendingly and then by first element alphabatically; As the kaggle requires, we only output top10 items here, if user want to output more lines, just modify the return part to 'return result[0:No. lines to output]'

4. get_final_pct(inputfile, outputfile, job_state): combine former 3 functions and output the data accordingly 

# RunInstructions 

Run 

    h1b_statistics~$ ./run.sh 

It should generate two text files in the output folder: 

* `top_10_occupations.txt`: Top 10 occupations for certified visa applications
* `top_10_states.txt`: Top 10 states for certified visa applications

The run.sh file contains this command: 

    python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt

The processing time for 230MB input file is around 40 seconds based on my test. 
