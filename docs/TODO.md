TODO

* SAMPLES for TESTs

email samples
- empty subject
- empty body
- 1 attachment
- 3 attachments
- attachments : word.docx, .pdf, vcard, excel
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



### Textual Representation:

```
+----------------+     +----------------+     +----------------+
|     Emails     |     | Attachments   |     |   Contacts    |
+----------------+     +----------------+     +----------------+
| MessageID (PK) |---> | MessageID (PK) |     | ContactID (PK) |
| Subject        |     | Attachment1    |     | Name           |
| Timestamp      |     | Attachment2    |     | Phone          |
| ThreadID       |     | Attachment3    |     | Country        |
| Body           |     +----------------+     | City           |
| SenderID       | -------------------------> | SenderID       |
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

-- investigate how to use this
Introducing the Spam Detection Model with Pre-Trained LLM | by Varun Tyagi | Mar, 2024 | Medium
https://medium.com/@varun.tyagi83/introducing-the-spam-detection-model-with-pre-trained-llm-3eb1f8186ba1

