################# basic conf ###########
MYSQL=mysql
PYTHON=python

#base_dir需要是绝对路径
BASE_DIR="/home/meihua/dingchuan/autoindex"
SQL_DIR="${BASE_DIR}/sql/"
BIN_DIR="${BASE_DIR}/bin/"
SCRIPT_DIR="${BASE_DIR}/script/"
WORK_DIR="${BASE_DIR}/data/work/"
WORK_BAK_DIR="${BASE_DIR}/data/work.bak"
LOG_DIR="${BASE_DIR}/log/"
CONF_DIR="${BASE_DIR}/conf/"
INDEX_DIR="${BASE_DIR}/index/"

################# 图片热度算法 conf ###########
HOT_PIC_CONF="${CONF_DIR}/calculate_hot_pic.conf"

################# DB conf ###########
DB_HOST=""
DB_PORT=""
DB_USER=""
DB_PWD=""
DB_ARGS="--default-character-set=utf8"
DB_TABLE=""


################# file ###########
RAW="${WORK_DIR}/raw"
TWEET="${WORK_DIR}/tweet"
ZAN="${WORK_DIR}/zan"
COMMENT="${WORK_DIR}/comment"
RESOURCE="${WORK_DIR}/resource"
TWEET_ACTION="${WORK_DIR}/tweet_action"
FINALLY="${OUTPUT_DIR}/finally"
CATALOG="${WORK_DIR}/catalog"
TAG="${WORK_DIR}/tag"
FLAG="${BASE_DIR}/makeindex_flag"

################# makeindex ###########
MAKEINDEX_DIR="./"
SE_INDEX_CONF="/home/meihua/jinkaifeng/github/se/output/conf/index.conf"
SE_VERSION_FILE="/home/meihua/jinkaifeng/github/se/output/var/version"
