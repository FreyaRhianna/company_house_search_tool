import scrapy


class BySicSpider(scrapy.Spider):
    name = "bysic"

    ##INPUT HERE THE SIC CODES AND LOCATIONS YOU WANT TO SEARCH ##
    sicCodes = ["62020", "72200"]
    cities = ["Swansea", "Cardiff"]
    urls = []
    for city in cities:
        urls.append("https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?registeredOfficeAddress=" + city + "&sicCodes=" + sicCodes[0] + "&status=active&page=1")

    for code in sicCodes:
        searchCodes = "and contains(.," + code + ")"

    def start_requests(self):
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }



        url = 'https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?registeredOfficeAddress=Swansea&sicCodes=' + self.sicCodes[0] + '&page=1'
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        results = response.xpath('//li/a[contains(@id,"page")]/@href').extract()
        #cells = response.xpath('//td[@class="govuk-table__cell"]/p[descendant-or-self::text()]').extract()''
        cells = response.xpath('//td[@class="govuk-table__cell" and descendant-or-self::text()[contains(.,' + self.sicCodes[0] + ') ' + self.searchCodes + ']]/h2[@class="govuk-heading-m"]/a/text()').extract()
        for cell in cells:
            print(cell)
        for result in results:
            yield scrapy.Request('https://find-and-update.company-information.service.gov.uk/advanced-search/' + result)
