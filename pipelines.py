class CsvByCategoryPipeline(object):  #
    
    stats_name = 'csvbycategory_pipeline'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.stats.set_value('done', 0)
        self.settings = crawler.settings
        self.files = {}
        self.export_dict = {}
    
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.export_dict.values()]
        [f.close() for f in self.files.values()]


    @defer.inlineCallbacks
    def process_item(self, item, spider):
        if not item['category']:
            logger.info("Not category in item")
            return
        file_name = slugify(file_name)

        if file_name not in self.export_dict:
            file = open(f'{file_name}.csv', 'w+b')
            exporter = CsvItemExporter(file)
            exporter.start_exporting()
            self.export_dict[file_name] = exporter
            self.files[file_name] = file
        else:
            exporter = self.export_dict[file_name]
        
        self.stats.inc_value('done')
        
        exporter.export_item(item)
        if self.stats.get_value('done') % 10 == 0:
            logger.info("--> Done %s/ %s", self.stats.get_value('done'), self.stats.get_value('total'))
        yield item
        
        
