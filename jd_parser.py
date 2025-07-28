import re

def extract_job_description(text):
    """
    Cleans and returns job description text.
    Assumes raw text input (from textarea or file).
    """
    # Remove HTML tags if any
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)

    # Normalize whitespace
    cleantext = re.sub(r'\s+', ' ', cleantext).strip()

    return cleantext
