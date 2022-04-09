# 如何设置

1. 首先需要抓包环境，charles，公司有买这个，可以邮件里找找。
2. 需要python环境，最好是最新版本。 https://www.python.org/downloads/macos/ mac请使用最新的3.10.x版本
3. python库只依赖 `pip install requests`，原版本还有微信通知和声音效果，我这里都去掉了。可以去看原版本 https://gist.github.com/0xKira/87cc84e7eddc462719f3e8f3e6a3728e
4. 开发环境PyCharm即可
5. 注意抓好包记得关掉charles的mac proxy，否则影响mac上网
6. 和原版本区别还有就是注释了request和下单的sleep （根据飙哥的建议）

另外就是要先测试，下午时段可以买葱试试，有问题和一起探讨。

祝好运

# 运行

使用了module，在根目录需要如下运行
`python -m src.mini.dingdong`


# 抓包设置
可以参考这个 https://www.jianshu.com/p/468e2905a3e1， 设置起来需要花费点时间

1. mac上安装证书，打开mac proxy
2. 手机上连上mac的代理地址，安装证书
3. 测试



# 实战的log
```buildoutcfg
(venv3) ➜  Lver git:(main) ✗ python -m src.mini.dingdong
04.09 08:29:55: 更新配送站信息...
04.09 08:29:55: 获取购物列表...
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:55: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": []}
04.09 08:29:56: NOTIFY -> 需购买商品数：14，总价：144.88，配送费：0.0

【产地特色】金坛水芹 350g/份: 9.90 * 1 元
大娃娃菜（黄心） 1.5kg/份: 16.90 * 1 元
胭脂红蜜薯 750g/袋: 11.90 * 1 元
【产地特色】滕州土豆 约500g: 4.99 * 1 元
崇明西葫芦 350g/份: 9.50 * 1 元
日本桃太郎粉番茄 600g/份: 9.90 * 1 元
【高原鲜】高原豆王 约300g: 12.90 * 1 元
【春菜】芦笋 350g/份: 12.80 * 1 元
【高原鲜】高原油麦菜 约500g: 6.99 * 1 元
【春菜】菠菜苗 250g/份: 9.50 * 1 元
崇明番茄 450g/份: 10.90 * 1 元
【叮咚自营农场】苏州青 300g/份: 5.90 * 1 元
崇明大叶蓬蒿菜 300g/份: 9.90 * 1 元
崇明水果黄瓜 500g/份: 12.90 * 1 元
04.09 08:29:56: 获取配送时间...
04.09 08:29:57: 总配送时间数：4，可配送时间数：0
04.09 08:29:57: 获取配送时间...
04.09 08:29:57: 总配送时间数：1，可配送时间数：1
04.09 08:29:57: NOTIFY -> 最近的配送时间为：自动尝试可用时段
尝试自动下单...
04.09 08:29:58: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": {}}
04.09 08:29:58: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": {}}
04.09 08:29:59: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": {}}
04.09 08:29:59: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": {}}
04.09 08:30:00: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": {}}
04.09 08:30:00: 200 {"success":false,"code":-3000,"msg":"当前人多拥挤，请稍后尝试刷新页面","data": {}}
04.09 08:30:02: {'success': True, 'code': 0, 'msg': 'success', 'data': {'pay_url': '{"timeStamp":"1649464202","package":"prepay_id=wx090830019446963177637e3052d8ea0000","appId":"wx1e113254eda17715","sign":"8010B055DA7070C72F2CB44689102A59","signType":"MD5","nonceStr":"05rw40mIxLJ2DyydryyOpy7ecTmBkcdI"}', 'pay_online': True, 'order_number': '2204094022542984155', 'cart_count': 0, 'station_id': '5c0f2468716de1e77d8b4a6d', 'event_tracking': {'post_product_algo': '{}'}}, 'tradeTag': 'success', 'server_time': 1649464202, 'is_trade': 1}
04.09 08:30:02: NOTIFY -> success
====================
04.09 08:30:02: NOTIFY -> 下单成功！快去支付吧

```