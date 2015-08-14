#!/user/bin/env python

import sys
import logging
import traceback
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

def update_mysql(mysql_host, mysql_port, mysql_user, mysql_passwd, mysql_db, result_list):
    conn=MySQLdb.connect(host = mysql_host, port = mysql_port, user = mysql_user, passwd = mysql_passwd, db = mysql_db, charset = 'utf8')
    cursor =conn.cursor()
    for item in result_list:
        sql="UPDATE ci_tweet SET score = %s WHERE tid = %s" % (str(item[1]), str(item[0]))
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close() 

def main():
    if len(sys.argv) != 7:
        logging.warning("cmd args error")
        exit(1)
    raw_file = sys.argv[1]
    mysql_host = sys.argv[2]
    mysql_port = int(sys.argv[3])
    mysql_user = sys.argv[4]
    mysql_passwd = sys.argv[5]
    mysql_db = sys.argv[6]

    output_list = []
    try:
        with open(raw_file, 'r') as raw_data:
            for line in raw_data:
                line_list = line.rstrip('\n').split('\t')
                output_list.append([line_list[0], line_list[3]])
        update_mysql(mysql_host, mysql_port, mysql_user, mysql_passwd, mysql_db, output_list)
    except Exception as e:
        logging.warning(traceback.format_exc())
        exit(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S')
    main()

