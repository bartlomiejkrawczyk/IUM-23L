#!/bin/bash

pandoc stage_1.ipynb \
    --verbose \
    --standalone \
    --highlight=tango \
    --pdf-engine=latexmk \
    --from ipynb \
    -o stage_1.pdf \
    -V geometry:margin=1cm \
    -F mermaid-filter
