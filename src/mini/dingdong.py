# -*- coding: utf-8 -*-
import requests
import time
from urllib.parse import unquote
import datetime
import json
import traceback

# /order/getMultiReserveTime 抓包获得以下参数
uid = ""
s_id = ""
device_id = ""
device_token = unquote("")
# 以下会随地址而变化
# longitude = "121.431275"  # 经度
# latitude = "31.350273"  # 纬度
# address_id = "624e236fe51a800001b7e154"  # 收货地址


address = {  # yangpu
        'latitude': "31.309978",
        'longitude': "121.490968",
        'station_id': '5c0f2468716de1e77d8b4a6d',
        'city_number': '0101',
        'address_id': '624fde1837ba6a0001ff15fd'
    }

latitude = address['latitude'] #"31.309978"
longitude = address['longitude']
address_id = address['address_id']

HOST = "maicai.api.ddxq.mobi"
base_url = f"https://{HOST}"
cookie = f"DDXQSESSID={s_id}"

pub_headers = {
    "Host": HOST,
    "Connection": "close",
    "cookie": cookie,
    "ddmc-longitude": longitude,
    "content-type": "application/x-www-form-urlencoded",
    "ddmc-city-number": "0101",
    "ddmc-build-version": "2.81.4",
    "ddmc-ip": "",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123c) NetType/WIFI Language/zh_CN",
    "Accept-Encoding": "gzip, deflate",
    "ddmc-app-client-id": "4",
    "ddmc-station-id": "",
    "ddmc-latitude": latitude,
    "ddmc-channel": "applet",
    "ddmc-os-version": "[object Undefined]",
    "charset": "utf-8",
    "ddmc-api-version": "9.48.0",
    "ddmc-device-id": device_id,
    "ddmc-uid": uid,
    "Referer": "https://servicewechat.com/wx1e113254eda17715/421/page-frame.html",
}

pub_request_params = {
    "uid": uid,
    "longitude": longitude,
    "latitude": latitude,
    "station_id": "",
    "city_number": "",
    "api_version": "9.48.0",
    "app_version": "2.80.6",
    "applet_source": "",
    "channel": "applet",
    "app_client_id": "4",
    "sharer_uid": "",
    "s_id": s_id,
    "openid": device_id,
    "h5_source": "",
    "device_token": device_token,
}

cart_products = []
package_order = None

apis = {
    'order_reserve_time': f'{base_url}/order/getMultiReserveTime',
    'add_order': f'{base_url}/order/addNewOrder',
    'cart': f'{base_url}/cart/index',
}


def log(s):
    now = datetime.datetime.now().strftime("%m.%d %H:%M:%S")
    print(f"{now}: {s}")


def notify_self(info: str):
    log(f'NOTIFY -> {info}')


def do_request(typ: str, url: str, headers: dict, data: dict) -> dict:
    # 网络拥堵时一直重试，处理非200响应 && timeout && 以下error类型：
    # {'code': 250100901, 'msg': '叮咚去邻居家串门了，马上回来哈～', 'success': False, 'timestamp': '2022-03-29 06:19:18'}
    # {'success': False, 'code': -3000, 'msg': '当前人多拥挤，请稍后尝试刷新页面', 'data': []}
    # {'success': False, 'code': -3001, 'msg': '当前人多拥挤，请稍后尝试刷新页面', 'tips': {'duration': 300, 'limitMsg': '前方拥挤，请稍后再试...'}, 'barrier': {'passRatio': 0.5, 'maxCount': 5}, 'data': {}}
    while True:
        try:
            if typ == "POST":
                r = requests.post(url=url, headers=headers, data=data, timeout=3)
            else:  # "GET"
                r = requests.get(url=url, headers=headers, params=data, timeout=3)
        except requests.exceptions.Timeout:
            log("Request timeout!\n")
            time.sleep(1)
            continue
        ERR_CODES = [250100901, -3000, -3001]
        if r.status_code != 200 or (
            not (resp := r.json())["success"] and resp["code"] in ERR_CODES
        ):
            # time.sleep(2)
            log(f"{r.status_code} {r.text}")
        else:
            break
    return resp

def update_location_info(config=None):
    global pub_headers, pub_request_params
    log("更新配送站信息...")
    if config is None:
        r = requests.get(
            url="https://sunquan.api.ddxq.mobi/api/v2/user/location/refresh/",
            params={"longitude": config['longitude'], "latitude": config['latitude']},
        )
        data = r.json()["data"]
        station_id = data["station_id"]
        city_number = data["city_number"]
        pub_headers["ddmc-station-id"] = station_id
        pub_headers["ddmc-city-number"] = city_number
        pub_request_params["station_id"] = station_id
        pub_request_params["city_number"] = city_number
    else:
        pub_headers["ddmc-station-id"] = config['station_id']
        pub_headers["ddmc-city-number"] = config['city_number']
        pub_headers["ddmc-longitude"] = config['longitude']
        pub_headers["ddmc-latitude"] = config['latitude']

        pub_request_params["station_id"] = config['station_id']
        pub_request_params["city_number"] = config['city_number']
        pub_request_params["longitude"] = config['longitude']
        pub_request_params["latitude"] = config['latitude']


def check_delivery_time(addr=None) -> list:
    log('获取配送时间...')
    address = address_id
    if addr:
        address = addr['address_id']
    resv_time_url = base_url + "/order/getMultiReserveTime"
    resp = do_request(
        "POST",
        url=resv_time_url,
        headers=pub_headers,
        data={
            **pub_request_params,
            "products": json.dumps(cart_products),
            "address_id": address,
        },
    )

    if not resp["success"]:
        log(resp)
        return []

    if len(resp["data"]) == 0:
        log('Error: no available times')
        return []

    avail_times = []
    count = 0
    days = resp["data"][0]["time"]
    for day in days:
        for t in day["times"]:
            count += 1
            if not t["fullFlag"]:
                avail_times.append(t)
    # avail_times.append(days[0]["times"][0])  # debug code, disable in production
    log(f"总配送时间数：{count}，可配送时间数：{len(avail_times)}")
    return avail_times


def new_order() -> dict:
    new_order_url = base_url + "/order/addNewOrder"
    resp = do_request(
        "POST",
        url=new_order_url,
        headers=pub_headers,
        data={
            **pub_request_params,
            "products": json.dumps(cart_products),
            "package_order": json.dumps(package_order),
        },
    )
    log(resp)
    return resp


def update_product_from_cart():
    log('获取购物列表...')
    global cart_products, package_order
    cart_url = base_url + "/cart/index"
    resp = do_request(
        "GET",
        url=cart_url,
        headers=pub_headers,
        data={
            **pub_request_params,
            "is_load": 1,
        },
    )

    if resp["code"] != 0:
        log("Error: no products in cart!!")
        return

    copy_keys = [
        "id",
        "parent_id",
        "count",
        "cart_id",
        "price",
        "product_type",
        "is_booking",
        "product_name",
        "small_image",
        "sale_batches",
        "order_sort",
        "sizes",
    ]
    packages_products = []
    if len(resp["data"]["new_order_product_list"]) == 0:
        log("Error: 购物车内无有效选中商品!!")
        exit()
    product_to_buy = resp["data"]["new_order_product_list"][0]  # 选中的商品
    for i in product_to_buy["products"]:
        item = {k: i[k] for k in copy_keys}
        packages_products.append(item)
    total_money = float(product_to_buy["total_money"])
    order_freight = 0 if total_money < 39.0 else 0.0
    product_to_buy["total_money"] = "%.2f" % (total_money + order_freight)
    notify_self(
        f'需购买商品数：{len(packages_products)}，总价：{product_to_buy["total_money"]}，配送费：{order_freight}\n\n'
        + "\n".join(f"{i['product_name']}: {i['price']} * {i['count']} 元" for i in product_to_buy["products"])
    )

    cart_products = [product_to_buy["products"]]
    package_order = {
        "payment_order": {
            "reserved_time_start": 0xDEADBEEF,
            "reserved_time_end": 0xDEADBEEF,
            "price": product_to_buy["total_money"],
            "freight_discount_money": "5.00",
            "freight_money": "5.00",
            "order_freight": "%.2f" % order_freight,
            "parent_order_sign": resp["data"]["parent_order_info"]["parent_order_sign"],
            "product_type": 1,
            "address_id": address_id,
            "form_id": "41414141",
            "receipt_without_sku": None,
            "pay_type": 6,
            "vip_money": "",
            "vip_buy_user_ticket_id": "",
            "coupons_money": "",
            "coupons_id": "",
        },
        "packages": [
            {
                "products": packages_products,
                "total_money": product_to_buy["total_money"],
                "total_origin_money": product_to_buy["total_origin_money"],
                "goods_real_money": product_to_buy["goods_real_money"],
                "total_count": product_to_buy["total_count"],
                "cart_count": product_to_buy["cart_count"],
                "is_presale": 0,
                "instant_rebate_money": "0.00",
                "total_rebate_money": "0.00",
                "used_balance_money": "0.00",
                "can_used_balance_money": "0.00",
                "used_point_num": 0,
                "used_point_money": "0.00",
                "can_used_point_num": 0,
                "can_used_point_money": "0.00",
                "is_share_station": 0,
                "only_today_products": [],
                "only_tomorrow_products": [],
                "package_type": 1,
                "package_id": 1,
                "front_package_text": product_to_buy["front_package_text"],
                "front_package_type": 0,
                "front_package_stock_color": "#2FB157",
                "front_package_bg_color": "#fbfefc",
                "eta_trace_id": "164801176300561566978",
                "reserved_time_start": 0xDEADBEEF,
                "reserved_time_end": 0xDEADBEEF,
                "soon_arrival": 0xDEADBEEF,
                "first_selected_big_time": 0,
            }
        ],
    }


#########

def main(retry_avail_times=0, address=None):
    update_location_info(config=address)
    update_product_from_cart()
    retry_count = 0
    retry_cnt_avail_times = 0
    while True:
        try:
            avail_times = check_delivery_time(address)
            if len(avail_times) > 0:
                fastest = avail_times[0]
                notify_self(f'最近的配送时间为：{fastest["select_msg"]}\n尝试自动下单...')
                time_start = fastest["start_timestamp"]
                time_end = fastest["end_timestamp"]
                package_order["payment_order"]["reserved_time_start"] = time_start
                package_order["payment_order"]["reserved_time_end"] = time_end
                package_order["packages"][0]["reserved_time_start"] = time_start
                package_order["packages"][0]["reserved_time_end"] = time_end
                package_order["packages"][0]["soon_arrival"] = (
                    1 if fastest["arrival_time"] else ""
                )
                resp = new_order()
                notify_self(resp["msg"])
                # {'success': False, 'code': 1, 'msg': '参数错误', 'data': [], 'tradeTag': 'success', 'server_time': 1648567550, 'is_trade': 1}
                if resp["success"]:
                    print("====================")
                    notify_self("下单成功！快去支付吧")
                    break

                match resp.get("tradeTag"):
                    case "NOTE_ORDER_SPECIAL":  # 暂未营业，请6点后再试。
                        break
                    # 有商品缺货；商品总价错误；商品信息有变化，请重新下单
                    case "PRODUCT_OUT_OF_STOCK" | "WRONG_TOTAL_PRICE" | "PRODUCT_INFO_HAS_CHANGED":
                        update_product_from_cart()
                        continue
                    case "TIME_DELIVERY":  # 您选择的送达时间已经失效了，请重新选择
                        continue
                    case "FLAG":  # 操作太频繁，请返回购物车稍后重试。
                        pass
                    case "ADDRESS_DELIVERY":  # 此地址不在配送范围内
                        pass
                    case None:
                        log(f"no tradeTag found\n{resp}")
                    case _:
                        log(f"unhandled case\n{resp}")
            else:
                retry_cnt_avail_times += 1
                if 0 < retry_avail_times < retry_cnt_avail_times:
                    log('Error: retry too many times, cannot get available times')
                    break
            # time.sleep(3)
            retry_count = 0
        except Exception:
            notify_self("Error!\n" + traceback.format_exc())
            retry_count += 1
            if retry_count > 5:
                notify_self("fail too many times")
                break
            time.sleep(30)


if __name__ == '__main__':
    main(address=address)
    # update_location_info(config=address)
    # update_product_from_cart()
    # check_delivery_time(address)
