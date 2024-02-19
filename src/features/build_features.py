from ast import literal_eval
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
import string
from sklearn.feature_selection import VarianceThreshold

# get interim data
df = pd.read_csv("../../data/interim/data.csv")



# fill nan-values for references with empty list
df.references.fillna("[]", inplace=True)



# change references type from string into array
df.references = df.references.apply(literal_eval)



# keyword-matching features

def addKeywordFeature(df, keyword, column, col_name):
    toAdd = []
    if column == "abstract":
        for index, row in df.loc[:, [column]].iterrows():
            if pd.isna(df[column][index]):
                toAdd.append(2)
            elif keyword in row.abstract.lower():
                toAdd.append(1)
            else:
                toAdd.append(0)
        df.insert(loc=len(df.columns), column=col_name, value=toAdd)
    elif column == "title":
        for index, row in df.loc[:, [column]].iterrows():
            if pd.isna(df[column][index]):
                toAdd.append(2)
            elif keyword in row.title.lower():
                toAdd.append(1)
            else:
                toAdd.append(0)
        df.insert(loc=len(df.columns), column=col_name, value=toAdd)

addKeywordFeature(df, "literature review", "title", "title_literaturereview")
addKeywordFeature(df, "literature review", "abstract", "abstract_literaturereview")
addKeywordFeature(df, "review", "title", "title_review")
addKeywordFeature(df, "review", "abstract", "abstract_review")
addKeywordFeature(df, "survey", "title", "title_survey")
addKeywordFeature(df, "survey", "abstract", "abstract_survey")
addKeywordFeature(df, "experiment", "title", "title_experiment")
addKeywordFeature(df, "experiment", "abstract", "abstract_experiment")
addKeywordFeature(df, "interview", "title", "title_interview")
addKeywordFeature(df, "interview", "abstract", "abstract_interview")
addKeywordFeature(df, "case study", "title", "title_casestudy")
addKeywordFeature(df, "case study", "abstract", "abstract_casestudy")
addKeywordFeature(df, "questionnaire", "title", "title_questionnaire")
addKeywordFeature(df, "questionnaire", "abstract", "abstract_questionnaire")
addKeywordFeature(df, "design science", "title", "title_designscience")
addKeywordFeature(df, "design science", "abstract", "abstract_designscience")



# method paper matching feature

# read in list of literature review method papers and extract dois
df_method_papers = pd.read_csv("../../data/external/lr-method-papers.csv", usecols=["doi"])
df_method_papers.dropna(inplace = True)
method_papers = df_method_papers['doi'].tolist()

reference_count = []

for index, row in df.loc[:, ["references"]].iterrows():
    counter = 0
    for doi in df["references"][index]:
        if doi in method_papers:
            counter += 1
    reference_count.append(counter)
    
df.insert(loc=len(df.columns), column="references_count", value=reference_count)




# text mining feature with bag of words

df.abstract.fillna("", inplace=True)
df.title.fillna("", inplace=True)

# clean text helper function
def clean_text(text):
    
    # lowercase
    text = text.lower()
    
    # remove punctuation and multiple spaces
    text = re.sub(
        f"[{re.escape(string.punctuation)}]", " ", text
    )
    text = " ".join(text.split())
    
    remove_digits = str.maketrans('', '', string.digits)
    text = text.translate(remove_digits)
    
    return text

# clean abstracts and titles
df["clean_abstracts"] = df.abstract.map(clean_text, na_action="ignore")
df["clean_titles"] = df.title.map(clean_text, na_action="ignore")

# count vectorizer for bag of words
bow_abstracts = CountVectorizer(ngram_range=(1,2), stop_words="english")
bow_titles = CountVectorizer(ngram_range=(1,2), stop_words="english")

# fit vocabulary
abstract_matrix = bow_abstracts.fit_transform(df.clean_abstracts)
title_matrix = bow_titles.fit_transform(df.clean_titles)

# variance threshold feature selection
selector = VarianceThreshold()
abstract_matrix = selector.fit_transform(abstract_matrix)
title_matrix = selector.fit_transform(title_matrix)

# convert sparse matrix into dataframe
df_abstracts = pd.DataFrame.sparse.from_spmatrix(abstract_matrix)
df_titles = pd.DataFrame.sparse.from_spmatrix(title_matrix)

# change column names to prepare for concat
df_titles.rename(columns=lambda x: str(x) + "_title", inplace=True)
df_abstracts.rename(columns=lambda x: str(x) + "_abstracts", inplace=True)

# concat all dataframes to single dataframe
df_final = pd.concat([df, df_titles, df_abstracts], axis=1)



# drop unnecessary columns
df_final.drop(['title', 'abstract', 'references', 'clean_titles', 'clean_abstracts'], axis = 1, inplace = True)



# save data as csv
df_final.to_csv("../../data/processed/data.csv", index=False)
