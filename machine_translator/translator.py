

# split text into sentences using some stopwords
def splitText(text):
    # stopwords are different with different languages. For now we just choose these three.
    stopwords = ['.', '!', '?']
    stopword_indxs = []
    for indx, char in enumerate(text):
        if char in stopwords:
            stopword_indxs.append(indx)
    all_sentences = []
    for ix, indx in enumerate(stopword_indxs):
        if ix == 0:
            all_sentences.append(text[:indx+1])
            if len(stopword_indxs) == 1:
                all_sentences.append(text[indx+1:])
        else:
            all_sentences.append(text[stopword_indxs[ix-1]+1:indx+1].strip())
            if len(text)>indx and ix == len(stopword_indxs)-1:
                    all_sentences.append(text[indx+1:])
    if len(stopword_indxs):
        return all_sentences
    else:
        return [text]


# remove leading spaces from each sentences and make the first letter capital for each sentences
def sentenceNormalization(all_sentences):
    all_sentences_temp = []
    for sentence in all_sentences:
        sentence = sentence.strip()
        if len(sentence)>1:
            sentence = sentence[0].upper()+sentence[1:]
        all_sentences_temp.append(sentence)
    return all_sentences_temp


# translate by sentence using syncronous parallilazition
def translateEachSentence_sync(mt_obj, sentence, source_language, target_language):
    mt_obj.tokenizer.src_lang = source_language
    encoded_text = mt_obj.tokenizer(sentence, return_tensors = "pt")
    encoded_text = encoded_text.to("cuda:0") # input text to cuda!!
    mt_obj.model = mt_obj.model.to("cuda:0")
    generated_tokens = mt_obj.model.generate(**encoded_text, forced_bos_token_id = mt_obj.tokenizer.lang_code_to_id[target_language])
    translated_sentence = mt_obj.tokenizer.batch_decode(generated_tokens, skip_special_tokens = True)
    return translated_sentence[0]


# translate text into text and audio in their targeted language
def translate_text(mt_obj, text, source_language, target_language):
    all_sentences = splitText(text)
    all_sentences = sentenceNormalization(all_sentences)
    src_sentences = []
    translated_sentence_ls = []
    # sequnetial processing
    for ix, sentence in enumerate(all_sentences):
        if len(sentence)<=1:
            continue
        if source_language == target_language:
            translated_sentence_ls.append(sentence)
            src_sentences.append(sentence)
        else:
            translated_sentence_ls.append(translateEachSentence_sync(mt_obj, sentence, source_language, target_language))
            src_sentences.append(sentence)
    translated_text = " ".join(translated_sentence_ls)
    return translated_text, src_sentences



# translate by sentence using syncronous parallilazition
def translateEachSentence_lifeline(mt_obj, sentence, source_language, target_language):
    mt_obj.tokenizer.src_lang = source_language
    encoded_text = mt_obj.tokenizer(sentence, return_tensors = "pt")
    generated_tokens = mt_obj.model.generate(**encoded_text, forced_bos_token_id = mt_obj.tokenizer.get_lang_id(target_language))
    translated_sentence = mt_obj.tokenizer.batch_decode(generated_tokens, skip_special_tokens = True)
    return translated_sentence[0]


# translate text into text and audio in their targeted language
def translate_text_lifeline(mt_obj, text, source_language, target_language):
    all_sentences = splitText(text)
    src_sentences = []
    translated_sentence_ls = []
    # sequnetial processing
    for ix, sentence in enumerate(all_sentences):
        if len(sentence)<=1:
            continue
        if source_language == target_language:
            translated_sentence_ls.append(sentence)
            src_sentences.append(sentence)
        else:
            translated_sentence_ls.append(translateEachSentence_lifeline(mt_obj, sentence, source_language, target_language))
            src_sentences.append(sentence)
    translated_text = " ".join(translated_sentence_ls)

    return translated_text, text

