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