#!/bin/bash

ln -s ../ontosplit/onto_splitter.pl .
ln -s ../ontospec/onto_spec.pl .
ln -s ../ontosplit/split.sh .
ln -s ../ontospec/spec.sh .

./split.sh
./spec.sh

