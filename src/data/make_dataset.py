import bibtexparser
import pandas as pd

# first modification of original dataset

with open('../../data/external/records.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

records_df = pd.DataFrame(bib_database.entries)
records_df.dropna(subset="literature_review", inplace=True)

top_8 = ["European Journal of Information Systems", "Information System Journal", "Information System Research", "Journal of AIS", "Journal of Information Technology", "Journal of MIS", "Journal of Strategic Information Systems", "MIS Quarterly"]

records_top_8 = records_df.loc[records_df['journal'].isin(top_8)]

records_top_8.drop(['colrev.dblp.dblp_key', 'colrev_pdf_id', 'colrev_data_provenance', 'colrev_masterdata_provenance', 'colrev_status', 'colrev_origin', 'colrev.semantic_scholar.id', 'pdf_processed', 'prescreen_exclusion', 'note', 'fulltext', 'link', 'file', 'cited_by', 'screening_criteria', 'ID'], axis=1, inplace=True)
records_top_8.reset_index(inplace=True, drop=True)
records_top_8["literature_review"].replace(to_replace="yes", value=1, inplace=True)
records_top_8["literature_review"].replace(to_replace="no", value=0, inplace=True)
records_top_8.astype({"literature_review": int})
records_top_8.to_csv("../../data/interim/data.csv", index=False)

# feature preparation/engineering

df = pd.read_csv("../../data/interim/data.csv")

df.drop(['language', 'url', 'pages', 'number', 'volume', 'year', 'journal', 'author', 'ENTRYTYPE', 'doi'], axis = 1, inplace = True)

def addKeywordFeature(df, keyword, column, col_name):
    toAdd = []
    if column == "abstract":
        for index, row in df.loc[:, [column]].iterrows():
            if pd.isnull(df[column][index]):
                toAdd.append(0)
            elif keyword in row.abstract.lower():
                toAdd.append(1)
            else:
                toAdd.append(0)
        df.insert(loc=len(df.columns), column=col_name, value=toAdd)
    elif column == "title":
        for index, row in df.loc[:, [column]].iterrows():
            if pd.isnull(df[column][index]):
                toAdd.append(0)
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

df.drop(['title', 'abstract'], axis = 1, inplace = True)

df.to_csv("../../data/processed/data.csv", index=False)


