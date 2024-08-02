from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10
    )
    text = text_splitter.split_text(text)
    return text

# text = chunk_text(example_text)
# print(text)
