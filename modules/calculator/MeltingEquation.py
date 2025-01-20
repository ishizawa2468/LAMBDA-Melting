
import numpy as np
from scipy.optimize import curve_fit

class MeltingEquation:
    params = {} # パラメータを保存しておくところ

    # simon_eqとかのパラメータを保存しておく
    # FIXME 式として保存して、Pを渡したらTを返すとかにする
    def set_params(self, key: str, params: list):
        self.params[key] = params
        print(f"以下を追加しました。\n -> key: {key} / {params}")

    @staticmethod
    def simon_eq(P, T0, A, c):
        return T0 * (P / A + 1)**c

    def fit_by_simon(self, P, T, initial_guess=None):
        if initial_guess is None:
            initial_guess = [1_000, 10, 0.5]  # T0, A, cの適当な初期推定値
        params, covariance = curve_fit(self.simon_eq, P, T, p0=initial_guess)
        params_std = np.sqrt(np.diag(covariance))
        print(f"params: T0, A, c / {params}")
        return params, params_std
