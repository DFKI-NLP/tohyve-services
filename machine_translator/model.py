import torch
import os

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
# from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


# intitialize model for machine translation
class MbartTranslatorModels():
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt").to(self.device)
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")


class M2m100TranslatorModels():
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.path = "models/"
        if os.path.exists(self.path+"/m2m100_418M"):        
            self.model = M2M100ForConditionalGeneration.from_pretrained("models/m2m100_418M").to("cuda:0")
            self.tokenizer = M2M100Tokenizer.from_pretrained("models/m2m100_418M")
        elif os.path.exists("/app/"+self.path+"/m2m100_418M"):
            self.model = M2M100ForConditionalGeneration.from_pretrained("/app/models/m2m100_418M").to("cuda:0")
            self.tokenizer = M2M100Tokenizer.from_pretrained("/app/models/m2m100_418M")
        else:
            self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(self.device)
            self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
        # self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_1.2B")
        # self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_1.2B")