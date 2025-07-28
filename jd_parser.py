def extract_skills_from_jd(jd_text):
    keywords = {"python", "java", "c++", "sql", "html", "css", "javascript", "aws", "react", "node.js"}
    found_skills = {word for word in keywords if word.lower() in jd_text.lower()}
    return found_skills