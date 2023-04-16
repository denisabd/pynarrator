import re

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

