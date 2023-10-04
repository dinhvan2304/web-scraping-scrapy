# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from datetime import datetime
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


class MasothueCrawlPipeline:
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
        # run the db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        # d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        # d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        d.addCallback(self._handle_error)

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""

        if item["mst"]:
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

            #conn.execute(
            #    """
            #        INSERT INTO temp_clients(mst) VALUES(%s)
            #    """,
            #    (item["mst"],),
            #)

        return item

    def _handle_error(self, failure):
        """Handle occurred on db interaction."""
        # do nothing, just log
        print(failure)
