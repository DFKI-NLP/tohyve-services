import fugashi
import nltk
nltk.download('punkt')

from nltk.tokenize import sent_tokenize, word_tokenize
from langdetect import detect

# param: text-> str
# return: words->list (tokenized list for japanese language)
def create_japanesse_tokenizer(text):
    words = []
    texts = [text]
    tagger = fugashi.Tagger()
    for txt in texts:
        words = tagger(txt)
    for i , v in enumerate(words):
        words[i] = str(v)
    
    return  words


# param: text-> str
# return: words->list (tokenized list for all other languages)
def create_tokenizer(text):
    words = []
    words_ls = [word_tokenize(t) for t in sent_tokenize(text)]
    for single_word_ls in words_ls:
        for word_ls in single_word_ls:
            words.append(word_ls)
    
    return words


# params: bi-obj-> bitext-align class object, src_text-> str, tr_text-> str
# return: list-> list of tuples (each tuple contains alignment indexes of two words, 
# first index denote from src_text and second index denote index from tr_text)
def align_text(bi_obj, src_text, tr_text):
    src_ln = detect(str(src_text))
    tr_ln = detect(str(tr_text))
    if src_ln == "ja":
        src_words = create_japanesse_tokenizer(src_text)
    else:
        src_words = create_tokenizer(src_text)

    if tr_ln == "jp":
        tr_words = create_japanesse_tokenizer(tr_text)
    else:
        tr_words = create_tokenizer(tr_text)

    alignments = bi_obj.model.get_word_aligns(src_words, tr_words)
    tuple_ls = []
    for tuple in alignments["mwmf"]:
        tuple_ls.append((src_words[tuple[0]] +" : "+tr_words[tuple[1]]))
    return alignments["mwmf"],src_words, tr_words, tuple_ls