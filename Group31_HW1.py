# -*- coding: utf-8 -*-
"""ML_Assignment1_SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UMLT8bisUB1-bfFQnMP9KCNXo9AS5pxu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm, datasets
import seaborn as sns
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.datasets import make_classification, make_circles
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from matplotlib.colors import ListedColormap
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
from sklearn.linear_model import Perceptron
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

X = np.array([[1.3, 3.3], [1.4, 2.5], [1.8, 2.8], [1.9, 3.1], [1.5, 1.5], [1.8, 2], [2.3, 1.9], [2.4, 1.4], [2.4, 2.4], [2.4, 3], [2.7, 2.7], [2.3, 3.2]])
Y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])

X_test = np.array([[1.7, 2.5], [1.9, 2.7], [2, 2.15], [2.4, 2], [2.2, 3.25], [2.4, 2.25]])
y_test = np.array([0, 0, 1, 1, 2, 2])

custom_cmap = ListedColormap(['red', 'blue', 'orange'])

def plot_tsne(X, y, class_names):
    # Compute t-SNE embedding
    tsne = TSNE(n_components=2, perplexity=11, random_state=42)
    X_embedded = tsne.fit_transform(X)
    # Create a DataFrame with the embedding and class labels
    data = pd.DataFrame(X_embedded, columns=['x', 'y'])
    data['class'] = y
    # Set the color palette​
    palette = sns.color_palette('bright', n_colors=len(class_names))
    # Plot the t-SNE embedding colored by class​
    fig, ax = plt.subplots(figsize=(8, 8))
    for i, class_name in enumerate(class_names):
        mask = data['class'] == class_name
        ax.scatter(data.loc[mask, 'x'], data.loc[mask, 'y'],   label=class_name, s=50, alpha=0.8, c=palette[i])
    ax.set_xlabel('t-SNE 1')
    ax.set_ylabel('t-SNE 2')
    ax.legend(loc='upper right')
    # Show the plot​

    plt.show()

def plot_decision_boundary(clf, X, y,marker,xlabel,ylabel, label):
    # Create a mesh grid to plot the decision boundary
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the class labels for the mesh grid
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    custom_cmap = ListedColormap(['red', 'blue', 'orange'])
    # Plot the decision boundaries and the data points
    plt.contourf(xx, yy, Z,  alpha=0.8,cmap=custom_cmap)
    plt.scatter(X[:, 0], X[:, 1], c=y,  marker=marker ,cmap=custom_cmap, edgecolors='k', label=y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(label+'Decision boundaries')
    plt.show()

def getAccuracy(model, x, y):
    return model.score(x,y)*100

class_names = list(np.unique(Y))
class_names

def main():
    class_names = list(np.unique(Y))
    plot_tsne(X, Y, class_names)
  
    model = svm.SVC()
    model.fit(X, Y)
    print('Accuracy of model: {:.2f}%'.format(getAccuracy(model, X_test, y_test)))

    y_true, y_pred = y_test, model.predict(X_test)
    print('\nClassification Report:\n')
    print(classification_report(y_true, y_pred))
    
    plot_decision_boundary(model, X, Y,'o','X Training data','y Training data', 'OVR training ')

    plot_decision_boundary(model, X_test, y_test,'^','X Training data','y Training data', 'OVR Testing ')

    print('\nConfusion Matrix:\n')
    print(confusion_matrix(y_true, y_pred))

    ConfusionMatrixDisplay.from_estimator(model, X, Y)
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)

if __name__ == '__main__':
    main()

"""**(b) One VS Rest**"""

one_hot_encoded_data = pd.get_dummies(Y, columns = class_names)
y_Class0 = one_hot_encoded_data.iloc[:, 0:1].values
y_Class1 = one_hot_encoded_data.iloc[:, 1:2].values
y_Class2 = one_hot_encoded_data.iloc[:, 2:3].values
Classes = np.array((y_Class0,y_Class1,y_Class2))
print(one_hot_encoded_data)

binary_classifiers = []
for class_label in class_names:
    model = svm.SVC(kernel = 'linear',probability=True)
    model.fit(X, Classes[class_label])
    binary_classifiers.append(model)
  
y_predTrn = []
j=0
for model in binary_classifiers:
    y_pred_binary = model.predict(X)
    y_pred_class = (y_pred_binary == 1).astype(int)
    plot_decision_boundary(model, X, Y,'^','X Training data','y Training data', 'OVR class '+str(j)+' Testing ')
    y_predTrn.append(y_pred_class)
    
    accuracy_train =accuracy_score(y_pred_binary, Y)
    print("Accuracy: {:.2f}".format(accuracy_train))
    j=j+1

y_predTst = []
i=0
for model in binary_classifiers:
    
    y_pred_binary = model.predict(X_test)
    y_pred_class = (y_pred_binary == 1).astype(int)
    plot_decision_boundary(model, X_test, y_test,'^','X Testing data','y Testing data', 'OVR class '+str(i)+' Testing ')
    y_predTst.append(y_pred_class)
    accuracy_test1 =accuracy_score(y_test, y_pred_binary)
    print("Accuracy: {:.2f}".format(accuracy_test1))
    i= i +1

i=0
for model in binary_classifiers:
    print(f'\nConfusion Matrix: class {i}\n')
    ConfusionMatrixDisplay.from_estimator(model, X, Y)
    i+=1
i=0
for model in binary_classifiers:
    print(f'\nConfusion Matrix: class {i}\n')
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
    i+=1

y_pred_ovr_trn = [max(range(0,len(class_names)), key=lambda i: y_predTrn[i][idx]) for idx in range(len(X))]

y_pred_ovr = [max(range(0,len(class_names)), key=lambda i: y_predTst[i][idx]) for idx in range(len(X_test))]

accuracy_trn = accuracy_score(Y, y_pred_ovr_trn)
print("Accuracy Training: {:.2f}".format(accuracy_trn))
accuracy_test = accuracy_score(y_test, y_pred_ovr)
print("Accuracy: {:.2f}".format(accuracy_test))

# binary_classifiers = []
# for class_label in class_names:
#     model = svm.SVC(probability=True)
#     model.fit(X, Classes[class_label])
#     binary_classifiers.append(model)
  
# y_predTrn = []
# for model in binary_classifiers:
#     y_pred_binary = model.predict(X)
#     y_pred_class = (y_pred_binary == 1).astype(int)
#     plot_decision_boundary(model, X, Y,'^','X Training data','y Training data', 'OVR training '+str(j)+' Testing ')
#     y_predTrn.append(y_pred_class)

# y_predTst = []
# for model in binary_classifiers:
#     y_pred_binary = model.predict(X_test)
#     y_pred_class = (y_pred_binary == 1).astype(int)
#     plot_decision_boundary(model, X_test, y_test,'^','X Training data','y Training data', 'OVR training '+str(j)+' Testing ')
#     y_predTst.append(y_pred_class)

# for model in binary_classifiers:
#     ConfusionMatrixDisplay.from_estimator(model, X, Y)

# for model in binary_classifiers:
#     ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap= custom_cmap)

# y_pred_ovr_trn = [max(range(0,len(class_names)), key=lambda i: y_predTrn[i][idx]) for idx in range(len(X))]

# y_pred_ovr = [max(range(0,len(class_names)), key=lambda i: y_predTst[i][idx]) for idx in range(len(X_test))]

# accuracy_trn = accuracy_score(Y, y_pred_ovr_trn)
# print("Accuracy Training: {:.2f}".format(accuracy_trn))
# accuracy_test = accuracy_score(y_test, y_pred_ovr)
# print("Accuracy: {:.2f}".format(accuracy_test))

#Perceptron
clf = Perceptron(penalty='l1',  alpha=0.0049,tol=1e-3, random_state=0)
clf.fit(X, Y)
clf.score(X, Y)

binary1_classifiers = []
for class_label in class_names:
    clf = Perceptron()
    clf.fit(X, Classes[class_label])
    binary1_classifiers.append(clf)
j=0
y_predPTrn = []
for clf in binary1_classifiers:
    y_pred_binary = clf.predict(X)
    y_pred_class = (y_pred_binary == 1).astype(int)
    plot_decision_boundary(clf, X, Y,'^','X Training data','y Training data', 'Perceptron Class '+str(j)+' Training ')
    y_predPTrn.append(y_pred_class)
    j+=1
j=0
y_predPTest = []
for clf in binary1_classifiers:
    y_pred1_binary = clf.predict(X_test)
    y_pred_class1 = (y_pred1_binary == 1).astype(int)
    plot_decision_boundary(clf, X_test, y_test,'^','X Testing data','y Testing data', 'Perceptron class '+str(j)+' Testing ')
    y_predPTest.append(y_pred_class1)
    j+=1

for model in binary_classifiers:
    ConfusionMatrixDisplay.from_estimator(clf, X, Y)

for model in binary_classifiers:
    ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)

y_pred_ovr_trn = [max(range(0,len(class_names)), key=lambda i: y_predTrn[i][idx]) for idx in range(len(X))]

accuracy_trn = accuracy_score(Y, y_pred_ovr_trn)
print("Accuracy Training: {:.2f}".format(accuracy_trn))

y_pred_ovr = [max(range(0,len(class_names)), key=lambda i: y_predPTest[i][idx]) for idx in range(len(X_test))]

accuracyP = accuracy_score(y_test, y_pred_ovr)
print("Accuracy: {:.2f}".format(accuracyP))

svm_predictions=[]
for classifier in binary_classifiers:
  svm_predictions.append(classifier.predict_proba(X_test)[:,1])
svm_predictions
aggregated_labels = np.argmax(svm_predictions, axis=0)
aggregated_labels
confusion_mat = confusion_matrix(y_test, aggregated_labels)

confusion_mat

calibrated_classifier=[]
for classifier in binary1_classifiers:
  calibrated_classifier.append(CalibratedClassifierCV(classifier, cv='prefit', method='sigmoid'))
  calibrated_classifier[-1].fit(X, Y)

predicted_labels = []
for classifier1 in calibrated_classifier:
  # Step 5: Predict Probabilities using the Calibrated Perceptron
  probabilities = classifier1.predict_proba(X_test)
  predicted_label = classifier1.predict(X_test)
  predicted_labels.append(classifier1.predict_proba(X_test)[:,1])

aggregated1_labels = np.argmax(predicted_labels, axis=0)
aggregated1_labels

confusion_mat1 = confusion_matrix(y_test, aggregated1_labels)

confusion_mat

#confusion matrix for SVM aggrigated results
fig, ax = plt.subplots()

im = ax.imshow(confusion_mat, cmap=custom_cmap)
cbar = ax.figure.colorbar(im, ax=ax)

ax.set_xlabel('Predicted')
ax.set_ylabel('True')
ax.set_title('Confusion Matrix')
ax.set_xticks(np.arange(len(class_names)))
ax.set_yticks(np.arange(len(class_names)))

for i in range(len(class_names)):
    for j in range(len(class_names)):
        text = ax.text(j, i, confusion_mat[i, j], ha="center", va="center", color="black")

plt.tight_layout()
plt.show()

fig2, ax2 = plt.subplots()

im1 = ax2.imshow(confusion_mat1, cmap=custom_cmap)
cbar = ax2.figure.colorbar(im1, ax=ax2)

ax2.set_xlabel('Predicted')
ax2.set_ylabel('True')
ax2.set_title('Confusion Matrix')
ax2.set_xticks(np.arange(len(class_names)))
ax2.set_yticks(np.arange(len(class_names)))

for i in range(len(class_names)):
    for j in range(len(class_names)):
        text = ax2.text(j, i, confusion_mat1[i, j], ha="center", va="center", color="black")

plt.tight_layout()
plt.show()

agg_percept_model = svm.SVC()
agg_percept_model.fit(X_test, aggregated1_labels)
plot_decision_boundary(agg_percept_model,X_test, y_test,'^','X Training data','y Training data', '')

agg_svm_model = svm.SVC()
agg_svm_model.fit(X_test, aggregated_labels)
plot_decision_boundary(agg_svm_model,X_test, y_test,'^','X Training data','y Training data', '')

model_refined = svm.SVC(max_iter = 10 , decision_function_shape = 'ovo', cache_size = 500)
model_refined.fit(X, Y)
print('Accuracy of model: {:.2f}%'.format(getAccuracy(model_refined, X_test, y_test)))

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
#from mlxtend.evaluate import bias_variance_decomp
from sklearn import clone
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import Ridge, Lasso, LassoLarsIC
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.utils import check_random_state, shuffle

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import warnings

warnings.filterwarnings('ignore')

np.random.seed(42)

def load_dataset():
    dataset = pd.read_csv("car_evaluation.csv",header=None)
    mapping = {
    'low': '0',
    'med': '1',
    'high': '2',
    'vhigh': '3',
    'more': '4',
    '5more': '5',
    'small': '0',
    'big': '2',
    'unacc': '0',
    'good': '1',
    'vgood': '2',
    'acc': '3'
    }
    dataset.replace(mapping, inplace=True)
    dataset=dataset.astype(int)


    shuffled = dataset.sample(frac=1, random_state=42)   
    train_data, remaining_data = train_test_split(shuffled, train_size=1000, random_state=42)
    val_data, test_data = train_test_split(remaining_data, train_size=300, random_state=42)
    print("All set size:", len(shuffled))
    print("Training set size:", len(train_data))
    print("Validation set size:", len(val_data))
    print("Testing set size:", len(test_data))

    return train_data, val_data, test_data



Train,Val, Test =load_dataset ()

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
X1 = Test.iloc[:, :-1]
Y1 = Test.iloc[:, -1]
X2 = Val.iloc[:, :-1]
Y2 = Val.iloc[:, -1]
Training_size = 1000
neigh=[]
test_acc=[]
val_acc =[]
x_axis_val=[]
for i in range(1, 11):
    s = i / 10.0
    x_axis_val.append(s)
    if (s<1):
        Training_portion , f= train_test_split(Train, train_size=(int(Training_size*s)))
    else:
        Training_portion=Train

    X = Training_portion.iloc[:, :-1]
    Y = Training_portion.iloc[:, -1]
    neigh.append( KNeighborsClassifier(n_neighbors=2, algorithm = 'auto'))
    neigh[-1].fit(X,Y)
    y_pred1 =neigh[-1].predict (X1)
    test_acc.append(accuracy_score(Y1, y_pred1))
    print(f"The Testing Accuracy of Knn at {s} of training:", test_acc[-1])
    y_pred2 =neigh[-1].predict (X2)
    val_acc.append(accuracy_score(Y2, y_pred2))
    print(f" Validation Accuracy of Knn at {s} of training:", val_acc[-1])

x = x_axis_val
y1 =test_acc
y2 =val_acc
df = pd.DataFrame({'constant':1, 'x':x, 'y':y1})
df2 = pd.DataFrame({'constant':1, 'x':x, 'y':y2})
df.head()
sns.regplot(x='x', y='y', data = df, label='Testing Accuracy')
sns.regplot(x='x', y='y', data = df2, label='Validation Accuracy ')
plt.xlabel('The portion of the training set')
plt.ylabel('The accuracy score')
plt.legend()
plt.show()

neighk=[]
test_acck=[]
val_acck =[]
x_axis_valxx=[]
max_test =0
max_test_idx=0
max_val =0
max_val_idx=0

for i in range(1, 11):
    x_axis_valxx.append(i)
    Training_portion=Train

    X = Training_portion.iloc[:, :-1]
    Y = Training_portion.iloc[:, -1]
    neighk.append( KNeighborsClassifier(n_neighbors=i, algorithm = 'auto'))
    neighk[-1].fit(X,Y)
    y_pred1 =neighk[-1].predict (X1)
    test_acck.append(accuracy_score(Y1, y_pred1))
    print(f"The Testing Accuracy of Knn at k = {i} :", test_acck[-1])
    y_pred2 =neighk[-1].predict (X2)
    val_acck.append(accuracy_score(Y2, y_pred2))
    print(f"Validation Accuracy of Knn at k = {i} :", val_acck[-1])
    if max_test < test_acck[-1] :
      max_test = test_acck[-1]
      max_test_idx=i     
    if max_val < val_acck [-1]:
      max_val = val_acck[-1]
      max_val_idx=i 

print(max_test)
print(max_test_idx)
print(max_val)
print(max_val_idx)

from sklearn.linear_model import LinearRegression
x2 = x_axis_valxx
y3 =test_acck
y4 =val_acck

plt.plot(x2, y3, color='blue', label='Testing Accuracy Data')

plt.plot(x2, y4, color='red', label='Validation Accuracy Data')

plt.xlabel('No. of KNNeighbors')
plt.ylabel('The accuracy score')
plt.legend()
plt.show()

