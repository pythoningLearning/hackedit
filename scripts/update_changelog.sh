#! /bin/bash

export CHANGELOG_GITHUB_TOKEN=67de0cef5612a0089ac56e597c5716d377931636

cd ..

# automatically generate changelog (ignoring issues reported for plugins).
github_changelog_generator --exclude-labels duplicate,question,invalid,wontfix,hackedit-cobol,hackedit-python
