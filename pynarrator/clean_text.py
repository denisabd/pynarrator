import re

def clean_text(
    text, 
    upper=['YTD', 'PYTD'], 
    lower=['vs', 'br>', 'h1>', 'h2>', 'h3>', 'h4>', 'h5>', 'h6>', 'b>']
    ):
    """
    Clean Text String.

    This function cleans up the text string improving narration, removing excessive white spaces.

    Args:
        text (str): Text string for cleaning. Can contain multiple sentences.
        upper (List[str], optional): Vector of words that need to be changed to uppercase in text. Defaults to None.
        lower (List[str], optional): Vector of words that need to be changed to lowercase in text. Defaults to None.

    Returns:
        str: Text string.

    Examples:
        >>> text = 'Similarly in 2020 the sum of spend increased by 15.4%  ( 4.3 % higher  than average).'
        >>> clean_text(text)
        'Similarly in 2020 the sum of spend increased by 15.4% (4.3% higher than average).'
        >>> clean_text(' Total  is 12,300 Orders ( 23.5 % for East  ) ')
        'Total is 12,300 Orders (23.5% for East).'
    """
    # helper to detect the upper case
    def is_upper(string):
        return all(c.isupper() for c in string)
    
    # assertion
    text_processed = re.sub(r'\s+', ' ', text.strip())
    
    # Clean spaces before commas and after brackets ---------------------------
    text_processed = re.sub(r'\( ', '(', text_processed)
    text_processed = re.sub(r' \)', ')', text_processed)
    text_processed = re.sub(r' ,', ',', text_processed)
    text_processed = re.sub(r' \.', '.', text_processed)
    
    # Add space before percentage ---------------------------------------------
    text_processed = re.sub(r'(?<=\d)\%', ' %', text_processed)
    
    # Capitalize first word ---------------------------------------------------
    # Split to sentences and capitalize every first word (if it is not UPPER case)
    sentences = re.split(r'\. ', text_processed)
    
    for i in range(len(sentences)):
        # check for UPPER case
        if not is_upper(sentences[i].split()[0]):
            sentences[i] = re.sub(r'\b\w+\b', lambda m: m.group(0).capitalize(), sentences[i], 1)
    
    text_processed = '. '.join(sentences)
    
    # Replace the pattern Lowercase
    for pat in lower:
        text_processed = re.sub(re.escape(pat), pat.lower(), text_processed, flags=re.IGNORECASE)
    
    # Replace the pattern Uppercase
    for pat in upper:
        text_processed = re.sub(re.escape(pat), pat.upper(), text_processed, flags=re.IGNORECASE)
    
    # Replace excessive whitespaces once again - in case if replacement led to multiple spaces
    text_processed = re.sub(r'\s+', ' ', text_processed.strip())
    
    return text_processed