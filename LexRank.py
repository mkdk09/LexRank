from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

class LexRank:
    def tense_analyze(self, text, sentences_count):
        # 1行1文となっているため、改行コードで分離
        # sentences = [t for t in text.split('\n')]
        sentences = [t for t in text.split('。')]

        # 形態素解析器を作る
        analyzer = Analyzer(
                [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')],  # ()「」、。は全>てスペースに置き換える
                JanomeTokenizer(),
                [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]  # 名詞>・形容詞・副詞・動詞の原型のみ
                )

        # 抽出された単語をスペースで連結
        # 末尾の'。'は、この後使うtinysegmenterで文として分離させるため。
        corpus = [' '.join(analyzer.analyze(s)) + '。' for s in sentences]

        # 連結したcorpusを再度tinysegmenterでトークナイズさせる
        parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

        # LexRankで要約を2文抽出
        summarizer = LexRankSummarizer()
        summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外>する
        summary = summarizer(document=parser.document, sentences_count=sentences_count)

        return sentences, corpus,  summary
