# Spacy_NER
-- Using ScaPy package to train and test a model to identify named entities

Requirements:

Pycharm IDE

Install pickle, spacy packages

1)	Saved the dataset given into .tsv file  ----  filename: data.tsv
2)	Convert the .tsv into json format  
  
	Run the file  --- tsv_to_json.py

3)	Now from json we need the json format which Spacy Library could understand. So again converting accordingly into spacy json format 

  
To convert, run the following

 Run the file -----   json_spacy.py

After this you will be getting    “ data_spacy_format.json “  file as output


4)	Now train and test the model by giving “ data_spacy_format.json “  as input to Trained_Data

Run the file = train_test_model.py

the stored model will be stored inside Path directory

For testing please change the  “input string” and try


All the .py files and .tsv files and .json files have been uploaded in Git




