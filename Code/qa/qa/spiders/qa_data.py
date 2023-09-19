import scrapy
from scrapy import Request
from qa.items import QaItem
class QaDataSpider(scrapy.Spider):
    name = 'qa_data'
    allowed_domains = ['www.chunyuyisheng.com']
    # start_urls = ['https://www.chunyuyisheng.com/pc/search/qalist/']
    def start_requests(self):
        symptom_qwds = ['症状', '表征', '现象', '症候', '表现', '不良反应','征兆']
        cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何',
                        '如何才会', '怎么才会', '会导致', '会造成']
        acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现',
                            '伴随发生', '伴随', '共现']
        not_food_qwds = ['不能吃什么','忌口','不能吃什么食物','不能吃什么东西','忌食','少吃']
        can_food_qwds = ['吃什么食物','怎么补','吃什么菜','保健品','食谱','宜食','多吃']
        drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开',
                            '避掉', '躲开', '躲掉', '绕开',
                            '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                            '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                            '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                            '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时',
                            '多少年']
        cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法',
                            '咋治', '怎么办', '咋办', '咋治']
        cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性',
                            '能治', '可治', '可以治', '可以医']
        easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        question_type = [symptom_qwds, cause_qwds, acompany_qwds, not_food_qwds, can_food_qwds, drug_qwds, check_qwds, prevent_qwds, lasttime_qwds, cureway_qwds, cureprob_qwds, easyget_qwds]
        for i in question_type:
            for j in i:
                for z in range(1,10):
                    yield Request(url = ('https://www.chunyuyisheng.com/pc/search/qalist/'+ '?query=' + str(j) + '&page=' + str (z)))
    def get_str(self,data):
        """格式化输出"""
        return data.strip().replace('问</i>', '').replace('\t', '').replace('\n', '').replace(
                '<i class="ask-tag answer-tag">答</i>', '').replace('<span class=\'s-hl\'>', '').replace('</span>', '')
    def parse(self, response):
        question = response.xpath('//div[@class = "qa-item qa-item-ask"]//a/text()').extract()
        answer = response.xpath('//div[@class = "qa-item qa-item-answer"]/text()').extract()
        question = [item for item in question if item != '\n\t\t\t\t\t']
        answer = [item for item in answer if item != '\n\t\t\t\t']
        for a,b in zip(question,answer):
            qa_data = QaItem()
            qa_data['question'] = self.get_str(a)
            qa_data['answer'] = self.get_str(b)
            yield qa_data
