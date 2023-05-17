from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
# from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


# intitialize model for machine translation
class MbartTranslatorModels():
    def __init__(self):

        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")


class M2m100TranslatorModels():
    def __init__(self):
        self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
        # self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_1.2B")
        # self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_1.2B")