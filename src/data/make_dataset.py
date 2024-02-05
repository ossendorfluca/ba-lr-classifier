import bibtexparser
import pandas as pd
import json
import typing
import requests

# import dataset and drop not relevant columns

with open('../../data/external/records.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

records_df = pd.DataFrame(bib_database.entries)
records_df.dropna(subset="literature_review", inplace=True)

top_8 = ["European Journal of Information Systems", "Information System Journal", "Information System Research", "Journal of AIS", "Journal of Information Technology", "Journal of MIS", "Journal of Strategic Information Systems", "MIS Quarterly"]

df = records_df.loc[records_df['journal'].isin(top_8)]

df.drop(['colrev.dblp.dblp_key', 'colrev_pdf_id', 'colrev_data_provenance', 'colrev_masterdata_provenance', 'colrev_status', 'colrev_origin', 'colrev.semantic_scholar.id', 'pdf_processed', 'prescreen_exclusion', 'note', 'fulltext', 'link', 'file', 'cited_by', 'screening_criteria', 'ID'], axis=1, inplace=True)
df.reset_index(inplace=True, drop=True)
df["literature_review"].replace(to_replace="yes", value=1, inplace=True)
df["literature_review"].replace(to_replace="no", value=0, inplace=True)
df.astype({"literature_review": int})

# add references column

api_url = "https://opencitations.net/index/coci/api/v1/references/"

new_column = []

for index, row in df.loc[:, ["doi"]].iterrows():
    
    references = []

    url = f"{api_url}{row.doi}"

    # headers = {"authorization": "YOUR-OPENCITATIONS-ACCESS-TOKEN"}
    headers: typing.Dict[str, str] = {}
    ret = requests.get(url, headers=headers, timeout=300)
    try:
        items = json.loads(ret.text)
        for item in items:
            references.append(item["cited"])
    except json.decoder.JSONDecodeError:
        print(f"Error retrieving citations from OpenCitations for DOI: {row.doi}")
    if len(references) == 0:
        new_column.append(None)
    else:
        new_column.append(references)

df.insert(loc=len(df.columns), column="references", value=new_column)

df.to_csv("../../data/interim/data.csv", index=False)

# feature preparation/engineering

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
