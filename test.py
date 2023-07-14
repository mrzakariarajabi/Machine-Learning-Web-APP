import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay, roc_curve, auc, precision_recall_curve, PrecisionRecallDisplay


def main():
   st.title("Binary classification web App")
   st.sidebar.title("Binary Classification Web App")
   st.markdown("Are you mushrooms editble or poisonous ??")
   st.sidebar.markdown ("Are you mushrooms editble or poisonous ")
   
   ######################              load data                 ######################

   @st.cache_data(persist = True)
   def load_data():
       data = pd.read_csv('mushrooms.csv') 
       label = LabelEncoder()
       for col in data.columns:
           data[col] = label.fit_transform(data[col])
       return data
   
   ######################              split data                 ######################

   @st.cache_data(persist = True)
   def split(df):
       y = df['class'] 
       x = df.drop(['class'], axis=1)
       x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
       return x_train, x_test, y_train, y_test
   
    ######################              plot_metrics                 ######################
   def plot_metrics(metrics_list, predictions):
       if 'Cofusion Matrics' in metrics_list :
           st.subheader("Cofusion Matrics")
           #predictions =model.predict(X_test)
           cm = confusion_matrix(y_test, predictions)#, labels='x'
           disp = ConfusionMatrixDisplay(confusion_matrix=cm )#display_labels='y'
           disp.plot()
           #fig, ax = plt.subplots()
           st.pyplot()
           st.set_option('deprecation.showPyplotGlobalUse', False)
    #####################          ROC Curve          ###################
       if 'ROC Curve' in metrics_list :
           st.subheader("ROC Curve")
           #predictions =model.predict(X_test)
           fpr, tpr, thresholds = roc_curve(y_test, predictions)
           roc_auc = auc(fpr, tpr)
           disp = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc= roc_auc)# , estimator_name=class_names
           disp.plot()
           
           st.pyplot()
       if 'Precision-Recall Curve' in metrics_list :
           st.subheader("Precision-Recall Curve")
           #predictions =model.predict(X_test)
           precision, recall, _ = precision_recall_curve(y_test, predictions)
           disp = PrecisionRecallDisplay(precision=precision, recall=recall)
           disp.plot()
            ###############3 Precision-Recall Curve
           st.pyplot()
            
    ######################              set classifire                 ######################
   df = load_data()
   x_train, x_test, y_train, y_test = split(df)
   class_names = ['edible', 'poisonous']
   st.sidebar.subheader("Choose Classifier")
   classifire = st.sidebar.selectbox("Classifire", ("Support Vector Machine (SVM)","Logistic Regression", "Random Forest"))
   ######################              Support Vector Machine                 ######################
   if classifire == 'Support Vector Machine (SVM)':
       st.sidebar.subheader("Model Hyperparmeters")
       C = st.sidebar.number_input("C (Regulation number)", 0.01, 10.0, step=0.01, key='C')
       kernel = st.sidebar.radio("Kernel", ("rbf", "linear"), key='kernel')
       gamma = st.sidebar.radio("Gamma (Kernel Coefficient)", ("scale", "auto"), key='gamma')

       metrics = st.sidebar.multiselect("what metrics to plot?",('Cofusion Matrics', 'ROC Curve', 'Precision-Recall Curve'))
       if st.sidebar.button("Classify", key='classify'):
           st.subheader("Support Vector Machine (SVM) Results")
           model = SVC(C=C, kernel=kernel, gamma=gamma )
           model.fit(x_train, y_train)
           accuracy = model.score(x_test, y_test)
           y_pred = model.predict(x_test)
           st.write("Accuracy: ", accuracy.round(2))
           st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
           st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
           plot_metrics(metrics, y_pred)
######################              Logistic Regression                 ###################### 
   if classifire == 'Logistic Regression':
       st.sidebar.subheader("Model Hyperparmeters")
       C = st.sidebar.number_input("C (Regulation paramter)", 0.01, 10.0, step=0.01, key='C I.R')
       max_iter = st.sidebar.slider("Maximum number of iterations", 100, 500, key='max_iter')

       metrics = st.sidebar.multiselect("what metrics to plot?",('Cofusion Matrics', 'ROC Curve', 'Precision-Recall Curve'))

       if st.sidebar.button("Classify", key='classify'):
           st.subheader("Logistic Regression Results")
           model = LogisticRegression(C=C, max_iter=max_iter)
           model.fit(x_train, y_train)
           accuracy = model.score(x_test, y_test)
           y_pred = model.predict(x_test)
           st.write("Accuracy: ", accuracy.round(2))
           st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
           st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
           plot_metrics(metrics, y_pred)
######################              Random Forest                 ######################       
   if classifire == 'Random Forest':
       st.sidebar.subheader("Model Hyperparmeters")
       n_estimators = st.sidebar.number_input("C (Regulation paramter)", 100, 5000, step=10, key='n_estimators')
       max_depth = st.sidebar.number_input("The maximum depth of the tree", 1, 20, step=1,key='max_derth')
       bootstrap = st.sidebar.radio("bootstrap sample when building trees", (True, False),key='bootstrap')
       metrics = st.sidebar.multiselect("what metrics to plot?",('Cofusion Matrics', 'ROC Curve', 'Precision-Recall Curve'))

       if st.sidebar.button("Classify", key='classify'):
           st.subheader("Random Forest Results")
           model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap=bootstrap, n_jobs= -1)
           model.fit(x_train, y_train)
           accuracy = model.score(x_test, y_test)
           y_pred = model.predict(x_test)
           st.write("Accuracy: ", accuracy.round(2))
           st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
           st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
           plot_metrics(metrics , y_pred)



######################              show raw data                 ######################

   if st.sidebar.checkbox("show raw data", False):
       st.subheader("mushrooms data set (classification)")
       st.write(df)

   

if __name__ == '__main__':
    main()