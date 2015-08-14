#!/bin/bash
. ./conf/conf.sh

if [ ! -d ${WORK_DIR} ]
then
    rm -rf ${WORK_DIR}
    mkdir -p ${WORK_DIR}
fi

date
echo 'start dump data from mysql'
sh ${SCRIPT_DIR}/dump_data.sh
if [ $? -ne 0 ]
then
    date
    echo 'dump date error'
    exit 1
fi

date
echo 'start merge data'
${PYTHON} ${SCRIPT_DIR}/merge_data.py \
    ${RAW} \
    ${TWEET} \
    ${ZAN} \
    ${COMMENT} \
    ${RESOURCE} \
    ${TWEET_ACTION} \
    ${HOT_PIC_CONF}
if [ $? -ne 0 ]
then
    date
    echo 'merge date error'
    exit 1
fi

date
echo 'update tweet score'
${PYTHON} ${SCRIPT_DIR}/update.py \
    ${RAW} \
    ${DB_HOST} \
    ${DB_PORT} \
    ${DB_USER} \
    ${DB_PWD} \
    ${DB_TABLE}
if [ $? -ne 0 ]
then
    date
    echo 'update tweet score error'
    exit 1
fi

