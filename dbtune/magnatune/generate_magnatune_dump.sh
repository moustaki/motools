#!/bin/bash

D2R_HOME=/home/dbtune/d2r-server
MAGNATUNE_DIR=/home/dbtune/motools/dbtune/magnatune
TMP_DIR=/tmp
RDF_DUMP=magnatune.rdf

curl http://www.magnatune.com/info/song_info.sql > ${TMP_DIR}/song_info.sql
mysql -udbtune magnatune < ${MAGNATUNE_DIR}/reset.sql
mysql -udbtune magnatune < ${TMP_DIR}/song_info.sql
rm ${TMP_DIR}/song_info.sql
${D2R_HOME}/dump-rdf -m ${MAGNATUNE_DIR}/magnatune_mapping.n3 -o ${MAGNATUNE_DIR}/magnatune.ttl -b http://dbtune.org/magnatune/

