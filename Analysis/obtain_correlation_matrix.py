
# coding: utf-8

# In[1]:


import os
import sys
import numpy as np
import csv


# In[2]:


# generate a dict of pebl metrics to be correlated
# each element of the dict is another dict
pebl_metrics = {}
# generate a list of keys for the outer dict
names_of_pebl_metrics = []
# generate a dict of aasanas to be correlated
# each element of the dict is another dict
aasanas = {}
# generate a list of keys for the outer dict
names_of_aasanas = []
# generate a list of keys for the inner dict
subjIDs = []


# In[4]:


with open ('OUTPUT.csv','r') as output:
    csv_reader = csv.reader(output)
    i = 0
    # inititalize metric name
    metric_name = ''
    # initialize the key name
    subjID = ''
    # read the csv and classify
    for row in csv_reader:
        if(i%2 != 0):
            continue
        i = i + 1
        # extract metric value
        value = np.float64(row[3])
        # check if row represents an aasana or pebl data
        metric_name = row[1]+'_'+row[2]
        # add subjID to the list of keys of inner dict
        subjID = row[0]
        if(subjID not in subjIDs):
            subjIDs.append(subjID)
        # classify into aassana or pebl
        if(row[2]=='Stability'): # aasana
            if(metric_name not in names_of_aasanas):
                names_of_aasanas.append(metric_name)
                aasanas[metric_name] = {}
            inner_dict = aasanas[metric_name]
            inner_dict[subjID] = value
        else:
            if(metric_name not in names_of_pebl_metrics):
                names_of_pebl_metrics.append(metric_name)
                pebl_metrics[metric_name] = {}
            inner_dict = pebl_metrics[metric_name]
            inner_dict[subjID] = value


# In[9]:


with open('CORRELATION_MATRIX.csv','w') as corrM:
    csv_writer = csv.writer(corrM)
    row = ['Pebl Metric']
    for aasana in names_of_aasanas:
        row.append(aasana)
    csv_writer.writerow(row)


# In[10]:


prProg = 0
for pebl_metric in names_of_pebl_metrics:
    # user updates
    print('processing correlation '+ str(prProg+1) +' out of '+ str(len(names_of_pebl_metrics)))
    prProg += 1
    # extract inner dict for the given metric
    pebl_data = pebl_metrics[pebl_metric]
    # initialize the row to be printed
    row = [pebl_metric]
    for aasana in names_of_aasanas:
        corr_pebl = []
        corr_aasana = []
        # obtain inner dict aasana to correlate
        aasana_data = aasanas[aasana]
        for subjID in subjIDs:
            try:
                metric_value = pebl_data[subjID]
                stability_value = aasana_data[subjID]
                corr_pebl.append(metric_value)
                corr_aasana.append(stability_value)
                continue
            except:
                continue
        # obtain correlation of this metric for the given aasana
        try:
            X = np.float64(corr_pebl)
            Y = np.float64(corr_pebl)
            sigmaX = np.std(X)
            sigmaY = np.std(Y)
            meanX = np.mean(X)
            meanY = np.mean(Y)
            tempX = X-mean(X)
            tempY = Y-mean(Y)
            temp = tempX*tempY
            covXY = np.mean(temp)
            corrXY = covXY/(sigmaX*sigmaY)
            row.append(corrXY)
        # if the correlation cannot be obtained, append a string instead of the correlation value
        except:
            row.append('correlation error')
    with open('CORRELATION_MATRIX.csv','a') as corrM:
        csv_writer = csv.writer(corrM)
        csv_writer.writerow(row)
        # user updates
        print('fin: '+str(prProg))

