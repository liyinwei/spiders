# Spiders

This is an open source project aims at crawling data from the Internet.

# Motivation

*One can't make bricks without straw.*

The motivation of launching this project is that data is playing more and more important role in data science area, and most of the time the data scientist have to spend a lot of energy on crawling data that they need. Thus we launch the project for the sake of reducing burden of the one who need data from the Internet.

# Prerequisites

- [Python](https://www.python.org/) 3.5 + 


# Structure(Spider List)

- [shfe](https://github.com/liyinwei/spiders/tree/master/shfe): Crawling the copper futures prices from [Shanghai Futures Exchange](http://www.shfe.com.cn/)
  - **Desc:**：Daily futures exchanging data from [Shanghai Futures Exchange](http://www.shfe.com.cn/)
  - **Data Page:** http://www.shfe.com.cn/statements/dataview.html?paramid=kx
  - **Url:** "http://www.shfe.com.cn/data/dailydata/kx/kx" + exchange_date + ".dat"
  - **data description:** @see [table definition](https://github.com/liyinwei/spiders/blob/master/shfe/data_desc.sql)

# Running

There is a main method in each python file so you can run it easily.


# Authors
- [Yinwei Li](https://github.com/liyinwei)
  - **weichat**: coridc
  - **email**: 251469031@qq.com

*Don't hesitate to contact me on any topics about this project at your convenience.*


# Contributors
- [Yinwei Li](https://github.com/liyinwei)


# Contributing

When contributing to this repository, you can first discuss the change you wish to make via issue, email, or any other method with the owners of this repository.


# License

This project is licensed under the [GNU General Public License v3.0](http://www.gnu.org/licenses/gpl-3.0.html) License - see the [LICENSE](https://github.com/liyinwei/copper_price_forecast/blob/master/LICENSE) file for details.

# Acknowledgments

I'd like hat tip to anyone who use the codes or send me any proposals of the project.