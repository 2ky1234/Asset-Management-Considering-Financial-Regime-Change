import numpy as np
import pandas as pd
from scipy.stats import norm


def mdd(ret):
    """maximum drawdown

    :param ret: return series
    :return: maximum drawdown
    """
    cum_ret = (1 + ret).cumprod()
    max_drawdown = 0
    max_ret = 1
    for ix_ret in cum_ret.values:
        if max_drawdown > (ix_ret - max_ret) / max_ret:
            max_drawdown = (ix_ret - max_ret) / max_ret
        if max_ret < ix_ret:
            max_ret = ix_ret

    return abs(max_drawdown)


def sharpe_ratio(ret, rf, num_of_year=252):
    """basic sharpe ratio

    :param ret: daily return series(default)
    :param rf: annual risk free rate
    :param num_of_year: using to transfer to yearly data
    :return: basic sharpe ratio
    """
    return ((np.mean(ret - (rf / num_of_year))) / (np.std(ret))) * np.sqrt(num_of_year)


def calmar_ratio(ret, rf, num_of_year=252):
    """calmar ratio

    :param ret: daily return series
    :param rf: annual risk free rate
    :param num_of_year: using to transfer to yearly data
    :return: calmar ratio
    """
    return (np.mean(ret * num_of_year - rf)) / mdd(ret)


def winning_rate(ret):
    """winning rate = num of win /total number

    :param ret: daily return series
    :return: winning rate
    """
    var_winning_rate = np.sum(ret > 0) / len(ret)
    return var_winning_rate


def profit_loss_ratio(ret):
    """profit loss ratio

    :param ret: daily return series
    :return: 손익비
    """

    if np.sum(ret > 0) == 0:
        var_profit_loss_ratio = 0
    elif np.sum(ret < 0) == 0:
        var_profit_loss_ratio = np.inf
    else:
        win_mean = np.mean(ret[ret > 0])
        loss_mean = np.mean(ret[ret < 0])
        var_profit_loss_ratio = win_mean / loss_mean
    return abs(var_profit_loss_ratio)


def value_at_risk(ret, para_or_hist="para", confidence_level=0.95):
    """value at risk

    :param ret: return series
    :param para_or_hist: para=Parametric VaR, hist=Non-Parametric historical VaR
    :param confidence_level: confidence level
    :return: value at risk
    """
    vol = np.std(ret)
    if para_or_hist == "para":
        VaR = np.mean(ret) - vol * norm.ppf(confidence_level)
    elif para_or_hist == "hist":
        # Sort Returns in Ascending Order
        sorted_ret = sorted(ret)
        VaR = np.percentile(sorted_ret, int((1.0 - confidence_level) * 100))
    else:
        raise Exception("check the value of para_or_hist")

    return VaR


def total_return(price):
    '''

    :param price: price data
    :return: 기간 total return
    '''
    price_data = price.dropna()
    ret = (price_data.tail(1).values - price_data.head(1).values) / price_data.head(1).values
    return ret[0]


def get_total_performance(ret_data, risk_free):
    '''

    :param ret_data: return data
    :param risk_free: risk free return data
    :return: performance dataframe
    '''
    performance = {'MDD': ret_data.apply(mdd),
                   'Sharpe ratio': ret_data.apply(lambda x: sharpe_ratio(x, risk_free)),
                   'VaR': ret_data.apply(value_at_risk),
                   'Profit loss ratio': ret_data.apply(profit_loss_ratio),
                   'Winning ratio': ret_data.apply(winning_rate),
                   'Calmar ratio': ret_data.apply(lambda x: calmar_ratio(x, risk_free)),
                   'Mean': ret_data.mean() * 252,
                   'Std': ret_data.std() * np.sqrt(252),
                   'Total return': ((1 + ret_data).cumprod()).apply(total_return)}
    return pd.DataFrame(performance)
