from faker import Faker

fake = Faker()

def generate_examples(mime_type, num_examples=5):
    examples = []
    if mime_type == 'text/plain':
        for _ in range(num_examples):
            examples.append(fake.text())
    elif mime_type == 'text/html':
        for _ in range(num_examples):
            examples.append(f'<html><body>{fake.text()}</body></html>')
    elif mime_type == 'application/pdf':
        for _ in range(num_examples):
            examples.append(f'{fake.file_name(extension="pdf")}')
    elif mime_type == 'image/jpeg':
        for _ in range(num_examples):
            examples.append(f'{fake.file_name(extension="jpeg")}')
    elif mime_type == 'image/png':
        for _ in range(num_examples):
            examples.append(f'{fake.file_name(extension="png")}')
    else:
        print("Unsupported MIME type")
    return examples

if __name__ == "__main__":
    mime_types = ['text/plain', 'text/html', 'application/pdf', 'image/jpeg', 'image/png']
    for mime_type in mime_types:
        print(f'MIME Type: {mime_type}')
        examples = generate_examples(mime_type)
        for example in examples:
            print(example)
        print("\n")