from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

# text = """転職 Advent Calendar 2016 - Qiitaの14日目となります。 少しポエムも含みます。
# 今年11月にSIerからWebサービスの会社へ転職しました。
# 早くから退職することを報告していたこともあって、幸いにも有給消化として１ヶ月のお休みをいただくことができました（これでも10日ほど余らせてしまいました）。
# ・・・ (省略) ・・・
# だからこそ、有給消化期間はなんとしてでももぎ取るようにしましょう。"""

text = """児童文学者、翻訳家。
群馬県北甘楽郡生まれ。
筆名は朝日壮吉等。
1918（大正7）年、早稲田大学英文科卒業後、母校、立教中学の教師となる。
早稲田在学中から山本有三に師事し、1919（大正8）年には、浜田広介、水谷まさるらと同人雑誌「基調」を創刊。
「新青年」に、吉田夏村の筆名で探偵小説の翻訳を寄稿した時期を経て、1927（昭和2）年頃からは、朝日壮吉名で「少年倶楽部」等に児童文学作品を発表するようになる。
1932（昭和7）年、明治大学教授に。戦後は、1946（昭和21）年に創刊された児童雑誌「銀河」（新潮社）の編集にたずさわる。
代表作に、「サランガの冒険」「源太の冒険」「兄弟いとこものがたり」等。ラドヤード・キップリングの「海の子ハービ」、マーク・トウェイン「ハックルベリー＝フィンの冒険」等の翻訳もある。（代）"""

# 1行1文となっているため、改行コードで分離
sentences = [t for t in text.split('\n')]
for i in range(2):
    print(sentences[i])
# 転職 Advent Calendar 2016 - Qiitaの14日目となります。 少しポエムも含みます。
# 今年11月にSIerからWebサービスの会社へ転職しました。

# 形態素解析器を作る
analyzer = Analyzer(
    [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')],  # ()「」、。は全てスペースに置き換える
    JanomeTokenizer(),
    [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]  # 名詞・形容詞・副詞・動詞の原型のみ
)

# 抽出された単語をスペースで連結
# 末尾の'。'は、この後使うtinysegmenterで文として分離させるため。
corpus = [' '.join(analyzer.analyze(s)) + '。' for s in sentences]
for i in range(2):
    print(corpus[i])
# 転職 Advent Calendar 2016 - Qiita 14 日 目 なる 少し ポエム 含む。
# 今年 11 月 SIer Web サービス 会社 転職 する。

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# 連結したcorpusを再度tinysegmenterでトークナイズさせる
parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

# LexRankで要約を2文抽出
summarizer = LexRankSummarizer()
summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する

summary = summarizer(document=parser.document, sentences_count=2)

print(summary)

# 元の文を表示
for sentence in summary:
    print(sentences[corpus.index(sentence.__str__())])
