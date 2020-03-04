import requests,json,re
from lxml import etree
from urllib import parse

def get_conent(url,headers):
    '''
    :param url: request url
    :param headers:
    :return: python list or json
    '''
    response = requests.get(url,headers=headers)
    return response.text

def parse_json(json_data):
    item = {}
    for data in json_data:
        rating = data['rating']
        imag = data['cover_url']
        title = data['title']
        actors = data['actors']
        detail_url = data['url']
        vote_count = data['vote_count']
        types = data['types']
        item['rating'] = rating
        item['imag'] = imag
        item['title'] = title
        item['actors'] = actors
        item['vote_count'] = vote_count
        item['detail_url'] = detail_url
        item['types'] = types
        print(item)

def parse_ajax(url,type_,refer):
    headers = {
        'X-Requseted-With': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Matintosh; Inter Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
        'Referer': refer,
    }
    i=0
    while True:
        json_str = get_conent(url.format(type_,i), headers=headers)
        print(json_str)
        if json_str == '[]':
            break
        json_data = json.loads(json_str)
        parse_json(json_data)
        i += 100

def main():
    base_url = 'https://movie.douban.com/chart'
    headers={
        'Referer': 'https://movie.douban.com/',
        'user-agent': 'Mozilla/5.0 (Matintosh; Inter Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    }
    html_str = get_conent(base_url,headers)
    html = etree.HTML(html_str)
    type_urls = html.xpath('//div[@class="types"]/span/a/@href')
    for url in type_urls:
        p = re.compile(r'.*?type_name=(.*?)&type=(.*?)&interval.*?')
        result = p.search(url)
        type_name = result.group(1)
        type_ = result.group(2)
        params = {
            'type_name': type_name,
            'type': type_,
            'interval_id': '100:90',
            'action': '',
        }
        refer = 'https://movie.douban.com/j/chart/top_list?'+parse.urlencode(params)
        ajax_url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=100'
        parse_ajax(ajax_url,type_,refer)

if __name__ == '__main__':
    main()
