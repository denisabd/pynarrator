import re
from pynarrator import clean_text, format_text

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
