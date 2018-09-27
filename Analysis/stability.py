import sys
import numpy as np
import os
import csv
#usage
def usage():
    print('<address> <starttime(s)> <duration(s)> <subjectID> <aasanaID>')
if(len(sys.argv) != 6):
    usage()
#filename = 'version2/Kunal_Naukasana/joints.csv'
filename = sys.argv[1]
joints = []
with open(filename, 'r') as fo:
    csv_reader = csv.reader(fo)
    i = 0
    for row in csv_reader:
        if(i%2 == 0):
            joints.append(row) 
        i = i+1

joint_types = ['JointType_SpineBase',
               'JointType_SpineMid',
               'JointType_Neck',
               'JointType_Head',
               'JointType_ShoulderLeft',
               'JointType_ElbowLeft',
               'JointType_WristLeft',
               'JointType_HandLeft',
               'JointType_ShoulderRight',
               'JointType_ElbowRight',
               'JointType_WristRight',
               'JointType_HandRight',
               'JointType_HipLeft',
               'JointType_KneeLeft',
               'JointType_AnkleLeft',
               'JointType_FootLeft',
               'JointType_HipRight',
               'JointType_KneeRight',
               'JointType_AnkleRight',
               'JointType_FootRight',
               'JointType_SpineShoulder',
               'JointType_HandTipLeft',
               'JointType_ThumbLeft',
               'JointType_HandTipRight',
               'JointType_ThumbRight'
               ]

weights = np.zeros((len(joint_types),3),dtype = np.float64)
weights = weights + 1

jointwise = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
for row in joints:
    for j in range(len(joint_types)):
        if(row[2]==joint_types[j]):
            jointwise[j].append(row)
def getIndices(h,m,s):
    #binary search for finding index
    timestring = 0
    lb = 0
    ub = len(jointwise[1])
    mid = int((lb+ub)/2)
    while(lb<ub):
        timestring = jointwise[0][mid][1]
        jh,jm,js = timestring.split(':')
        jh,jm,js = np.float64(jh),np.float64(jm),np.float64(js)
        compare = 3600*(jh-h)+60*(jm-m)+(js-s)
        if(compare>0): #it means data[mid] is greater than item
            ub = mid-1
        elif(compare<0):
            lb = mid+1
        else:
            return mid
        mid = int((lb+ub)/2)
    return mid

start = sys.argv[2]
#start = '0:1:0'
sh = int(start/3600)
sm = int((start%3600)/60)
ss = (start%60)
'''
sh,sm,ss = start.split(':')
sh,sm,ss = np.float64(sh),np.float64(sm),np.float64(ss)
'''
duration = sys.argv[3]
dh = int(duration/3600)
dm = int((duration%3600)/60)
ds = (duration%60)
#duration = '0:2:0'
'''
dh,dm,ds = duration.split(':')
dh,dm,ds = np.float64(dh),np.float64(dm),np.float64(ds)
'''
initial = jointwise[0][0][1]
Ih,Im,Is = initial.split(':')
Ih,Im,Is = np.float64(Ih),np.float64(Im),np.float64(Is)
#commencement of holding aasana
cs = (Is + ss)%60
cm = int((Is+ss)/60) + Im + sm
ch = Ih + sh + int(cm/60)
cm = cm%60
#end of holding aasana
es = cs + ds
em = int(es/60) + cm + dm
es = es%60
eh = int(em/60) + ch + dh
em = em%60
#get indices
begin = getIndices(ch,cm,cs)
end = getIndices(eh,em,es)
print(jointwise[0][begin][1])
print(jointwise[0][end][1])
instability = []
for i in range(25):
    any_joint = jointwise[i]
    hrs = []
    mns = []
    scs = []
    x = []
    y = []
    z = []
    varX = []
    varY = []
    varZ = []
    inverted_frame_rate = []
    for row in any_joint[begin+10:end-10]:
        hours, minutes, seconds = row[1].split(':')
        hours, minutes, seconds = np.float64(hours), np.float64(minutes), np.float64(seconds) 
        hrs.append(hours)
        mns.append(minutes)
        scs.append(seconds)
        x.append(np.float64(row[7]))
        y.append(np.float64(row[8]))
        z.append(np.float64(row[9]))
    mx,my,mz = np.mean(x),np.mean(y),np.mean(z)
    for i in range(1,len(x)):
        inverted_frame_rate.append(3600*(hrs[i]-hrs[i-1])+60*(mns[i]-mns[i-1])+(scs[i]-scs[i-1]))
        varX.append(inverted_frame_rate[i-1]*((x[i]-mx)**2))
        varY.append(inverted_frame_rate[i-1]*((y[i]-my)**2))
        varZ.append(inverted_frame_rate[i-1]*((z[i]-mz)**2))
    sumlist = np.array([sum(varX),sum(varY),sum(varZ)])
    normalizer = sum(inverted_frame_rate)
    instability.append(sumlist/normalizer)

weighted_instability_matrix = instability*weights

inst = np.sum(weighted_instability_matrix)

print(normalizer)
print(sumlist)
'''
try:
    os.chdir(sys.argv[6]+'_correlation')
except:
    os.mkdir(sys.argv[6]+'correlation')
    os.chdir(sys.argv[6]+'correlation')
with open(sys.argv[5]+'.csv','a') as corr:
    row_csv = [sys.argv[4],inst]
    writer = csv.writer(corr)
    writer.writerow(row_csv)
'''
row = [sys.argv[4],sys.argv[5],'Stability',inst]
with open('OUTPUT.csv','a') as csvFile:
    csv_writer = csv.writer(csvFile)
    csv_writer.writerow(row)
print(sys.argv[4],sys.argv[5],'Stability',inst)
