import pandas as pd
import re
import snowballstemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec

#sayısal değerlerin kaldırılması
def remove_numeric(value):
    bfr = [item for item in value if not item.isdigit()]
    bfr = "".join(bfr)
    return bfr

#emojileri kaldırmak
def remove_emoji(value):
    bfr = re.compile("[\U00010000-\U0010ffff]",flags=re.UNICODE)
    bfr = bfr.sub(r'',value)
    return bfr

#tek karakterli ifadelerin kaldırılması
def remove_single_character(value):
    return re.sub(r'(?:^| )\w(?:$| )', '', value)

#noktalama işaretlerinin kaldırılması
def remove_noktalama(value):
    return re.sub(r'[^\w\s]','',value)

#linklerin kaldırılması
def remove_link(value):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',value)

#hashtaglerin kaldırılması
def remove_hashtag(value):
    return re.sub(r'#[^\s]+','',value)

#kullanıcı adların kaldırılması
def remove_username(value):
    return re.sub('@[^\s]+','',value)

#kök indirgeme ve stop words işlemleri
def stem_word(value):
    stemmer = snowballstemmer.stemmer("turkish")
    value = value.lower()
    value = stemmer.stemWords(value.split())
    stop_words = ["acaba", "ama", "aslında", "az", "bazı", "belki", "ben", "biri", "birkaç", "birşey", "biz", "bu", 
        "çok","çünkü", "da", "daha", "de", "defa", "diye", "eğer"
        "en", "gibi", "hem", "hep", "hepsi", "her", "hiç", "için", "ile", "ise", 
        "kez", "ki", "kim", "mı", "mu", "mü", "nasıl", "ne", "neden",
        "nerde", "nerede", "nereye", "niçin", "niye", "o", "sanki", "şey", "siz", "şu", 
        "tüm", "ve", "veya", "ya", "yani",
        "bir","iki","üç","dört","beş","altı","yedi","sekiz","dokuz","on"]
    value = [item for item in value if not item in stop_words]
    value = ' '.join(value)
    return value

#bütün fonksiyonların çağrılıp kullanılmasını sağlayan fonksiyonumuz
def pre_processing(value):
    return [remove_numeric(remove_emoji
                          (remove_single_character
                           (remove_noktalama
                            (remove_link
                             (remove_hashtag
                              (remove_username
                               (stem_word(word)))))))) for word in value.split()]

# boşlukların kaldırılması
def remove_space(value):
    return [item for item in value if item.strip()]

# bag of words model
def bag_of_words(value):
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(value)
    return x.toarray().tolist()

# tf-idf modelimiz
def tfidf(value):
    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform(value)
    return x.toarray().tolist()

#word2vec modelimiz
def word2vec(value):
    model = Word2Vec.load("data/word2vec.model")
    bfr_list = []
    bfr_len = len(value)
    
    for k in value:
        bfr = model.wv.key_to_index[k]
        bfr = model.wv[bfr]
        bfr_list.append(bfr)
    
    bfr_list = sum(bfr_list)
    bfr_list = bfr_list/bfr_len
    return bfr_list.tolist()