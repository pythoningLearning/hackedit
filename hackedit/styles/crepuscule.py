"""
This module contains the darcula pygments theme.
"""
from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Literal, Name, \
    Operator, Text, Punctuation


class CrepusculeStyle(Style):
    """
    A dark theme for hackedit inspired by the Tomorrow Night theme from
    fish shell, adapted to look when using the Breeze Dark Theme (KDE) or the
    dark stylesheet (all platforms).
    """
    background_color = '#232629'
    highlight_color = '#353535'

    styles = {
        Comment.Multiline: '#969896',
        Comment.Preproc: '#81A2BE',
        Comment.Single: '#969896',
        Comment.Special: 'bold #81A2BE',
        Comment: '#969896',
        Error: '#CC0000',
        Generic.Deleted: '#CC4040',
        Generic.Emph: ' #c0d0e2',
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
        Keyword.Type: '#af81bd bold',
        Keyword: '#DE935F bold',
        Literal.Number: '#6897B3',
        Literal.String: '#B5BD68',
        Literal.String.Doc: '#81A2BE',
        Name.Attribute: '#800080',
        Name.Builtin.Pseudo: '#fcb5c6 italic',
        Name.Builtin: '#af81bd',
        Name.Class: '#CC6666 bold underline',
        Name.Constant: '#87feb9',
        Name.Decorator: '#CBC539',
        Name.Entity: '#CC6666',
        Name.Exception: '#CC6666 bold',
        Name.Function: '#CC6666 bold',
        Name.Label: '#c0d0e2 bold',
        Name.Namespace: '#c0d0e2',
        Name.Tag: '#A5C261 bold',
        Name.Variable.Class: '#c0d0e2 bold',
        Name.Variable.Global: '#c0d0e2 bold',
        Name.Variable.Instance: '#c0d0e2',
        Name.Variable: '#c0d0e2',
        Operator: '#c0d0e2 bold',
        Operator.Word: '#DE935F bold',
        Text: '#c0d0e2',
        Text.Whitespace: '#656565',
        Punctuation: '#c0d0e2'
    }
