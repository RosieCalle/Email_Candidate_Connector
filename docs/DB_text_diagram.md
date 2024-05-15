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

mark email as answered