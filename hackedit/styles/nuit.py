"""
This module contains the darcula pygments theme.
"""
from .crepuscule import CrepusculeStyle


class NuitStyle(CrepusculeStyle):
    """
    A darker version of the crepuscule style.

    This theme looks good on KDE Breeze dark or with the dark stylesheet.
    """
    background_color = '#252525'
    highlight_color = '#353535'
