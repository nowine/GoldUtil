# coding:utf-8

import requests
import juhe_config
import errors

# Here is the common const, like the status codes
AUTH_KEY = 'Nil0911'
SUCCESS = 200
#WATCH_LIST = ['美元账户黄金']


class BaseBot(object):
    _KEY = juhe_config.CONFIG['key']
    _JSON_VERSION = juhe_config.CONFIG['v']

    def __init__(self):
        self.status_code = 0
        self.reason = None
        self.result = None
        self.watchers = ['美元账户黄金']  # set default watch list

    def get_raw(self, url, params=None):
        if not params:
            params = dict()

        params['key'] = self._KEY
        params['v'] = self._JSON_VERSION

        r = requests.get(url, params=params)
        if r and r.status_code == 200:
            raw = r.json()
            self.status_code = raw['resultcode']
            self.reason = raw['reason']
            self.result = raw['result'][0]
        else:
            raise errors.DataRetrievalError("Error occured when retrieving data from {0}".format(url),
                                     "Retrieving Status is {0}, reason is: {1}".format(self.status_code, self.reason))

        return r.status_code


class BankGoldBot(BaseBot):
    _URL = juhe_config.CONFIG['bankgold']

    '''
    def set_watcher(self, varieties):
        if type(varieties) == 'list':
            self.watcher = varieties
        else:
            raise ValueError("Expecting a list of varieties to be watched")
    '''

    def get_data(self, url=None, params=None):
        url = url if url else self._URL
        if self.get_raw(url, params=params) == 200:
            gold_objs = []
            for watcher in self.watchers:
                gold_objs.append(BankGoldObject(self.result[watcher]))
            return gold_objs
        else:
            raise DataRetrievalError("Error occured when retrieving Shang Hai Gold Market data",
                                     "Retrieving Status is {0}, reason is: {2}".format(self.status_code, self.reason))


class BaseGoldObject(object):
    def __init__(self):
        pass

    def __repr__(self):
        str_list = ['{0}\n'.format(self.__module__)]
        for attr, value in self.__dict__.items():
            str_list.append('{0} : {1}\n'.format(attr, value))
        return ''.join(str_list)

    def __str__(self):
        return self.__repr__()


class BankGoldObject(BaseGoldObject):
    def __init__(self, raw_dict):
        self.variety = raw_dict['variety']
        self.middle_price = raw_dict['midpri']
        self.bank_buy_in = raw_dict['buypri']
        self.bank_sell_out = raw_dict['sellpri']
        self.max_price = raw_dict['maxpri']
        self.min_price = raw_dict['minpri']
        self.today_open = raw_dict['todayopen']
        self.yesterday_close = raw_dict['closeyes']
        self.price_variance = raw_dict['quantpri']
        self.price_at_time = raw_dict['time']

    def html(self):
        html_template = """
        <h1>
          <p>{variety}</p>
        </h1>
        <table border=1>
          <tr>
            <th>字段</th><th>值</th>
          </tr>
          <tr>
            <td>中间价</td><td>{middle_price}</td>
          </tr>
          <tr>
            <td>银行买入价</td><td>{bank_buy_in}</td>
          </tr>
          <tr>
            <td>银行卖出价</td><td>{bank_sell_out}</td>
          </tr>
          <tr>
            <td>最高价</td><td>{max_price}</td>
          </tr>
          <tr>
            <td>最低价</td><td>{min_price}</td>
          </tr>
          <tr>
            <td>今日开盘价</td><td>{today_open}</td>
          </tr>
          <tr>
            <td>昨日收盘价</td><td>{yesterday_close}</td>
          </tr>
          <tr>
            <td>价格变动</td><td>{price_variance}</td>
          </tr>
          <tr>
            <td>价格时间</td><td>{price_at_time}</td>
          </tr>
        </table>
        """
        return html_template.format(**self.__dict__)
