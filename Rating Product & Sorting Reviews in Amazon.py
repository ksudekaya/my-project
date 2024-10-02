git add
###################################################
# PROJE: Rating Product & Sorting Reviews in Amazon
###################################################

###################################################
# İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden bir tanesi ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır.
# Bu problemin çözümü e-ticaret sitesi için daha fazla müşteri memnuniyeti sağlamak, satıcılar için ürünün öne çıkması ve satın
# alanlar için sorunsuz bir alışveriş deneyimi demektir. Bir diğer problem ise ürünlere verilen yorumların doğru bir şekilde sıralanması
# olarak karşımıza çıkmaktadır. Yanıltıcı yorumların öne çıkması ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi kayıp
# hem de müşteri kaybına neden olacaktır. Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken müşteriler
# ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.

###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı




#  Average Rating'i Güncel Yorumlara Göre Hesaplayınız ve Var Olan Average Rating ile Kıyaslama

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("amazon_review.csv")
df.head()
df.shape



df["overall"].value_counts()

df["overall"].mean()

df.head()
df.info()
df["reviewTime"] = pd.to_datetime(df["reviewTime"])


df["days"] = df["day_diff"]

df.loc[df["days"] <= 30, "overall"].mean()

df.loc[(df["days"] > 30) & (df["days"] <= 90), "overall"].mean()

df.loc[(df["days"] > 90) & (df["days"] <= 180), "overall"].mean()

df.loc[(df["days"] > 180), "overall"].mean()

df.loc[df["days"] <= 30, "overall"].mean() * 28/100 + \
    df.loc[(df["days"] > 30) & (df["days"] <= 90), "overall"].mean() * 26/100 + \
    df.loc[(df["days"] > 90) & (df["days"] <= 180), "overall"].mean() * 24/100 + \
    df.loc[(df["days"] > 180), "overall"].mean() * 22/100
#ağrılık top 100-ağırlık arttıkça range hareket alanı azaşır
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "overall"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "overall"].mean() * w4 / 100

time_based_weighted_average(df)



df.head()

###################################################
# Adım 1. helpful_no Değişkenini Üretiniz
###################################################

# Not:
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# up, helpful demektir.
# veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.
df['helpful_no'] = df['total_vote'] - df['helpful_yes']

###################################################
# Adım 2. score_pos_neg_diff, score_average_rating ve wilson_lower_bound Skorlarını Hesaplayıp Veriye Ekleyiniz
###################################################

def score_pos_neg_diff(up,down):
    return up - down


def score_average_rating(up,down):
    if up + down == 0:
        return 0
    return up / (up + down)

def wilson_lower_bound(up, down, confidence=0.95):
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


1.
yol:


def score_average_rating(helpful_yes, total_vote):
    if helpful_yes + total_vote == 0:
        return 0
    return helpful_yes / total_vote


df['helpfulness_score'] = df.apply(lambda row: score_average_rating(row['helpful_yes'], row['total_vote']), axis=1)

df.sort_values(by="helpfulness_score", ascending=False).head(20)

# 2.yol:
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]


def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla


Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
Hesaplanacak skor ürün sıralaması için kullanılır.
Not:
Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


df['wlb_score'] = df.apply(lambda row: wilson_lower_bound(row['helpful_yes'], row['helpful_no']), axis=1)

df.sort_values(by="wlb_score", ascending=False).head(20)


# 3.yol

def score_pos_neg_diff(helpful_yes, helpful_no):
    return helpful_yes - helpful_no


df['score_pos_neg_diff'] = df.apply(lambda row: score_pos_neg_diff(row['helpful_yes'], row['helpful_no']), axis=1)

df.sort_values(by="score_pos_neg_diff", ascending=False).head(20)


df['score_pos_neg_diff'] = df['helpful_yes'] - df['helpful_no']
df['score_average_rating'] = df['helpful_yes'] / (df['helpful_yes'] + df['helpful_no']).replace(0)

def wilson_lower_bound(pos, neg, confidence=0.95):

        n = pos+neg
        if n == 0:
            return 0
        z = st.norm.ppf(1 - (1 - confidence) / 2)
        phat = 1.0 * pos / n
        return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

df['wilson_lower_bound'] = df.apply(lambda x: wilson_lower_bound(x['helpful_yes'], x['helpful_no']), axis=1)
##################################################
# Adım 3. 20 Yorumu Belirleyiniz ve Sonuçları Yorumlayınız.
###################################################
top_reviews = df.sort_values('wilson_lower_bound', ascending=False).head(20)
top_reviews[['reviewerID', 'reviewText', 'wilson_lower_bound']]
