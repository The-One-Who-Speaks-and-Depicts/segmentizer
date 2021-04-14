import numpy as np

def mean_length_score(text):
    given_list = text.split(' ')
    raw_list = []    
    for i in given_list:
        raw_list.append(len(i))
    Q1, Q3 = np.percentile(raw_list, [25,75])
    IQR=Q3-Q1
    minimum=Q1-1.5*IQR
    maximum=Q3+1.5*IQR
    result_list = []
    for i in given_list:
        if (len(i) > minimum and len(i) < maximum):
            result_list.append(len(i))
    mean = np.mean(result_list)
    return mean