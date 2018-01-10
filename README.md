# infoq_crawler
infoQ 文章区爬虫，批量抓取 infoQ 文章相关信息并发布到我的个人社区。
## 演示
![演示图片](https://github.com/enincc/infoq_crawler/blob/master/crawler.gif)
## crawler.py
爬虫模块，依赖 PyQuery 和 Requests 2个模块。支持缓存，节省了二次抓取的时间。
## post.py
发布模块，通过在请求中添加 Cookie 模拟登录状态，批量提交表单到我的[个人社区](https://github.com/enincc/myBBS)。

使用前需要在 `config.py` 中修改 Cookie、Token 及发布地址。
