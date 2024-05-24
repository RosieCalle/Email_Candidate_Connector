
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk

# https://www.nltk.org/install.html
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Stemming
    # https://tartarus.org/martin/PorterStemmer/
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    return ' '.join(tokens)


def determine_topic(text_body: str):
    # List of keywords for each topic
    job_offer_keywords = ["job alert", "job offer", "hiring", "vacancy", "open position"]
    job_interest_keywords = ["job search", "looking for a job", "career change"]
    person_looking_keywords = ["job hunting", "applying for jobs", "resume"]
    company_looking_keywords = ["recruiting", "talent acquisition", "hiring team"]

    # content = text_body.lower() 
    content = preprocess_text(text_body)
    # Check each topic
    if any(keyword in content for keyword in job_offer_keywords):
        return "JobOffer"
    elif any(keyword in content for keyword in job_interest_keywords):
        return "JobInterest"
    elif any(keyword in content for keyword in person_looking_keywords):
        return "PersonLooking"
    elif any(keyword in content for keyword in company_looking_keywords):
        return "CompanyLooking"
    else:
        return None
