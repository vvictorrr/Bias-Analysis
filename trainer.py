import pandas as pd
import string
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()

# load csv
df = pd.read_csv("bias_classification_dataset.csv")

df = df.groupby('bias').apply(lambda x: x.sample(n=min(len(x), 100), random_state=42)).reset_index(drop=True)

# preprocessing to remove distinctive formatting

def preprocess(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

df['clean_text'] = df['text'].apply(preprocess)

#vectorize
vectorizer = TfidfVectorizer(max_features=10000, stop_words='english', ngram_range=(1, 3), min_df=3, max_df=0.8)
X = vectorizer.fit_transform(df['clean_text'])
y = df['bias']

#split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

y_encoded = label_encoder.fit_transform(y)
X_train2, X_test2, y_train_encoded, y_test_encoded = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

#training models
model_lr = LogisticRegression(max_iter=1000, class_weight='balanced')
model_lr.fit(X_train, y_train)

model_rf = RandomForestClassifier(n_estimators=100)
model2.fit(X_train, y_train)

model_gb = GradientBoostingClassifier()
model_gb.fit(X_train, y_train)

model_xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
model_xgb.fit(X_train2, y_train_encoded)

#evaluation
y_pred = model_lr.predict(X_test)
print('logreg')
print(classification_report(y_test, y_pred))

y_pred2 = model_rf.predict(X_test)
print('randomforest')
print(classification_report(y_test, y_pred2))

print('gradientboost')
y_pred3 = model_gb.predict(X_test)
print(classification_report(y_test, y_pred3))

print('xgb')
y_pred4 = model_xgb.predict(X_test2)
print(classification_report(y_test_encoded, y_pred4))

#scoring system

y_proba = model3.predict_proba(X_test)
class_labels = model3.classes_

#for i, probs in enumerate(y_proba[:5]):  # show top 5
#    print(f"Text {i}:")
#    for label, prob in zip(class_labels, probs):
#        print(f"  {label}: {prob:.2f}")
#    print()

def score_bias(text):
    cleaned = preprocess(text)
    vec = vectorizer.transform([cleaned])
    proba = model3.predict_proba(vec)[0]
    #class_names = label_encoder.inverse_transform(range(len(proba)))
    return dict(zip(model3.classes_, proba))

text = "Consider a June Ipsos poll of Democrats, the latest of many surveys showing the Democratic base is unhappy with the state of their party. About half of Democrats are unsatisfied with current leadership, and 62 percent said party leaders should be replaced. This dissatisfaction is historic. Going back to 2009, Democrats havent been this upset with their party before. As noted, the last time a partys base was worked up was during the Republicans Tea Party movement, which culminated in Trumps GOP takeover.Unlike previous moments of Democratic infighting, this divide isnt primarily about ideology. That same June poll found that Democrats want their party to focus more on affordability, on getting the wealthy to pay more on taxes, and health care expansion. Older and younger Democrats are broadly in agreement about prioritizing economic concerns over social issues — and there arent that many differences between what younger and older Democrats want to prioritize."

scores = score_bias(text)

for label, score in sorted(scores.items(), key=lambda x: -x[1]):
    print(f"{label}: {score:.2f}")