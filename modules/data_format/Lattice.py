"""
格子体積関連の処理を集約する
"""
import numpy as np

class Lattice:
    def __init__(self, *, wavelength_m):
        self.set_wavelength(wavelength_m)

    def set_wavelength(self, wavelength_m):
        # メートルで与えられると思っている。poniファイルがそうであるため。
        # その他が必要な場合は作ってください。
        self.wavelength_A = wavelength_m * 10**10 # オングストロームに変換

    """
    ユースケース
    よく使うピークを書いておく
    """
    def calc_KCl110_V_from_tth(self, tth):
        d = self.calc_d_from_tth(tth)
        indices = {
            'h': 1,
            'k': 1,
            'l': 0,
        }
        a = self.calc_lp_from_d(d, **indices)
        return a**3

    def calc_Diamond111_V_from_tth(self, tth):
        d = self.calc_d_from_tth(tth)
        indices = {
            'h': 1,
            'k': 1,
            'l': 1,
        }
        a = self.calc_lp_from_d(d, **indices)
        return a ** 3

    """
    個別の計算メソッド
    """
    def calc_d_from_tth(self, tth):
        # ブラッグ反射
        # 波長が必要
        if self.wavelength_A is None:
            raise Exception("X線の波長が設定されていません。")
        # 回折角(2θ)をラジアンに変換
        rad = (tth / 180.0) * np.pi / 2
        # 面間隔を計算
        d = self.wavelength_A / (2 * np.sin(rad))
        return d

    @staticmethod
    def calc_lp_from_d(d, system='cubic', **indices):
        # lp = lattice param(s)
        if system == 'cubic':
            h, k, l = indices['h'], indices['k'], indices['l'] # ミラー指数を取得
            a = d * np.sqrt(h**2 + k**2 + l**2)
            return a
        else:
            raise NotImplementedError("他の結晶系はまだサポートされていません。")
