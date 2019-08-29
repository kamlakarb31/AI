# https://www.analyticsindiamag.com/introduction-to-boosting-implementing-adaboost-in-python/
import pandas as pd

data = pd.read_csv("apples_and_oranges.csv")
print(data)

from sklearn.model_selection import train_test_split
training_set, test_set = train_test_split(data, test_size = 0.2, random_state = 1)
# first parameter represents data
# second parameter represents size whose value is between 0 to 1, how much test data you want
# third parameter represents seed(start point of random number generator)


X_train = training_set.iloc[:,0:2].values #column 0 & 1 of all rows
Y_train = training_set.iloc[:,2].values #column 2 of all rows
X_test = test_set.iloc[:,0:2].values
Y_test = test_set.iloc[:,2].values

from sklearn.ensemble import AdaBoostClassifier
adaboost = AdaBoostClassifier(n_estimators=100, base_estimator= None,learning_rate=1, random_state = 1)
'''n_estimators : integer, optional (default=50)
The maximum number of estimators at which boosting is terminated. In case of perfect fit, the learning procedure is stopped early.
base_estimator : object, optional (default=None)

The base estimator from which the boosted ensemble is built. Support for sample weighting is required, as well as proper classes_ and n_classes_ attributes.
If None, then the base estimator is DecisionTreeClassifier(max_depth=1)

learning_rate : float, optional (default=1.)
Learning rate shrinks the contribution of each classifier by learning_rate. There is a trade-off between learning_rate and n_estimators.

random_state : int, RandomState instance or None, optional (default=None)
If int, random_state is the seed used by the random number generator; If RandomState instance, random_state is the random number generator;
If None, the random number generator is the RandomState instance used by np.random.

'''

adaboost.fit(X_train,Y_train)
# Build a boosted classifier from the training set (X, y).

Y_pred = adaboost.predict(X_test)


test_set["Predictions"] = Y_pred

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test,Y_pred)
'''
Compute confusion matrix to evaluate the accuracy of a classification
By definition a confusion matrix  is such that  is equal to the number of observations known to be in group  but predicted to be in group .
Thus in binary classification, the count of true negatives is , false negatives is , true positives is  and false positives 
'''

accuracy = float(cm.diagonal().sum())/len(Y_test)
print("\nAccuracy Of AdaBoost For The Given Dataset : ", accuracy)



'''
# Load libraries
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets
print("j")
# Import train_test_split function
from sklearn.model_selection import train_test_split
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
iris = datasets.load_iris()
X = iris.data
y = iris.target
# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
abc = AdaBoostClassifier(n_estimators=50,
                         learning_rate=1)
# Train Adaboost Classifer
model = abc.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = model.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
'''
