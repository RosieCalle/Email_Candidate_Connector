TODO

* SAMPLES for TESTs

email samples
- empty subject
- empty body
- 1 attachment
- 3 attachments
- attachments : word.docx, .pdf, vcard
- attachment: image (we will discard it)
- email with threads
- email with signature, different variations

* PARSING
    phone number
    address ?
    email == sender
 

* DATABASE

table emails
    subject
    timestamp
    messageid
    threadid
    body
    senderid

table attachemnts
    messageid
    attachment1
    attachemnt2
    attachment3

table contacts
    name
    phone
    email
    city
    country
    zipcode
    sponsorship
    hibryd
    remote
    inperson
    education
    license
    clearance
    salaryreq

# TODO Analyze case for email from another recruiter(jobseeker or company) or company looking for employees



# Review and improve the documentation 

### Textual Representation:

```                                               JobSeeker
+----------------+     +----------------+     +----------------+
|     Emails     |     | Attachments    |     |   Contacts     |
+----------------+     +----------------+     +----------------+
| MessageID (PK) |---> | MessageID (PK) |     | ContactID (PK) |
| Subject        |     | Attachment1    |     | Name           |
| Timestamp      |     | Attachment2    |     | Phone          |
| ThreadID       |     | Attachment3    |     | Country        |
| Body           |     +----------------+     | City           |
| SenderID       | -------------------------> | SenderID (SK)  |
+----------------+                            | Zipcode        |
                                              | Sponsorship    |
                                              | Hybrid         |
                                              | Remote         |
                                              | InPerson       |
                                              | Education      |
                                              | License        |
                                              | Clearance      |
                                              | SalaryReq      |
                                              +----------------+
```


           CREATE TABLE IF NOT EXISTS Emails (
                subject VARCHAR(255),
                timestamp TIMESTAMP,
                messageid VARCHAR(16) PRIMARY KEY,
                threadid VARCHAR(16),
                body TEXT,
                senderid INT




-- investigate how to use this
Introducing the Spam Detection Model with Pre-Trained LLM | by Varun Tyagi | Mar, 2024 | Medium
https://medium.com/@varun.tyagi83/introducing-the-spam-detection-model-with-pre-trained-llm-3eb1f8186ba1

