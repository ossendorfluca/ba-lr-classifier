import bibtexparser
import pandas as pd

with open('../../data/external/records.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

records_df = pd.DataFrame(bib_database.entries)

records_df = records_df[records_df['literature_review'].isin(["yes"])]

top_8 = ["European Journal of Information Systems", "Information System Journal", "Information System Research", "Journal of AIS", "Journal of Information Technology", "Journal of MIS", "Journal of Strategic Information Systems", "MIS Quarterly"]

records_top_8 = records_df.loc[records_df['journal'].isin(top_8)]



records_top_8.drop(['colrev.dblp.dblp_key', 'colrev_pdf_id', 'colrev_data_provenance', 'colrev_masterdata_provenance', 'colrev_status', 'colrev_origin', 'colrev.semantic_scholar.id', 'pdf_processed', 'prescreen_exclusion', 'note', 'fulltext', 'link', 'file', 'cited_by', 'screening_criteria', 'ID'], axis=1, inplace=True)





