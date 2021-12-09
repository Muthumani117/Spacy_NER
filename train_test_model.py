# train the model and next is test the model
from __future__ import unicode_literals, print_function
import pickle
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example

# Add the labels according to our dataset
LABEL = ['B-Cuisine', 'B-Dish', 'B-Hours', 'B-Location', 'B-Price', 'B-Rating', 'B-Restaurant_Name', 'I-Amenity',
         'I-Cuisine', 'I-Dish', 'I-Hours', 'I-Location', 'I-Price', 'I-Rating', 'I-Restaurant_Name', 'O' ]


def train_model(model=None, new_model_name='new_model', output_dir='Path', n_iter=10):
    """Setting up the pipeline and entity recognizer, and training the new entity."""
    if model is None:
        nlp = spacy.blank('en')  # create blank Language class always while training this will be done
        print("Created blank 'en' model")

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe('ner', last=True)

    for i in LABEL:
        ner.add_label(i)   # Add new entity labels to entity recognizer

    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.entity.create_optimizer()

    # Get names of other pipes to disable them during training to train only NER
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)

                example = []
                # Update the model with iterating each text
                for i in range(len(texts)):
                    doc = nlp.make_doc(texts[i])
                    example.append(Example.from_dict(doc, annotations[i]))
                nlp.update(example, sgd=optimizer, drop=0.35,
                           losses=losses)
            print('Losses', losses)

    # Save model in separate Path
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)


def test_model(model, test_string):
    if model is not None:
        nlp = spacy.load(model)  # load existing spacy model
        print("Loaded model '%s'" % model)
        doc2 = nlp(test_string)
        for entities in doc2.ents:
            print(entities.label_, entities.text)


# First Load training data
input_file = 'data_spacy_format.json'
with open(input_file, 'rb') as fp:
    TRAIN_DATA = pickle.load(fp)

train_model(model=None, new_model_name='new_trained_model', output_dir='Path', n_iter=10)

input_string = "outdoor live music lunch serves restaurant bakery cuisine go play meet"
# test_model(output_dir, input_strings)
test_model('Path', input_string)         # we have saved the trained model as Path. Change test_string to see different output

