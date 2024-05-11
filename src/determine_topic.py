def determine_topic(file_path):
    # TODO change the input params for body and keywords_table
    # List of keywords for each topic
    job_offer_keywords = ["job offer", "hiring", "vacancy", "open position"]
    job_interest_keywords = ["job search", "looking for a job", "career change"]
    person_looking_keywords = ["job hunting", "applying for jobs", "resume"]
    company_looking_keywords = ["recruiting", "talent acquisition", "hiring team"]

    # Read the file
    with open(file_path, 'r') as file:
        content = file.read().lower()  # Convert to lowercase for easier matching

    # Check each topic
    if any(keyword in content for keyword in job_offer_keywords):
        return "Job Offer"
    elif any(keyword in content for keyword in job_interest_keywords):
        return "Job Interest"
    elif any(keyword in content for keyword in person_looking_keywords):
        return "Person Looking for a Job"
    elif any(keyword in content for keyword in company_looking_keywords):
        return "Company Looking for Candidates"
    else:
        return "Uncategorized"

# Example usage
file_path = 'path/to/your/textfile.txt'
topic = determine_topic(file_path)
print(f"The topic of the text file is: {topic}")
# TODO return 'topic'