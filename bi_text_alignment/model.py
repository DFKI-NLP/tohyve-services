from simalign import SentenceAligner


class BiTextModels():
    def __init__(self):
        self.model = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")