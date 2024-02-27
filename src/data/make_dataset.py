import bibtexparser
import pandas as pd
import json
import typing
import requests

# import dataset and drop not relevant columns

with open('../../data/external/records_extended.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

records_df = pd.DataFrame(bib_database.entries)
records_df.dropna(subset="literature_review", inplace=True)

top_8 = ["European Journal of Information Systems", "Information Systems Journal", "Information Systems Research", "Journal of AIS", "Journal of Information Technology", "Journal of MIS", "Journal of Strategic Information Systems", "MIS Quarterly"]

df = records_df.loc[records_df['journal'].isin(top_8)]

df = df[df.prescreen_exclusion != "complementary material"]
df = df[df.title != "editorial"]
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
    
    if not pd.isna(row.doi):
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
        print(references)
        new_column.append(references)

df.insert(loc=len(df.columns), column="references", value=new_column)

df.drop(['language', 'url', 'pages', 'number', 'volume', 'year', 'journal', 'author', 'ENTRYTYPE', 'doi', 'crossmark-restriction', 'man_prep_hints', 'keywords'], axis = 1, inplace = True)

df.to_csv("../../data/interim/data.csv", index=False)


