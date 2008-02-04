#!/bin/bash

# Install dependencies for GNARQL
# Prerequesites:
#   * Install GIT

git clone git://gollem.science.uva.nl/home/git/ClioPatria.git

cp SeRQL/*.html ClioPatria/SeRQL/
cp SeRQL/*.css ClioPatria/SeRQL/
cp SeRQL/rdf_html.pl ClioPatria/SeRQL/
cp SeRQL/http_user.pl ClioPatria/SeRQL/


