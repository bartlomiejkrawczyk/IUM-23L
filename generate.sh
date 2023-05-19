#!/bin/bash

pandoc stage_2.ipynb \
    --verbose \
    --standalone \
    --highlight=tango \
    --pdf-engine=latexmk \
    --from ipynb \
    -o stage_2.pdf \
    -V geometry:margin=2cm \
    -F mermaid-filter

rm mermaid-filter.err