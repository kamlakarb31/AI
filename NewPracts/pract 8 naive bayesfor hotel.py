import pandas as pd

def predict(features, response, custcase):
    anskeys = list(response.keys())
    ansvalues = dict.fromkeys(anskeys,0)
    for respkey in anskeys :
        ansvalues[respkey] = response[respkey]            
        for custfeature, custval in custcase.items() :
            ansvalues[respkey] = ansvalues[respkey] * features[custfeature][custval][respkey]
        print("ans key is = " , ansvalues[respkey])
    print("Calculation(unnoramlized) - \n", ansvalues)
    #MAP Calculation
    maxkey=""
    maxans=-1
    for ikey, ival in ansvalues.items():
        if ival > maxans :
            maxans= ival
            maxkey = ikey
    return maxkey

col_names = ['Reservation', 'Raining', 'BadService','Satur','Result']
hoteldata = pd.read_csv("hotelfornaive.csv", header=None, names=col_names)
feature_cols = ['Reservation', 'Raining', 'BadService','Satur']
X = hoteldata[feature_cols] # Feature Columns
y = hoteldata.Result # Target variable
#https://www.geeksforgeeks.org/naive-bayes-classifiers/

resp_probabilities = dict()
resp_set = set(y)
for resp_val in resp_set:
    resp_probabilities[resp_val] = 0
print("resp count :\n" , resp_probabilities)
rows = X.shape[0]
cols = X.shape[1]
feature_probabilities = dict()
col=0
for featurename in feature_cols :
    featurename_set = set(X.iloc[:,col])
    col = col+1
    feature_probabilities[featurename] = dict()
    for item in featurename_set :
        feature_probabilities[featurename][item] = resp_probabilities.copy()
print("feature count :\n", feature_probabilities)        

print("Probability Value Ex 1:", feature_probabilities["Reservation"][1]["Wait"])
print("Probability Value Ex 2:", feature_probabilities["Satur"][2]["Leave"])

for r in range(0,rows)   :
    resp_probabilities[y.iloc[r]] = resp_probabilities[y.iloc[r]] + 1
    for c in range(0,cols):
        feature_probabilities [feature_cols[c]] [X.iloc[r][c]] [y.iloc[r]] += 1     

print("Initial Values - \n")
print("Resp count :\n" , resp_probabilities)
print("Feature count :\n", feature_probabilities)              

for featurename in feature_cols:
    for featureval in feature_probabilities[featurename].keys():
        #print(featureval)
        for key in feature_probabilities[featurename][featureval].keys() :
            feature_probabilities[featurename][featureval][key] = feature_probabilities[featurename][featureval][key]  / resp_probabilities[key] 
            

for res_key in resp_probabilities.keys() :        
    resp_probabilities[res_key] = resp_probabilities[res_key] / rows
    
print("Final Values - \n")
print("Resp count :\n" , resp_probabilities)
print("Feature count :\n", feature_probabilities)                  
print("Probability Value Ex 1:", feature_probabilities["Reservation"][1]["Wait"])
print("Probability Value Ex 2:", feature_probabilities["Satur"][2]["Leave"])

res_status = int(input("Manager asks Customer, have you reserved table?(1/2):"))
rain_status = int(input("Raining outside ?(1/2):"))
badserv_status = int(input("Customer got bad service?(1/2):"))
satur_status = int(input("Is saturday today ?(1/2):"))

custcase = {'Reservation':res_status, 'Raining':rain_status, 'BadService':badserv_status,'Satur':satur_status}
print("Manager predicts that Customer will :" , predict(feature_probabilities, resp_probabilities,custcase) )

    








