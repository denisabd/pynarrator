import re
import inflect

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

def format_text(
        text, 
        color='auto', 
        bold=True):
    """
    Add HTML Tags to Add Color and Boldness
    Function adds html code around the selected string adding options for colorized and/or bold display in HTML documents.

    Parameters
    ----------
    text: str or list of str
        Text string that you want to format
    color: str
        Color name, for 'auto' the color will be determined based on the number parsed - red for negative, green for positive
    bold: bool 
        Make text bold or not

    Returns
    -------
    str: text with HTML tags

    Examples
    --------
    >>> format_text("1.2%", color = "auto", bold = TRUE)
    """
    text = str(text)
    text = re.sub('  ', ' ', text)

    # automatic color will, if string contains a number
    if color == 'auto' and any(char.isdigit() for char in text):
        if float(re.findall(r'[-+]?\d*\.\d+|\d+', text)[0]) < 0:
            color = 'red'
        elif float(re.findall(r'[-+]?\d*\.\d+|\d+', text)[0]) > 0:
            color = 'green'
        else:
            color = 'black'
    elif color == 'auto' and not any(char.isdigit() for char in text):
        color = 'black'

    # bold text
    if bold:
        text_processed = f"<b> <span style='color: {color};'>{text}</span> </b>"
    else:
        text_processed = f"<span style='color: {color};'>{text}</span>"

    return text_processed

def format_pct(
        text, 
        positive = 'green', 
        negative = 'red'):
    """
    Add HTML tags with colors to percentage values in text.

    Parameters
    ----------
    text : str or list of str
        Text string or list of text strings.
    positive : str, optional
        Color to highlight percentage increase. Default is 'green'.
    negative : str, optional
        Color to highlight percentage decline. Default is 'red'.

    Returns
    -------
    list of str
        List of text strings with HTML tags added for colored percentage values.

    Examples
    --------
    >>> text = 'Spend increased by 13.2 % in EMEA but decreased by -13.2 % in LATAM'
    >>> format_pct(text)
    ['Spend increased by <span style='color:green'>13.2%</span> in EMEA but decreased by <span style='color:red'>-13.2%</span> in LATAM']
    """
    # Check if text or number is provided for text
    if not isinstance(text, (str, list)):
        raise ValueError('Provide list, character text or numeric value')
    
    # Converting str to list
    if isinstance(text, str):
        text = [text]

    # Replace excessive punctuation
    text = [re.sub(' %', '%', t) for t in text]
    text = [re.sub(r'\(', ' (', t) for t in text]
    text = [re.sub(r'\)', ') ', t) for t in text]
    text = [re.sub(r'(?![.%-//)//://(])[[:punct:]]', '', t) for t in text]

    # Looping through the vector/list of narrations
    for i, t in enumerate(text):
        t_list = t.split()
        num_value = float(re.sub(r'[^\d.-]', '', t_list[0])) if '%' in t_list[0] else None
        t_list[0] = format_text(t_list[0], color=positive) if num_value is not None and num_value >= 0 else format_text(t_list[0], color=negative) if num_value is not None and num_value < 0 else t_list[0]
        text[i] = ' '.join(t_list)

    text_output = [clean_text(t) for t in text] if isinstance(text, list) else clean_text(text)
    return text_output

def pluralize(word):
  engine = inflect.engine()
  plural = engine.plural(word)
  return(plural)

def clean_tags(html_string):
    """
    Clean HTML Tags from the Text

    :param html_string: Text with HTML tags
    :type html_string: str
    
    :return: A string with the text content of the input without HTML tags
    :rtype: str
    
    :raises ValueError: If the input is not a string
    
    :seealso: `add_tag()` function for adding tags to text
    
    :examples:
    >>> clean_tags('<b>Total increase is equal to 14.5 % </b>')
    'Total increase is equal to 14.5 %'
    >>> clean_tags('<h2>Sales by Region</h3>')
    'Sales by Region'
    """
    if not isinstance(html_string, str):
        raise ValueError('Provide text string')

    string_processed = re.sub('<.*?>', '', html_string)
    string_processed = string_processed.replace('( ', '(')
    string_processed = string_processed.replace(' )', ')')
    string_processed = string_processed.replace(' ,', ',')
    string_processed = string_processed.replace(' .', '.')
    string_processed = re.sub('(?<=\\d)%', ' %', string_processed)
    string_processed = re.sub('\\s+', ' ', string_processed).strip()

    return string_processed

def add_tag(text, tag='h3'):
    """
    Add HTML Tags to Text

    :param text: A text string or numeric value
    :type text: str or int or float
    
    :param tag: An HTML tag like p, b, h1 or other (default is 'h3')
    :type tag: str
    
    :return: A string with the text content of the input wrapped in the specified HTML tag
    :rtype: str
    
    :raises ValueError: If the input is not a string or numeric value
    
    :seealso: `clean_tags()` function for removing HTML tags from text
    
    :examples:
    >>> add_tag('Title Text', tag='h2')
    '<h2> Title Text </h2>'
    >>> add_tag('bold text', tag='b')
    '<b> bold text </b>'
    """
    if not isinstance(text, (str, int, float)):
        raise ValueError('Provide text string or numeric value')

    output = f'<{tag}> {text} </{tag}>'
    return output