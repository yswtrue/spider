#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-05-11 23:51:07
# Project: company_spider

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'timeout': 10,
        'retries': 3,
    }

    def on_start(self):
        self.crawl('http://b2b.huangye88.com/shenzhen/',
                   callback=self.list_page)

    @config(age=0)
    def list_page(self, response):
        for each in response.doc('#subcatlisting_10 a[href^="http"]').items():
            type = each.text()
            self.crawl(each.attr.href, callback=self.list_detail,
                       save={'type': type})

    @config(age=0)
    def list_detail(self, response):
        for each in response.doc('.mach_list2 form dl[itemtype="http://data-vocabulary.org/Organization"]').items():
            title = each('h4 a[href^="http"]').text()
            tel = each('span[itemprop="tel"] a[href^="http"]').text()
            detail_url = each('span[itemprop="tel"] a[href^="http"]').attr.href
            self.crawl(detail_url, callback=self.detail_page, save={
                       'title': title, 'tel': tel, 'type': response.save['type']})

    @config(age=0)
    def detail_page(self, response):
        ul = response.doc('ul.con-txt')
        name = ''
        address = ''
        tel = response.save['tel']
        for each in ul.items('li'):
            label = each('label').text()
            if '联系人' in label:
                name = each.text().replace('联系人：', '').strip()
            if '地址' in label:
                address = each.text().replace('地址：', '').strip()
            if '手机' in label:
                tel = each.text().replace('手机：', '').strip()

        return {
            "url": response.url,
            "company_name": response.save['title'],
            "type": response.save['type'],
            "name": name,
            "address": address,
            "tel": tel,
        }
