import requests
from lxml import html


class Model(object):
    def __repr__(self):
        """
         规定输出的格式
        """
        class_name = self.__class__.__name__
        properties = (u'{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{}:\n  {}\n>'.format(class_name, u'\n  '.join(properties))
        return r


class Movie(Model):
    def __init__(self):
        """
         用一个 class 保存要抓取的对象
         初始化需要爬取的类的属性
        """
        super(Movie, self).__init__()
        self.ranking = 0
        self.cover_url = ''
        self.name = ''
        self.staff = ''
        self.publish_info = ''
        self.rating = 0
        self.quote = ''
        self.number_of_comments = 0


def save(data):
    """
     以 txt 格式保存爬取的信息
    """
    data = str(data)
    path = 'doubanTop250.txt'
    with open(path, 'a', encoding='utf-8') as f:
        f.write(data)


def add_quote(div):
    """
     不是每部电影都有 quote
     额外判断
    """
    if div.xpath('.//span[@class="inq"]'):
        quote = div.xpath('.//span[@class="inq"]')[0].text
    else:
        quote = ''
    return quote


def movie_from_div(div):
    """
     XPath 解析网页 body
     存储到指定的类里
    """
    movie = Movie()
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@src')
    names = div.xpath('.//span[@class="title"]/text()')
    movie.name = ''.join(names)
    movie.rating = div.xpath('.//span[@class="rating_num"]')[0].text
    movie.quote = add_quote(div)
    infos = div.xpath('.//div[@class="bd"]/p/text()')
    movie.staff, movie.publish_info = [i.strip() for i in infos[:2]]
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    return movie


def movies_from_url(url):
    """
     封装使用的库
     调用这个函数只需要传入要爬取的 url
     返回爬虫的结果
    """
    page = requests.get(url)
    root = html.fromstring(page.content)
    movie_divs = root.xpath('//div[@class="item"]')
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def main():
    """
     启动的主函数
     这里包括翻页功能
     根据 query 的参数做循环
    """
    url = 'https://movie.douban.com/top250?start='
    for i in range(10):
        u = url + str(i * 25)
        movies = movies_from_url(u)
        save(movies)
        print(movies)


if __name__ == '__main__':
    main()
