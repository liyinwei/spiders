-- -------------------------------------------------------
-- 上海期货交易所每日交易数据表结构
-- -------------------------------------------------------
create database dataset;


DROP TABLE shfe_daily;

CREATE TABLE
IF NOT EXISTS shfe_daily (
  -- 2
  id                     INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT
  COMMENT '主键',
  price_date             DATE    NOT NULL
  COMMENT '交易日期',

  -- 主力指数(o_curinstrument)16
  product_id             VARCHAR(5) COMMENT '期货编码',
  product_sort_no        INTEGER COMMENT '未知',
  product_name           VARCHAR(10) COMMENT '期货名称',
  delivery_month         VARCHAR(4) COMMENT '交割月份',
  pre_settlement_price_i INTEGER COMMENT '前结算',
  open_price_i           INTEGER COMMENT '今开盘',
  highest_price_i        INTEGER COMMENT '最高价-主力',
  lowest_price_i         INTEGER COMMENT '最低价-主力',
  close_price_i          INTEGER COMMENT '收盘价-主力',
  settlement_price_i     INTEGER COMMENT '结算参考价-主力',
  zd1_chg                INTEGER COMMENT '涨跌1',
  zd2_chg                INTEGER COMMENT '涨跌2',
  volume_i               INTEGER COMMENT '成交手-主力',
  open_interest          INTEGER COMMENT '持仓手',
  open_interest_chg      INTEGER COMMENT '变化',
  order_no               INTEGER COMMENT '未知',

  -- 综合指数(o_curproduct)7
  highest_price_p        INTEGER COMMENT '最高价-综合',
  lowest_price_p         INTEGER COMMENT '最低价-综合',
  avg_price_p            DOUBLE COMMENT '加权平均价-综合',
  volume_p               INTEGER COMMENT '成交手-综合',
  turn_over              DOUBLE COMMENT '成交额(亿元)',
  year_volume            DOUBLE COMMENT '年成交手(万手)',
  year_turn_over         DOUBLE COMMENT '年成交额(亿元)',

  -- 金属指数(o_curmetalindex)12
  trading_day            DATE COMMENT '交易日期',
  last_price             DOUBLE COMMENT '最新价',
  open_price_m           DOUBLE COMMENT '今开盘价-金属',
  close_price_m          DOUBLE COMMENT '今收盘价-金属',
  pre_close_price_m      DOUBLE COMMENT '昨收盘价-金属',
  updown                 DOUBLE COMMENT '涨跌-金属(页面未显示)',
  updown1                DOUBLE COMMENT '涨跌1-金属',
  updown2                DOUBLE COMMENT '涨跌2-金属',
  highest_price_m        DOUBLE COMMENT '最高价-金属',
  lowest_price_m         DOUBLE COMMENT '最低价-金属',
  avg_price_m            DOUBLE COMMENT '加权平均价-金属',
  settlement_price_m     DOUBLE COMMENT '结算参考价-金属',

  -- others 13
  o_year                 INTEGER COMMENT '年份',
  o_month                INTEGER COMMENT '月份',
  o_day                  INTEGER COMMENT '日',
  o_weekday              VARCHAR(2) COMMENT '未知',
  o_year_num             INTEGER COMMENT '年期序号',
  o_total_num            INTEGER COMMENT '总期序号',
  o_trade_day            INTEGER COMMENT '总交易日序号',
  o_imchange_data        DATE COMMENT '未知',
  o_code                 INTEGER COMMENT '未知',
  o_msg                  VARCHAR(20) COMMENT '交易快讯查询成功',
  report_date            DATE COMMENT '报告日期',
  update_date            TIMESTAMP COMMENT '更新日期',
  print_date             TIMESTAMP COMMENT '打印日期'
);

SELECT *
FROM
  cu_price;

TRUNCATE TABLE cu_price;

-- -------------------------------------------------------
-- 筛选沪铜主力价格历史数据
-- -------------------------------------------------------
SELECT *
FROM
  (
    SELECT *
    FROM
      shfe_daily
    WHERE
      product_id != '总计'
      AND product_name != '小计'
    ORDER BY
      volume_i
  ) AS a
WHERE
  a.product_name = '铜'
GROUP BY
  a.price_date,
  a.product_id;

