#import joblib
from movierecommend import  recommend_course
#recommend_course = joblib.load('finalized_model.sav')
#print(joblib.load('finalized_model.sav'))
ans1 = recommend_course('The Complete 2020 Web Development Bootcamp', num_of_rec=3)
print(ans1)
