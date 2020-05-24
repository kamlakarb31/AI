# for building the model
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics 
# for plotting tree
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus

col_names = ['Reservation', 'Raining', 'BadService','Satur','Result']
hoteldata = pd.read_csv("hotel.csv", header=None, names=col_names)
feature_cols = ['Reservation', 'Raining', 'BadService','Satur']
X = hoteldata[feature_cols] # Feature Columns
y = hoteldata.Result # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                            test_size=0.3, random_state=1) 
# 70% training and 30% test
#clf = DecisionTreeClassifier()
clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)
clf = clf.fit(X_train,y_train)
#Predict the response for test dataset
y_pred = clf.predict(X_test)
print("ytest = ", y_test)
print("ypred = ", y_pred)
# Accuracy of the model
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# install graphviz library from https://graphviz.gitlab.io/_pages/Download/Download_windows.html
# update your path variable to include C:\Program Files (x86)\Graphviz2.38\bin

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  filled=True, rounded=True,
                 feature_names = feature_cols,
                class_names=['Leave','Wait'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 
graph.write_png('hotel.png')


















