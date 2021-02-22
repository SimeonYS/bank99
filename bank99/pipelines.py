import sqlite3


class Bank99Pipeline:

    # Database setup
    conn = sqlite3.connect('bank99.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute("""CREATE TABLE IF NOT EXISTS `bank99`
                         (date text, title text, category text, link text, content text)""")

    def process_item(self, item, spider):
        self.c.execute("""SELECT * FROM bank99 WHERE title = ? AND date = ?""",
                       (item.get('title'), item.get('date')))
        duplicate = self.c.fetchall()
        if len(duplicate):
            return item
        print(f"New entry added at {item['link']}")

        # Insert values
        self.c.execute("INSERT INTO bank99 (date, title, category, link, content)"
                       "VALUES (?,?,?,?,?)", (item.get('date'), item.get('title'), item.get('category'), item.get('link'), item.get('content')))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

