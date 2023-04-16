import re

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