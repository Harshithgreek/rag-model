import tiktoken

def chunk_text(text: str, chunk_tokens: int=450, overlap_tokens: int =80):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)   

    chunks=[]
    start=0
    while start < len(tokens):
        end = start + chunk_tokens
        chunk = tokens[start:end]
        chunks.append(chunk)
        start += chunk_tokens - overlap_tokens
        if start<0:
            start=0
    
    # Decode chunks back to text
    text_chunks = [enc.decode(chunk) for chunk in chunks]
    return text_chunks