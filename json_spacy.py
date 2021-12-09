# Convert json file to spaCy format.
import logging
import json
import pickle


def json_spacy_format(input_file, output_file):
    try:
        training_data = []
        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # print(line)
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                # only single point in text annotations
                point = annotation['points'][0]
                labels = annotation['label']
                # handles both list of lables and single label
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    entities.append((point['start'], point['end'] + 1, label))

            training_data.append((text, {"entities": entities}))

        # print(training_data)

        with open(output_file, 'wb') as fp:
            pickle.dump(training_data, fp)
            print("Data is dumped inside the output. Please check output file")

    except Exception as e:
        logging.exception("Unable to process " + input_file + "\n" + "error = " + str(e))
        return None


json_spacy_format('data.json', 'data_spacy_format.json')
