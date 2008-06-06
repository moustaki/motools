#!/bin/bash

# Pick a random DBtune uri in file

RANGE=`cat $1 |grep dbtune.org | wc -l`
echo $RANGE
number=$RANDOM
let "number %= $RANGE" 
echo "$number: "

#cat $1 |grep dbtune.org | grep -n dbtune.org | grep "^$number: "
cat $1|grep dbtune.org | sed -n "${number} p"


