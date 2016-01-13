"""
This module contains the darcula pygments theme.
"""
from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Literal, Name, \
    Operator, Text, Punctuation


class AubeStyle(Style):
    """
    A light color scheme inspired by the Tomorrow theme from fish shell.
    """
    background_color = '#ffffff'
    highlight_color = '#c7e7f9'

    styles = {
        Comment.Multiline: '#969896',
        Comment.Preproc: '#4271AE',
        Comment.Single: '#969896',
        Comment.Special: 'bold #4271AE',
        Comment: '#969896',
        Error: '#CC0000',
        Generic.Deleted: 'bg:#ffdddd #000000',
        Generic.Emph: ' #000000',
        Generic.Error: '#aa0000',
        Generic.Heading: '#999999',
        Generic.Inserted: 'bg:#ddffdd #000000',
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
        Keyword.Type: '#8959A8 bold',
        Keyword: '#DE935F bold',
        Literal.Number: '#6897B3',
        Literal.String: '#007EA1',
        Literal.String.Doc: '#4271AE',
        Name.Attribute: '#800080',
        Name.Builtin.Pseudo: '#705050 italic',
        Name.Builtin: '#8959A8',
        Name.Class: '#CC6666 bold underline',
        Name.Constant: '#B200B2',
        Name.Decorator: '#DFB500',
        Name.Entity: '#8959A8',
        Name.Exception: '#CC6666 bold',
        Name.Function: '#CC6666 bold',
        Name.Label: '#000000 bold',
        Name.Namespace: '#000000',
        Name.Tag: '#2984C6 bold',
        Name.Variable.Class: '#000000 bold',
        Name.Variable.Global: '#000000 bold',
        Name.Variable.Instance: '#000000',
        Name.Variable: '#000000',
        Operator: '#000000 bold',
        Operator.Word: '#DE935F bold',
        Text: '#000000',
        Text.Whitespace: '#BFBFBF',
        Punctuation: '#000000'
    }
