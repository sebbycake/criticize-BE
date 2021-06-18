import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_recommendations(df, column, value, cosine_similarities, limit):
    indices = pd.Series(df.index, index=df[column]).drop_duplicates()

    target_index = indices[value]

    cosine_similarity_scores = list(enumerate(cosine_similarities[target_index]))

    cosine_similarity_scores = sorted(cosine_similarity_scores, key=lambda x: x[1], reverse=True)
    cosine_similarity_scores = cosine_similarity_scores[1:limit+1]
 
    index = (x[0] for x in cosine_similarity_scores)
    scores = (x[1] for x in cosine_similarity_scores)    

    recommendation_indices = [i[0] for i in cosine_similarity_scores]

    recommendations = df[column].iloc[recommendation_indices]

    df = pd.DataFrame(list(zip(index, recommendations, scores)), 
                      columns=['index','recommendation', 'cosine_similarity_score'])
    return df


def get_json_data(all_articles, article_title):
    inter = dict(map(lambda x: (x["title"], x["content"]), all_articles))
    df = pd.DataFrame(list(inter.items()), columns = ["Title", "Content"])
    indices = pd.Series(df.index, index=df['Title']).drop_duplicates()
    content = df["Content"].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(content)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    limit = 4
    recommendations = get_recommendations(df, 
                                      'Title', 
                                      article_title, 
                                      cosine_similarities,
                                      limit)
    final_output = []
    for i in range(limit):
        inter = dict()
        curr_article = df.loc[recommendations['index'][i]]
        inter["title"] = curr_article["Title"]
        inter["content"] = curr_article["Content"]
        final_output.append(inter)
    return final_output


