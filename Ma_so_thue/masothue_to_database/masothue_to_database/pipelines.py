# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from datetime import datetime
import mysql.connector


TYPE_UPDATE = 0
TYPE_INSERT = 1

class MasothueToDatabasePipeline:
    def __init__(self, dbpool):
        self.dbpool = dbpool
        
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset="utf8mb4",
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbargs)
        return cls(dbpool)
    
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addCallback(self._handle_error)
    
    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""

        if item["mst"]:
            if item["append_type"] == TYPE_INSERT:
                conn.execute(
                    """
                        INSERT INTO clients(province, province_code, vi_name, en_name, mst, city, street, district, location, phone, telco, manager_name, created_date, main_business, main_business_code, enterprise_type, status, business) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s,%s, %s,%s)
                    """,
                    (item["province"],
                    item["province_code"], 
                    item["vi_name"],
                    item["en_name"], 
                    item["mst"],
                    item["city"], 
                    item["street"],
                    item["district"], 
                    item["location"],
                    item["phone"], 
                    item["telco"],
                    item["manager_name"], 
                    item["created_date"],
                    item["main_business"], 
                    item["main_business_code"],
                    item["enterprise_type"], 
                    item["status"],
                    item["business"],),
                )

            elif item["append_type"] == TYPE_UPDATE:
                conn.execute(
                    """
                        UPDATE clients SET main_business=%s, main_business_code=%s WHERE mst=%s
                    """,
                    (
                    item["main_business"], 
                    item["main_business_code"],
                    item["mst"],),
                )
                
        return item

    def _handle_error(self, failure):
        """Handle occurred on db interaction."""
        # do nothing, just log
        print(failure)
