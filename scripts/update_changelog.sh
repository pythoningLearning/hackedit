#! /bin/bash

# automatically generate changelog (ignoring issues reported for plugins).
github_changelog_generator --exclude-labels duplicate,question,invalid,wontfix,hackedit-cobol,hackedit-python

