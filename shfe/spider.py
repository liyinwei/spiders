#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2017/4/16 13:26
@Description: 从上海期货官网爬取所有期货日交易数据（Since 20020107）
"""

import urllib
import urllib.request
import json
import datetime
import time
import mysql.connector


def generate_date_lists(start, end):
    """
    根据开始日期和结束日期返回待采集的日期列表
    """
    start_date = datetime.datetime.strptime(start, '%Y%m%d')
    end_date = datetime.datetime.strptime(end, '%Y%m%d')
    result = [start]
    for i in range((end_date - start_date).days):
        result.append((start_date + datetime.timedelta(days=i + 1)).strftime('%Y%m%d'))
    return result


def get_response(exchange_date):
    """
    根据日期返回当天的期货数据
    """
    url = "http://www.shfe.com.cn/data/dailydata/kx/kx" + exchange_date + ".dat"
    try:
        f = urllib.request.urlopen(url)
        if f.getcode() == 200:
            response = f.read()
            response = response.decode('UTF-8')
            dict_data = json.loads(response)
            return dict_data
        else:
            print(date + " response abnormal code:" + f.getcode())
    except Exception as e:
        print(date + " response exception: " + str(e))
    return None


def format_response(response):
    """
    对爬取的Json数据进行格式化，便于直接存入数据库 
    """
    if response is not None and response != "" and response.get("o_curproduct") is not None:
        # o_curproduct
        cur_product = {}
        for val in response.get("o_curproduct"):
            cur_product[val.get("PRODUCTID")] = str(val)

        # o_curmetalindex （20121226日之前没有这部分数据）
        index_value = response.get("o_curmetalindex")[0] if len(response.get("o_curmetalindex")) > 0 else None

        # o_curinstrument
        formated_list = []
        for val in response.get("o_curinstrument"):
            formated = [None,
                        # detail["o_IMChangeDate"],
                        response.get("report_date"),

                        # o_curinstrument
                        val.get("PRODUCTID").strip(),
                        val.get("PRODUCTSORTNO"),
                        val.get("PRODUCTNAME").strip(),
                        val.get("DELIVERYMONTH"),
                        val.get("PRESETTLEMENTPRICE") if val.get("PRESETTLEMENTPRICE") != '' else None,
                        val.get("OPENPRICE") if val.get("OPENPRICE") != '' else None,
                        val.get("HIGHESTPRICE") if val.get("HIGHESTPRICE") != '' else None,
                        val.get("LOWESTPRICE") if val.get("LOWESTPRICE") != '' else None,
                        val.get("CLOSEPRICE") if val.get("CLOSEPRICE") != '' else None,
                        val.get("SETTLEMENTPRICE") if val.get("SETTLEMENTPRICE") != '' else None,
                        val.get("ZD1_CHG") if val.get("ZD1_CHG") != '' else None,
                        val.get("ZD2_CHG") if val.get("ZD2_CHG") != '' else None,
                        val.get("VOLUME") if val.get("VOLUME") != '' else None,
                        val.get("OPENINTEREST") if val.get("OPENINTEREST") != '' else None,
                        val.get("OPENINTERESTCHG") if val.get("OPENINTERESTCHG") != '' else None,
                        val.get("ORDERNO"),

                        # o_curproduct（20160707 agefp异常）
                        eval(cur_product.get(val.get("PRODUCTID"))).get("HIGHESTPRICE") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("HIGHESTPRICE") != '' else None,

                        eval(cur_product.get(val.get("PRODUCTID"))).get("LOWESTPRICE") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("LOWESTPRICE") != '' else None,

                        eval(cur_product.get(val.get("PRODUCTID"))).get("AVGPRICE") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("AVGPRICE") != '' else None,

                        eval(cur_product.get(val.get("PRODUCTID"))).get("VOLUME") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("VOLUME") != '' else None,

                        eval(cur_product.get(val.get("PRODUCTID"))).get("TURNOVER") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("TURNOVER") != '' else None,

                        eval(cur_product.get(val.get("PRODUCTID"))).get("YEARVOLUME") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("YEARVOLUME") != '' else None,

                        eval(cur_product.get(val.get("PRODUCTID"))).get("YEARTURNOVER") if cur_product.get(
                            val.get("PRODUCTID")) is not None and eval(
                            cur_product.get(val.get("PRODUCTID"))).get("YEARTURNOVER") != '' else None,

                        # o_curmetalindex
                        index_value.get("TRADINGDAY") if index_value is not None and index_value.get(
                            "TRADINGDAY") != '' else None,
                        index_value.get("LASTPRICE") if index_value is not None and index_value.get(
                            "LASTPRICE") != '' else None,
                        index_value.get("OPENPRICE") if index_value is not None and index_value.get(
                            "OPENPRICE") != '' else None,
                        index_value.get("CLOSEPRICE") if index_value is not None and index_value.get(
                            "CLOSEPRICE") != '' else None,
                        index_value.get("PRECLOSEPRICE") if index_value is not None and index_value.get(
                            "PRECLOSEPRICE") != '' else None,
                        index_value.get("UPDOWN") if index_value is not None and index_value.get(
                            "UPDOWN") != '' else None,
                        index_value.get("UPDOWN1") if index_value is not None and index_value.get(
                            "UPDOWN1") != '' else None,
                        index_value.get("UPDOWN2") if index_value is not None and index_value.get(
                            "UPDOWN2") != '' else None,
                        index_value.get("HIGHESTPRICE") if index_value is not None and index_value.get(
                            "HIGHESTPRICE") != '' else None,
                        index_value.get("LOWESTPRICE") if index_value is not None and index_value.get(
                            "LOWESTPRICE") != '' else None,
                        index_value.get("AVGPRICE") if index_value is not None and index_value.get(
                            "AVGPRICE") != '' else None,
                        index_value.get("SETTLEMENTPRICE") if index_value is not None and index_value.get(
                            "SETTLEMENTPRICE") != '' else None,

                        # others
                        response.get("o_year"),
                        response.get("o_month"),
                        response.get("o_day"),
                        response.get("o_weekday"),
                        response.get("o_year_num"),
                        response.get("o_total_num"),
                        response.get("o_trade_day"),
                        response.get("o_IMChangeDate"),
                        response.get("o_code"),
                        response.get("o_msg"),
                        response.get("report_date"),
                        time.strptime(response.get("update_date"), '%Y%m%d %H:%M:%S'),
                        time.strptime(response.get("print_date"), '%Y%m%d %H:%M:%S')
                        ]
            formated_list.append(formated)
        return formated_list
    return None


def save(data):
    """
    将格式化后的爬取的数据保存至MySQL数据库 
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE,
                                       use_unicode=True)
        cursor = conn.cursor()
        cursor.executemany(
            'INSERT INTO shfe_daily VALUES ('
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            data)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    # 每批次存入数据库的天数大小
    BATCH_SIZE = 100
    # 爬取开始日期
    START_DATE = "20020107"
    # 爬取结束日期
    END_DATE = "20170524"
    # MySQL host
    HOST = 'mysqlhost'
    # MySQL username
    USER = 'cvte'
    # MySQL password
    PASSWORD = 'cvte@cvte'
    # MySQL database name
    DATABASE = 'dataset'
    # 获取待爬取的日期列表
    date_list = generate_date_lists(START_DATE, END_DATE)
    print(date_list)
    response_list = []
    count = 0
    for date in date_list:
        print(date)
        formated_response = format_response(get_response(date))
        if formated_response is not None and formated_response != '':
            response_list.extend(formated_response)
        if len(response_list) > BATCH_SIZE:
            count += len(response_list)
            save(response_list)
            response_list.clear()
            print("transaction completed, total data counts: " + str(count))
    count += len(response_list)
    save(response_list)
    response_list.clear()
    print("transaction completed, total data counts: " + str(count))
