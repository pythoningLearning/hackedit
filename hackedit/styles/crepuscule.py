"""
This module contains the darcula pygments theme.
"""
from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Literal, Name, \
    Operator, Text, Punctuation


class CrepusculeStyle(Style):
    """
    A dark theme for hackedit inspired by the Tomorrow Night theme from
    fish shell (this color scheme looks good when using arc-dark gtk theme).
    """
    background_color = '#404552'
    highlight_color = '#303542'

    styles = {
        Comment.Multiline: '#969896',
        Comment.Preproc: '#81A2BE',
        Comment.Single: '#969896',
        Comment.Special: 'bold #81A2BE',
        Comment: '#969896',
        Error: '#CC0000',
        Generic.Deleted: '#CC4040',
        Generic.Emph: ' #B9C7D6',
        Generic.Error: '#aa0000',
        Generic.Heading: '#999999',
        Generic.Inserted: '#40CC40',
        Generic.Output: '#888888',
        Generic.Prompt: '#555555',
        Generic.Strong: 'bold',
        Generic.Subheading: '#aaaaaa',
        Generic.Traceback: '#aa0000',
        Keyword.Constant: '#DE935F',
        Keyword.Declaration: '#DE935F',
        Keyword.Namespace: '#DE935F',
        Keyword.Pseudo: '#DE935F',
        Keyword.Reserved: '#DE935F',
        Keyword.Type: '#B294BB bold',
        Keyword: '#DE935F bold',
        Literal.Number: '#6897B3',
        Literal.String: '#B5BD68',
        Literal.String.Doc: '#81A2BE',
        Name.Attribute: '#800080',
        Name.Builtin.Pseudo: '#B294BB italic',
        Name.Builtin: '#B294BB',
        Name.Class: '#CC6666 bold underline',
        Name.Constant: '#B294BB',
        Name.Decorator: '#CBC539',
        Name.Entity: '#B294BB',
        Name.Exception: '#CC6666 bold',
        Name.Function: '#CC6666 bold',
        Name.Label: '#B9C7D6 bold',
        Name.Namespace: '#B9C7D6',
        Name.Tag: '#A5C261 bold',
        Name.Variable.Class: '#B9C7D6 bold',
        Name.Variable.Global: '#B9C7D6 bold',
        Name.Variable.Instance: '#B9C7D6',
        Name.Variable: '#B9C7D6',
        Operator: '#B9C7D6 bold',
        Operator.Word: '#DE935F bold',
        Text: '#B9C7D6',
        Text.Whitespace: '#656565',
        Punctuation: '#B9C7D6'
    }
