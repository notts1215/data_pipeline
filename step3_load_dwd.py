# -- coding: utf-8 --
"""
@Time : 2022/7/10 16:13
@Author : Notts XIANG
@Description : parse the ODS value and separate them into columns respectively
"""
import argparse
from pyspark.sql import SparkSession

class HiveBasic():
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("DWD IMAGE PROCESSING TEST") \
            .config("hive.metastore.uris", "thrift://sz-hd-02:9083") \
            .config("spark.sql.shuffle.partitions", "1") \
            .enableHiveSupport() \
            .getOrCreate()
        self.tableName = "test.dwd_test_image_processing_di"

    def createTable(self):
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS {self.tableName} (
                filename STRING,
                md5 STRING,
                width INT,
                height INT,
                face_no INT
            ) PARTITIONED BY (imp_date STRING)
            STORED AS PARQUET 
            TBLPROPERTIES ('parquet.compress'='SNAPPY')
        """)

    def rePartition(self, imp_date):
        self.spark.sql(f"ALTER TABLE {self.tableName} DROP IF EXISTS PARTITION (imp_date='{imp_date}')")
        self.spark.sql(f"ALTER TABLE {self.tableName} ADD PARTITION (imp_date = '{imp_date}')")

    def write2Hive(self, imp_date):
        self.spark.sql(f"""
            INSERT INTO TABLE {self.tableName} PARTITION(imp_date='{imp_date}')
            SELECT /*+ COALESCE(1) */ filename,
                    get_json_object(image_info_json, '$.md5') AS md5,
                    get_json_object(image_info_json, '$.width') AS width,
                    get_json_object(image_info_json, '$.height') AS height,
                    get_json_object(image_info_json, '$.face_no') AS face_no
            FROM test.ods_test_image_processing_di
            WHERE imp_date = '{imp_date}'
        """)


if __name__ == '__main__':
    def parse_arg():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i1", "--input1", required=True, help="Please Input the date time")
        args = parser.parse_args()
        return args.input1

    def main():
        imp_date = str(parse_arg())
        HB = HiveBasic()
        HB.createTable()
        HB.rePartition(imp_date)
        HB.write2Hive(imp_date)

    main()
