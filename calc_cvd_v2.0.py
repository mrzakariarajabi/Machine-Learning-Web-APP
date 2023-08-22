
# By H.R. Marateb
# Citation:
# Hassannejad R, Mansourian M, Marateb H, Mohebian MR, Gaziano TA, 
# Jackson RT, Angelantonio ED, Sarrafzadegan N. Developing Non-Laboratory 
# Cardiovascular Risk Assessment Charts and Validating Laboratory and 
# Non-Laboratory-Based Models. Glob Heart. 2021 Sep 2;16(1):58. 
# doi: 10.5334/gh.890. PMID: 34692382; PMCID: PMC8428313.

# Inputs:
# Age : Age in years
# DMHx: zero for no Diabetes and one for Diabetes
# WHR: Waist-to-hip ratio (Wait and hip must have the same unit before
# calculating their ratio
# SBP: Systolic blood pressure in mmHg
# sex: 1 for female and 0 for male
# sms2cat: 1 for smoker and 0 for non-smoker

# Outputs:
# risk1: the 10-year fatal and non-fatal CVD risk of teh person (in percent)
# risk2: the 10-year fatal and non-fatal CVD risk of a person with the same Age and sex, but without
# any other risk factors (in percent)
# str: The risk level message to display to the subject : 'low',
# 'intermediate', 'high' and 'very high'

from dis import show_code
import math 
import streamlit as st
from matplotlib import pyplot
from collections import ChainMap
import numpy as np

def main():
    ########                   Message title                   ########
    st.title("cardiovascular disease predictor")
    st.sidebar.title("This is a risk calculation system based on individual characteristics")
    st.markdown("Enter your features and specifications in sidebar:")
    st.sidebar.markdown ("Please do it carefully ")
    ########                   Sidebar peripheral                   ########
    if st.sidebar.radio("Sex",('Male','Female'),key='Sex') == 'Female':
         sex = 1
    else:
         sex = 0
    if st.sidebar.radio("Do you have Diabete?",('Yes','No'),key='Diabete') == 'No':
         DMHx= 0
    else:
         DMHx = 1
    sms2cat = st.sidebar.checkbox("Are you an Smoker?",False)
    Age = st.sidebar.slider("How old are you?", 35 , 91,key= 'Age')
    SBP = st.sidebar.slider("What about your blood pressure?", 120 , 180,key= 'SBP')
    WHR = st.sidebar.number_input("Waist to Hip Ratio", 0.85 ,1.20,step = 0.01,key='WHR')
    #Hip = st.sidebar.number_input("Hip Circumferences", 53 , 145 , step = 1 , key = 'hip')
    #waist = st.sidebar.number_input("Waist  Circumferences", 51 , 140 , step = 1 , key = 'waist')
    #WHR = Hip / waist
    ########                   Define function for Calculate Risk                  ########
    def calc_cvd_risk(Age , DMHx, WHR ,SBP,sex,sms2cat):
        if SBP >=120 and SBP <= 139:
              sbpcat2,sbpcat3,sbpcat4 = 1,0,0
        elif SBP >= 140 and SBP < 159:
             sbpcat2,sbpcat3 , sbpcat4 = 0,1,0
        elif (SBP >= 160):
             sbpcat2,sbpcat3,sbpcat4 = 0,0,1
        else :
             sbpcat2 , sbpcat3 , sbpcat4 = 0,0,0
        if sex :
            if WHR >=0.85 and SBP < 0.90 :
                 WHR2,WHR3,WHR4 = 1,0,0
            elif WHR >= 0.90 and WHR < 0.95:
                 WHR2,WHR3,WHR4 = 0,1,0
            elif WHR >= 0.95 :
                 WHR2,WHR3,WHR4 = 0,0,1
            else : #WHR < 0.85
                 WHR2,WHR3,WHR4 = 0,0,0
        else :
            if WHR >=1 and SBP < 1.05 :
                 WHR2,WHR3,WHR4 = 1,0,0
            elif WHR >= 1.05 and WHR < 1.10:
                 WHR2,WHR3,WHR4 = 0,1,0
            elif WHR >= 1.10 :
                 WHR2,WHR3,WHR4 = 0,0,1
            else : #WHR < 1
                 WHR2,WHR3,WHR4 = 0,0,0
         ###                        Define function to calculate risk           ###        
        def calc_risk(Age , DMHx,sbpcat2,sbpcat3,sbpcat4,sex,sms2cat,WHR2,WHR3,WHR4):
            f = 0.03823*(Age-50.69)+0.73001*(DMHx-0.07)+0.47524*(sbpcat2-0.3534)+ 0.79045*(sbpcat3-0.1268)+1.13051*(sbpcat4-0.0730)+ \
              (-0.32309)*(sex-0.51)+0.26560*(sms2cat-0.22)+ \
                0.10478*(WHR2-0.1291)+0.17986*(WHR3-0.1414)+0.29440*(WHR4-0.2384)
            A = math.exp(f)
            return 1-0.96303975**A                             
        risk1 = 100*calc_risk(Age,DMHx , sbpcat2,sbpcat3,sbpcat4,sex,sms2cat , WHR2,WHR3,WHR4)
        risk2 = 100*calc_risk(Age , 0,0,0,0,sex,0,0,0,0)
        if (risk1<5):
            str=':green[low] risk'
        elif (risk1>=5 and risk1<10):
            str=' :orange[intermediate] risk'
        elif (risk1>=10 and risk1<15):
            str=' :red[high] risk'
        else :
           str=' :red[very-high] risk'
        return risk1, risk2,str
    def Recommendations(DMHx , WHR, SBP, sms2cat):
         st.write(''':red[General Recommandation:]It is recommended for adults of all ages to strive for at least 150 - 300 min a week of moderate intensity or 75 - 150 min a week of vigorous intensity aerobic PA, or an equivalent combination to reduce all-cause mortality, CV mortality, and morbidity.\n
Patients at (very) high risk for CVD may be
encouraged to try to avoid long-term exposure
to regions with high air pollution.\n
It is recommended to eat fish, preferably fatty, at least once a week and restrict (processed) meat.\n
It is recommended to choose a more plant based food pattern, rich in fibre, that includes whole grains, fruits, vegetables, pulses, and nuts.\n
It is recommended to reduce salt intake to lower BP and risk of CVD.                                    
''')
         if(DMHx):
              st.write(''':red[ForDiabetes:]Patients with DM should follow guidelines for the general population for the recommended intakes of saturated fat, dietary cholesterol, and trans fat.In general, trans fats should be avoided.\n
Adjusting daily protein intake is not indicated in patients with DM
unless kidney disease is present, at which point less protein is
recommended. 
Vitamin or micronutrient supplementation to reduce the risk of DM
or CVD in patients with DM is :red[not] recommended.\n
Patients with pre-DM and DM should do two sessions per week of resistance exercise; pregnant women with DM should engage in regular moderate physical activity.\n                                                                    
It is recommended to choose a more plant-
based food pattern, rich in fibre, that includes
whole grains, fruits, vegetables, pulses, and
nuts.\n
Consumption of more than four cups of coffee per day was associated with a lower risk of CVD in Finnish patients with DM.
''') 
         if(SBP >= 150):
              st.write(''':red[For Hypertension:]
The BP goal is to target SBP to 130 mmHg and <130 mmHg if tolerated, but not <120 mmHg. In older people (aged >65 years), the SBP goal is to a range of 130 - 139 mmHg, It is recommended that target DBP is targeted to <80 mmHg, but not <70 mmHg.\n
We recommend sodium intake to be limited to approximately 2.0 g per day (equivalent to approximately 5.0 g salt per day) in the general population and to try to achieve this goal in all hypertensive patients.\n

Hypertensive men who drink alcohol should be advised to limit their consumption to 14 units per week and women to 8 units per week (1 unit is equal to 125 mL of wine or 250 mL of beer).\n
Eating a healthy balanced diet containing vegetables, legumes, fresh fruits, low-fat dairy products, wholegrains, fish, and unsaturated fatty acids (especially olive
oil), and to have a low consumption of red meat and saturated fatty
acids.\n                       
It is recommended to reduce salt intake to lower
BP and risk of CVD,
Also replacing saturated with
unsaturated fats will help  lower the risk of
CVD.''')
         if(WHR >= 0.95):
              st.write(''':red[Weight Recommandation:]It is recommended that overweight and obese people aim for a reduction in weight to reduce BP, dyslipidaemia, and risk of type 2 DM, thus improve their CVD risk profile.\n
Body-weight control is indicated to avoid obesity (BMI >30 kg/m2 or waist circumference >102 cm in men and >88 cm in women), as is aiming at healthy BMI (about 20–25 kg/m2) and waist circumference values (<94 cm in men and <80 cm in women) to reduce BP and CV risk.\n
Regular aerobic exercise (e.g. at least 30 min of moderate dynamic exercise on 5–7 days per week) is recommended.\n
Bariatric surgery for obese high-risk individuals
should be considered when lifestyle change does not result in maintained weight loss. 
''')
         if(sms2cat):
              st.write(''':red[For smoking:]All smoking of tobacco should be stopped, as tobacoo use is strongly and independently
                       causal of ASCVD\n
You can use nicotine replacement therapy,varenicline,and bupropion individually or in combination should 
                       be considered.''')                  
              
    try:
    ########                   Calculating                ########   
        if st.sidebar.button("Calculate",key='calculate'):
            risk1, risk2,str = calc_cvd_risk(int(Age), DMHx ,float(WHR) ,int(SBP) , sex, sms2cat)
            st.write("10-year fatal and non-fatal CVD risk :",'%.4f'%risk1)
            st.write("10-year fatal and non fatal without any other risk factors:",'%.4f'%risk2)
            st.write(str)
            data = {'10-year fatal and non-fatal CVD risk': risk1, '10-year fatal and non fatal without any other risk factors': risk2}
        
        if (sms2cat == True):
             risk3, risk4,str2 = calc_cvd_risk(int(Age), DMHx ,float(WHR) ,int(SBP) , sex, not(sms2cat))
             risk4 = -((risk1 - risk3)/risk1)*100
             st.write("Risk if you quit smoking :",'%.2f'%risk3,'(%.2f'%risk4,'%)')
             #st.write("risk2 :",risk2)
             st.write(str2)
             data =ChainMap(data, {'Risk if you quit Smoking':  risk3}) 
    
        if (DMHx == True):
             risk5, risk6,str3 = calc_cvd_risk(int(Age), not(DMHx) ,float(WHR) ,int(SBP) , sex, sms2cat)
             risk6 = -((risk1 - risk5)/risk1)*100
             st.write("Risk without diabete :", '%.2f'%risk5,'(%.2f'%risk6,'%)')
             #st.write("risk2 :",risk2)
             st.write(str3)
             data = ChainMap(data, {'Risk without diabete': risk5})
    
        if (WHR >= 0.95):
            risk7, risk8,str4 = calc_cvd_risk(int(Age), DMHx ,WHR-0.05 ,int(SBP) , sex, sms2cat)
            risk8 = -((risk1 - risk7)/risk1)*100
            st.write("Risk if you decrease 5 Percent of WHR : ",'%.2f'%risk7,'(%.2f'%risk8,'%)')
             #st.write("risk2 :",risk2)
            st.write(str4)
            data = ChainMap(data, {'Risk if you decrease 5 Percent of WHR': risk7})
        
        if (SBP >= 150):
            risk13, risk14,str7 = calc_cvd_risk(int(Age), DMHx ,WHR , SBP-20, sex, sms2cat)
            risk14 = -((risk1 - risk13)/risk1)*100
            st.write("Risk with lower Blood Pressure : ",'%.2f'%risk13,'(%.2f'%risk14,'%)')
             #st.write("risk2 :",risk2)
            st.write(str7)
            data = ChainMap(data, {'Risk with lower Blood Pressure': risk13})

        if (sms2cat == True and DMHx == True):
             risk9, risk10,str5 = calc_cvd_risk(int(Age), not(DMHx) ,float(WHR) ,int(SBP) , sex, not(sms2cat))
             risk10 = -((risk1 - risk9)/risk1)*100
             st.write('Risk without diabete and without smoking : ','%.2f'%(risk9),'(%.2f'%risk10,'%)')
             #st.write("risk2 :",risk2)
             st.write(str5)
             data = ChainMap(data, {'Risk without diabete and without smoking': risk9})
        
        if (sms2cat == True and DMHx == True and WHR >= 0.95 and SBP >= 150):
             risk11, risk12,str6 = calc_cvd_risk(int(Age), ~(DMHx) ,WHR-0.05 ,SBP-20 , sex, ~(sms2cat))
             risk12 = -((risk1 - risk11)/risk1)*100
             st.write("Risk without diabete and smoking and blood pressure decrease 5 Percent of WHR: ",'%.2f'%risk11,'(%.2f'%risk12,'%)')
             #st.write("risk2 :",risk2)
             st.write(str6)
             data = ChainMap(data, {'Risk without diabete and  smoking and blood presuure and decrease 5 Percent of WHR': risk11})
         ############                   Plotting                  ########
        group_data = list(data.values())
        group_names = list(data.keys())
        group_mean = np.mean(group_data)
        fig, ax = pyplot.subplots()
        ax.set_facecolor("black")
        ax.tick_params(axis='y', colors='white')
        fig.patch.set_facecolor('black')
        dis = ax.barh(group_names, group_data ,color = 'maroon', edgecolor = 'crimson')
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)          
    except:
        #st.error("Need an Recommendation? Callculating? Check the sidebar!")
        st.stop()
         ####                 Recommendations           #######
    finally:
         if st.button("Recommendation", key='recommend'):
               st.empty()
               Recommendations(DMHx, WHR, SBP, sms2cat)    
   
if __name__ == '__main__':
    main() 