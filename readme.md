# An Empirical Study of IR and LDA-based Topic Modelling Approach for Duplicate Bug Detection


## Contributors
- Prachi Kabtiyal <pr522601@dal.ca>
- Vignesh Panemangalore Nayak <vg866663@dal.ca>
- Krishna Sanjaybhai Jadav <kr447707@dal.ca>


### Artifacts
The following table shows the artifacts, their description, organization and file structures.

| Artifact                  | Description | Organization       | File Structure                           |
|:-----------------------|:--------|:-----------------------|:-----------------------------------------|
| Eclipse LDA Topic Model Trained with 20, 50, 80, 100, 120, 140 topics | This is the pickle file created during the creation of topic model using eclipse bug reports | /ldamodel/eclipse-{number of topics}-ldamallet.pkl | Format of the file - pickle (.pkl) |
| Mozilla Firefox LDA Topic Model Trained with 20, 50, 80, 100, 120, 140 topics | This is the pickle file created during the creation of topic model using mozilla firefox bug reports | /ldamodel/mozilla-{number of topics}-ldamallet.pkl | Format of the file - pickle (.pkl) |
| Raw bug reports of Mozilla firefox | These bug reports are used as dataset to train LDA Topic model and run BM25 | /data/raw/mozilla.csv | csv file with headers- Issue_id,Priority,Component,Duplicated_issue,Title,Description,Status,Resolution,Version,Created_time,Resolved_time |
| Raw bug reports of eclipse platform | These bug reports are used as dataset to train LDA Topic model and run BM25 | /data/raw/eclipse.csv | csv file with headers- Issue_id,Priority,Component,Duplicated_issue,Title,Description,Status,Resolution,Version,Created_time,Resolved_time |
| Normalized bug reports of eclipse platform | These bug reports are created after appling data preprocessing on the raw bug reports | /data/normalized/eclipse-norm-data.csv | csv file with headers- issue_id,report |
| Normalized bug reports of mozilla firefox | These bug reports are created after appling data preprocessing on the raw bug reports | /data/normalized/mozilla-norm-data.csv | csv file with headers- issue_id,report |
| Test dataset - eclipse | The bug reports using which the topic model is validated | /data/eclipse-test.csv | csv file with headers- issue_id,Duplicate |
| Test dataset - mozilla firefox | The bug reports using which the topic model is validated | /data/mozilla-test.csv | csv file with headers- issue_id,Duplicate |
| BM25- Top-K scores with bug report ids for eclipse | It stores the bm25 performance results in terms of Top-K | /score_data/eclipse-bm25-{K}-score.csv | csv file with headers- original,duplicate, original being the bug report id and duplicates are the dictionary of top-k bug report and their similarity score |
| BM25- Top-K scores with bug report ids for mozilla | It stores the bm25 performance results in terms of Top-K | /score_data/mozilla-bm25-{K}-score.csv | csv file with headers- original,duplicate, original being the bug report id and duplicates are the dictionary of top-k bug report and their similarity score |
| Top-K score for Eclipse- LDA Topic Modelling for #topics  | It stores the performance results of lda model when trained for #topics in terms of Top-K | /score_data/eclipse-lda-{topics}{K}-score.csv | csv file with headers- original,duplicate, original being the bug report id and duplicates are the dictionary of top-k bug report and their similarity score |
| Top-K score for Mozilla- LDA Topic Modelling for #topics  | It stores the performance results of lda model when trained for #topics in terms of Top-K | /score_data/mozilla-lda-{topics}{K}-score.csv | csv file with headers- original,duplicate, original being the bug report id and duplicates are the dictionary of top-k bug report and their similarity score |
| Top-K score for eclipse- LDA Topic Modelling for #topics + BM25  | It stores the performance results of lda model when trained for topics combined with BM25 in terms of Top-K | /score_data/eclipse-bmlda--{topics}-{K}-score.csv | csv file with headers- original,duplicate, original being the bug report id and duplicates are the dictionary of top-k bug report and their similarity score |
| Top-K score for mozilla- LDA Topic Modelling for #topics + BM25  | It stores the performance results of lda model when trained for topics combined with BM25 in terms of Top-K | /score_data/mozilla-bmlda--{topics}-{K}-score.csv | csv file with headers- original,duplicate, original being the bug report id and duplicates are the dictionary of top-k bug report and their similarity score |


### Repository Directory Structure
 - **src/bm25/**: This folder contains the python program for bm25 search.
 - **src/combined/**: This folder contains execution of combining the similarity scores of IR and Topic Model searches.
 - **src/data_preprocessing/**: This folder contains data normalizing methods.
 - **src/performance_evaluator/**: This folder contains executable for calculating the performance of the searches based on Top-K.
 - **src/topic_model/**: This folder contains the implementation files of topic model creation and search.
 - **src/*.py**: These are the python executable numbered files that are to be executed in the order of the number assigned to them.
 - **requirements.txt**: It contains all the python libraries to be installed for the project.


### Operations / Features
1. Implementation of BM25 search model: An IR model- BM25 is implemented trained using the dataset (excluding the test issue ids)
2. Implementation of LDA-based Topic Model: Topic model creation and calculation of similarity score using Jensen Shannon Divergence
3. Top-K: It is a metric used for performance analysis of the two search engines
4. Combined IR + Topic Modelling: The prototype combines the similarities of the two search engines and then calculate the Top-k for the combined technique
5. Data preprocessing module does- tokenization, stopword removal, lemmatization, stemming and duplicate removal

### System Requirements
1. JDK 11.0 and above
2. Python 3.9 and above
3. mallet 2.0.8_1
4. Python libraries: nltk, pandas, numPy, gensim
5. Git


### Installation Details
Clone the repository by using the following command.
> $ git clone https://git.cs.dal.ca/kabtiyal/csci6308-py-empirical-study-on-duplicate-bug-detection.git

If you don't have git, please install git first using following commands.
> $ sudo apt-get update <br />
> $ sudo apt-get install git <br />

Open the project in an IDE- (Recommended Pycharm and Visual Studio Code)

Update mallet's path according to your local machine
> Go to "src/topic_model/modelling.py". Update the mallet's path in "mallet_abs_path" variable.


Select a project name for which you want to run the duplicate bug detection. Let's say project_name = "bluesky"

#### Follow the below steps to attain final output

- Place bluesky.csv file containing the bug reports in "/data/raw/ folder". It should contain "Issue_id", "Description", "Title" in the header. Case Sensitive.
- Place the dataset for testing in "/data/" folder. The name of the file should be "bluesky-test.csv" with headers- issue_id,Duplicate. Please see artifacts for reference.
- In terminal change directory to src folder.
- Update data_preprocessing_runner.py with project_name "bluesky" and run it.
- "bluesky-norm-data.csv" will be generated in the "../data/normalized/" folder.
- In the same directory as in step 3, update topic_model_runner.py with project_name "bluesky" and run it.
- "bluesky-{NUM_TOPICS}-ldamallet.pkl will be generated in the "../ldamodel/" folder.
- "bluesky-dist-{NUM_TOPICS}.csv" is generated that stores the topic probability distribution for each bug report.
- In the same directtory as in step 3, update lda_search_runner.py with project_name "bluesky" and run it.
- "bluesky-lda-{NUM_TOPICS}-{TOPK}-score.csv" is created with headers, issue_id and duplicate (dictionary of duplicate id with their similarity score). Directory: "/score_date/"
- In the same directory as in step 3, update 4bm25_search_runner.py with project_name "bluesky" and run it.
- "bluesky-bm25-{TOPK}-score.csv" is created with headers, issue_id and duplicate (dictionary of duplicate id with their similarity score). Directory: "/score_date/"
- In the same directory as in step 3, update compute_combined_search.py with project_name "bluesky" and run it.
- "bluesky-bmlda-{NUM_TOPICS}-{TOPK}-score.csv" is created with headers, issue_id and duplicate (dictionary of duplicate id with their similarity score). Directory: "/score_date/"
- In the same directory as in step 3, update performance_runner.py with project_name "bluesky" and run it.
- The performance report in terms of Top-K of IR, Topic Model and Combined is generated in the console.

#### To replicate the results of our empirical study using the produced artifacts, run the following python file and the result scores will display on the console.

> Open the terminal at src <br />
> Run command "python performance_runner.py" <br />
> This will display performance of BM25, LDA-based topic model and combined model in terms of MRR and Top-K for both projects- eclipse and mozilla


### License & Copyright

Licensed under the [MIT License](LICENSE)

### Code Analysis Report
We generated the report using Pylint <br />
[Click here for the report](code_quality_analysis/report.txt)
