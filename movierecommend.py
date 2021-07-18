import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

import joblib

df = pd.read_csv("turnskill courses.csv")
df['title']
dir(nfx)
df['clean_course_title'] = df['title'].apply(nfx.remove_stopwords)
df['clean_course_title'] = df['clean_course_title'].apply(nfx.remove_special_characters)
df[['title', 'clean_course_title']]
count_vect = CountVectorizer()
cv_mat = count_vect.fit_transform(df['clean_course_title'])
cv_mat.todense()
df_cv_words = pd.DataFrame(cv_mat.todense(), columns=count_vect.get_feature_names())
cosine_sim_mat = cosine_similarity(cv_mat)
course_indices = pd.Series(df.index, index=df['title']).drop_duplicates()
idx = course_indices['The Web Developer Bootcamp']
scores = list(enumerate(cosine_sim_mat[idx]))
sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
sorted_scores[1:]
selected_course_indices = [i[0] for i in sorted_scores[1:]]
selected_course_scores = [i[1] for i in sorted_scores[1:]]
recommended_result = df['title'].iloc[selected_course_indices]
rec_df = pd.DataFrame(recommended_result)
rec_df['similarity_scores'] = selected_course_scores


def recommend_course(title, num_of_rec=10):
    idx = course_indices[title]
    scores = list(enumerate(cosine_sim_mat[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    selected_course_indices = [i[0] for i in sorted_scores[1:]]
    selected_course_scores = [i[1] for i in sorted_scores[1:]]
    result = df['title'].iloc[selected_course_indices]
    rec_df = pd.DataFrame(result)
    rec_df['similarity_scores'] = selected_course_scores
    #print(rec_df.head(num_of_rec))
    return rec_df.head(num_of_rec)

#ans = recommend_course('The Complete 2020 Web Development Bootcamp', num_of_rec=10)
#print(ans)

#filename = 'finalized_model.sav'
#joblib.dump(recommend_course,filename)
