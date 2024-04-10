Bachelor's Thesis - Design of a machine-learning classifier for research papers: Identifying literature reviews
==============================

General Information
------------

This project is part of my bachelor's thesis "Design of a machine-learning classifier for research papers: Identifying literature reviews". The repository consists of the data used for training the model (can be found in the data folder) as well as the code produced for exploring the dataset, preprocessing the data, building the features and training as well as testing and evaluating the final models. The code consisting of eight Jupyter Notebooks can be found in the notebooks folder. The single notebooks are dependent on existing data produced by previous executions of the code, if the underlying dataset is changed, all files starting from 2-make_dataset.ipynb need to be executed consecutively. Further information about the code can be found in each Jupyter Notebook.

About The Thesis - Abstract
------------

This thesis explores the application of a machine learning classifier to predict literature reviews in information systems publications. As research becomes more accessible and scientific publications are growing exponentially, especially in a dynamically evolving field like information systems, literature screening requires an extensive amount of manual work. For many researchers, the type of method used in a paper is relevant for evaluating their suitability to be considered for a specific task, underlining the need for a classifier able to predict the utilized research method. The case of literature reviews is particularly important, as they give an overview of the current state of research and are therefore considered in various scopes of application. For my classifier, the highest F1 score of 44.8% was achieved with an SVM algorithm, thus pointing out the challenges of handling imbalanced datasets. SMOTE was implemented as an oversampling technique to balance out the dataset but did not produce the anticipated improvements. Finally, the underlying issue of insufficient transparency concerning research methodology in information systems papers is addressed, which is negatively impacting the identification of literature reviews.

--------

<p><small>The structure of this project is based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
