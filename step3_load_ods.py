# -- coding: utf-8 --
"""
@Time : 2022/7/9 11:34
@Author : Notts XIANG
@Description : load jsonString(info via fundamental image-processing) from previous DAG
"""
import argparse
import json
from pyspark.sql import SparkSession

class HiveBasic():
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("ODS IMAGE PROCESSING TEST") \
            .config("hive.metastore.uris", "thrift://sz-hd-02:9083") \
            .config("spark.sql.shuffle.partitions", "10") \
            .enableHiveSupport() \
            .getOrCreate()
        self.tableName = "test.ods_test_image_processing_di"

    def createTable(self):
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS {self.tableName} (
                filename STRING COMMENT 'primary key, each filename is unique in this case (alternatively using md5)',
                image_info_json STRING
            ) PARTITIONED BY (imp_date STRING)
            STORED AS PARQUET 
            TBLPROPERTIES ('parquet.compress'='SNAPPY')
        """)

    def rePartition(self, imp_date):
        self.spark.sql(f"ALTER TABLE {self.tableName} DROP IF EXISTS PARTITION (imp_date='{imp_date}')")
        self.spark.sql(f"ALTER TABLE {self.tableName} ADD PARTITION (imp_date = '{imp_date}')")

    def write2Hive(self, imp_date, file_path):
        """
        There are several ways of loading data into a table, I list 2 of them:
            1. using external table
            2. iterate the file and insert -- not using, due to time-costs & stability.
        """
        tmp_table = f"test.ods_test_image_processing_external_{imp_date}"
        self.spark.sql(f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS {tmp_table} (
                json_string STRING
            ) ROW FORMAT DELIMITED
            FIELDS TERMINATED BY '\t'
            LOCATION '/tmp/pipeline/{imp_date}/'
        """)

        self.spark.sql(f"""
            INSERT INTO TABLE {self.tableName} PARTITION (imp_date='{imp_date}')
            SELECT /*+ COALESCE(1) */ get_json_object('json_string', '$.field_name') AS field_name, json_string
            FROM {tmp_table}
        """)

        self.spark.sql(f"""DROP TABLE IF EXISTS {tmp_table}""")

        """
        Method2
        """
        # with open(file_path, 'r') as fw:
        #     lines = fw.readlines()  # is a list
        #     for line in lines:
        #         line = line.strip("\n")
        #         file_name = json.loads(line)["file_name"]
        #         self.spark.sql(f"""INSERT INTO TABLE {self.tableName} PARTITION (imp_date='{imp_date}')
        #                         SELECT '{file_name}', '{line}' """)


if __name__ == '__main__':
    # define the general submit command format:  e.g. spark-submit ....... -i1 20220709
    def parse_arg():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i1", "--input1", required=True, help="Please Input the date time")
        args = parser.parse_args()
        return args.input1

    def main():
        imp_date = str(parse_arg())
        file_path = f"/..../{imp_date}/result.json"     # The path varies from date
        HB = HiveBasic()
        HB.createTable()
        HB.rePartition(imp_date)
        HB.write2Hive(imp_date, file_path)

    main()


