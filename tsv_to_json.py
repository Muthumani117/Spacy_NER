# convert .tsv file into .json format
import json
import logging


def tsv_to_json_format(input_path, output_path, unknown_label):
    try:
        f = open(input_path, 'r')  # input file
        fp = open(output_path, 'w')  # output file
        data_dict = {}
        annotations = []
        label_dict = {}
        s = ''
        start = 0
        sentence_start = 1   # initial value to check sentence begin
        for line in f:
            if len(line) == 1:
                sentence_start = 1  # if there is blank line, then it should loop to next line and go to else part
                continue
            if line[0:len(line) - 1] != '.\tO' and sentence_start == 0:
                entity, word = line.split()   # for our dataset first is entity second is word, it changes according to dataset
                s += word + " "
                if entity != unknown_label:
                    if len(entity) != 1:
                        d = {}
                        d['text'] = word
                        d['start'] = start
                        d['end'] = start + len(word) - 1
                        try:
                            label_dict[entity].append(d)
                        except:
                            label_dict[entity] = []
                            label_dict[entity].append(d)
                start += len(word) + 1
            else:
                sentence_start = 0   # again making here zero so that further lines will get into if part in next loop
                data_dict['content'] = s
                s = ''
                label_list = []
                for ents in list(label_dict.keys()):
                    for i in range(len(label_dict[ents])):
                        if label_dict[ents][i]['text'] != '':
                            list_var = [ents, label_dict[ents][i]]
                            for j in range(i + 1, len(label_dict[ents])):
                                if label_dict[ents][i]['text'] == label_dict[ents][j]['text']:
                                    di = {}
                                    di['start'] = label_dict[ents][j]['start']
                                    di['end'] = label_dict[ents][j]['end']
                                    di['text'] = label_dict[ents][i]['text']
                                    list_var.append(di)
                                    label_dict[ents][j]['text'] = ''
                            label_list.append(list_var)
                for entities in label_list:
                    label = {}
                    label['label'] = [entities[0]]
                    label['points'] = entities[1:]
                    annotations.append(label)
                data_dict['annotation'] = annotations
                annotations = []
                json.dump(data_dict, fp)  # dumping the format into the json file
                fp.write('\n')
                data_dict = {}
                start = 0
                label_dict = {}

    except Exception as e:
        logging.exception("Unable to process file" + "\n" + "error = " + str(e))
        return None


# tsv_to_json_format(input_path, output_path, unknown_label):
tsv_to_json_format("data.tsv", 'data.json', 'abc')
