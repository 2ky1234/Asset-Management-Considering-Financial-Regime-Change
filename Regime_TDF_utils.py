import numpy as np
import pandas as pd
from scipy import stats


def drop_outliers(series_ret):
    """
    수익률 30.5%를 넘는 날짜를 0으로 처리
    :param series_ret: 
    :return: 
    """
    out_value = np.abs(series_ret).max() # 수익률의 절댓값 중 최댓값
    mask = np.argwhere(np.abs(series_ret) == out_value) # 최댓값의 위치(인덱스 넘버)
    while float(out_value) > 0.305: # 30.5%가 넘는 수익률이 발견되지 않을 때 까지
        series_ret[mask] = 0 # 이상치 값을 0으로 바꿔주고

        out_value = np.abs(series_ret).max() # out_value 값을 갱신
        mask = np.argwhere(np.abs(series_ret) == out_value) # 갱신된 값의 위치
    return series_ret

def cal_prob_of_loss(L, T, mu_safe, mu_risky, vol_risky, weight_risky):
    """probability of loss for a portfolio comprising both a risky asset and a safe asset
    :L: annualized percentage loss in discrete units, Float64
    :T: the number of years in the investment horizon, int/Float64
    :mu_safe: safe asset return, Float64
    :mu_risky: risky asset return, Float64
    :vol_risky: annualized standard deviation of risky asset return
    :weight_risky: risky asset weight, Float64
    :return: probability of loss, Float64
    """
    numerator = np.log(1+L)*T - (mu_risky*T*weight_risky + mu_safe*T*(1-weight_risky))
    denominator = vol_risky*weight_risky*np.sqrt(T)
    return stats.norm.cdf(numerator/denominator, 0, 1)

def cal_weight_risky(L, T, Z, mu_safe, mu_risky, vol_risky):
    """
    :L: Annualized percentage loss in discrete units, Float64
    :T: The number of years in the investment horizon, int/Float64
    :mu_risky: risky asset return, Float64
    :vol_risky: Annualized standard deviation of risky asset return
    :Z: Standardized normal variable corresponding to the probability we are targeting to determine the risky asset weight
    :mu_safe: Safe asset return, Float64
    :return: Risky asset weight
    """
    numerator = np.log(1+L)*T - mu_safe*T
    denominator = Z*vol_risky*np.sqrt(T) + mu_risky*T - mu_safe*T
    return numerator/denominator

def cal_turbulence(ret_data):
    """
    일별 수익률로부터 turbulence 지수 계산.
    :param ret_data: daily return data, pd.DataFrame
    :return:
    """

    # 월별 수익률 계산
    ret_monthly = ret_data.groupby([ret_data.index.year.rename("year"), ret_data.index.month.rename("month")])
    ret_monthly = ret_monthly.apply(lambda x: ((1+x).cumprod()-1)).resample("BM").last()

    cov_matrix = ret_monthly.cov()
    inverse_cov = np.linalg.inv(cov_matrix)
    mean = ret_monthly.mean()
    N = len(ret_monthly.columns)
    f = lambda x: (1/N) * (x-mean).T@inverse_cov@(x-mean)
    result = ret_monthly.apply(f, axis=1)
    return result


def cal_turbulence_rolling(ret_data, window=500):
    """

    :param ret_data:
    :param window:
    :return:
    """
    nassets = len(ret_data.columns)
    rolling_ret = ret_data.rolling(window=window)
    rolling_mean = rolling_ret.mean()
    rolling_cov = rolling_ret.cov().dropna().unstack()

    date_index = rolling_cov.index

    tb_index = pd.DataFrame()
    idx_num = 1
    for i in date_index[:-1]:
        cov = rolling_cov.loc[i].unstack()
        mean = rolling_mean.loc[i]
        invcov = np.linalg.inv(cov)

        ret = ret_data.loc[date_index[idx_num]]
        tb = (1/nassets) * (ret-mean)@invcov@(ret-mean)
        tb_index.loc[i, "turbulence"] = tb
        idx_num += 1
    return tb_index

def cal_absorption_ratio_rolling(ret_data, frac=0.2, decay=0.9972, window=500):
    """
    흡수비율을 계산한다. EWMA 방식을 적용한다.
    수익률 데이터를 decay factor로 지수이동평균 평활화(Exponential Weighted Moving Average)를 거친뒤 공분산 행렬를 계산한다.
    이후 rolling window에 따라 absorption ratio를 계산한다.
    t 일의 AR 값은 t-500 부터 t-1 시점의 데이터를 이용하여 계산한다. t일의 종가는 확인할 수 없기 때문이다.
    :param ret_data: 수익률 데이터, pandas.DataFrame
    :param frac: 고려할 고윳값의 비율, 0<frac<=1, float
    :param decay: EWM 계산상의 감소비율, 0<decay<=1, float
    :param window: 이동기간
    :return:
    """
    N = len(ret_data.columns)
    n = int(round(N * frac))

    ewm_cov = ret_data.ewm(alpha=decay).mean().rolling(window=window).cov().dropna().unstack()
    date_index = ewm_cov.index

    result = pd.DataFrame()
    idx_num = 1
    for i in date_index[:-1]:
        cov = ewm_cov.loc[i].unstack()
        eig_val, eig_vec = np.linalg.eig(cov)

        selected = eig_vec[:, np.argsort(-eig_val)[:n]]

        sum_of_selected = selected.var(axis=0).sum()
        sum_of_total = np.diag(cov).sum()

        ar = sum_of_selected / sum_of_total
        result.loc[date_index[idx_num], "absorption ratio"] = ar
        idx_num += 1
    return result


