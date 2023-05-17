import re
import json
import codecs
import ast
import csv

from language_code import mbart50

# clean all tags from translated text and identify spans for each tags in translated text
def identify_tags(text):
    clean = re.compile('<.*?>')
    clean_texts = re.sub(clean, ' ', text)
    
    clean_text = ""
    for ix, char in enumerate(clean_texts):
        if char == " " and ix != 0 and clean_texts[ix-1] == " ":
            continue
        elif char == " " and ix < len(clean_texts)-1 and (clean_texts[ix+1] == "." or clean_texts[ix+1] == "?") :
            continue
        else:
            clean_text += char

    clean_text = clean_text.strip()
    opening_tags = ["<M>", "<A>", "<AN>", "<C>", "<CN>"]
    ix = 0
    tag_dict_ls = []
    while ix < len(text):
        if text[ix] == "<":
            tag = ""
            while text[ix] != ">" and ix < len(text):
                tag += text[ix]
                ix += 1
            tag += text[ix]
            if tag in opening_tags:
                ix += 1
                tag_string = ""
                while text[ix] != "<" and ix < len(text):
                    tag_string += text[ix]
                    ix += 1
                tag = tag[1:]
                tag = tag[:-1]

                if len(tag_string)==0:
                    continue

                while len(tag_string)>1 and tag_string[-1] == "→":
                    tag_string = tag_string[:-1]
                while len(tag_string)>1 and tag_string[-1] == ".":
                    tag_string = tag_string[:-1]
                while len(tag_string)>1 and tag_string[-1] == ",":
                    tag_string = tag_string[:-1]
                while len(tag_string)>1 and tag_string[-1] == " ":
                    tag_string = tag_string[:-1]
                
                start_index = clean_text.find(tag_string)
                end_index = start_index+len(tag_string)
                tag_dict = {
                    "end": end_index,
                    "label": tag,
                    "start": start_index
                }
                tag_dict_ls.append(tag_dict)   
        else:
            ix += 1
    
    # print(json.dumps(tag_dict_ls, indent=4))
    return clean_text, tag_dict_ls


# identify language code for our mt model
def identify_language_codes(text_language, target_language):
    text_language = text_language.lower().strip()
    text_language_1 = text_language
    text_language = mbart50[text_language]

    target_language = target_language.lower().strip()
    target_language_1 = target_language
    target_language = mbart50[target_language]

    return text_language, target_language #, text_language_1, target_language_1


# extract texts from uploaded file
def extract_texts(file, file_type):
    data = {}
    all_texts = []

    if file_type == "json" or file_type == "jsonl":
        content_list = file.file.read().splitlines()
        for ix, row in enumerate(content_list):
            row = str(row, "utf-8")
            try:
                # json_acceptable_string = row.replace("'", "\"")
                # json_acceptable_string = row.replace("null", "None")
                row_dict = json.loads(row)
            except Exception as e:
                row_dict = ast.literal_eval(row.replace('null', 'None'))
            data[ix] = {
                "original_text": row_dict["text"],
                "meta": dict(list(row_dict.items())[1:])
            }
            all_texts.append(row_dict["text"])
    elif file_type == "csv":
        csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
        for ix, rows in enumerate(csvReader):             
            texts = rows["text"]
            texts = texts.split("\\n")
            # texts = extractSentences(texts)
            # texts = cleanText(texts)
            data[ix] = texts
            all_texts.append(texts)
    return data, all_texts


