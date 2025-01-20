"""
状態方程式（Equation of State）を集約するメソッド集（クラスではないので注意）
"""

from modules.reference.eqn_bm3 import *
from modules.reference.eqn_vinet import *
from modules.reference.eqn_therm import *

"""
それぞれの物質で実装している
"""
# B2-KCl
def calc_P_KCl_B2(V, T):
    # ref) Dewaele et al., 2012
    v0 = 54.5
    k0 = 17.2
    k0p = 5.89
    akt = 0.00224
    # 計算
    P_no_T = vinet_p(V, v0, k0, k0p) # 体積由来
    P_therm = T * akt # 温度由来
    P = P_no_T + P_therm # 合計
    return P

# cubic-diamond
def calc_P_c_diamond(V, T):
    pass

def calc_rho_diamond(P, T=300):
    """
    圧力 P におけるダイヤモンドの密度を計算
    :param P: 圧力 (GPa)
    :param T: 温度 (K), 現状では未使用
    :return: 密度 (g/cm^3)
    """
    # ref) Occelli et al., 2003
    # https://www.nature.com/articles/nmat831
    v0 = 3.4170 # cm^3/mol
    k0 = 446 # GPa
    k0p = 3.0

    # 圧力 P における単位セル体積 (Å³)
    V_cell = vinet_v(P, v0, k0, k0p)

    # 密度を計算
    molar_mass = 12.01  # g/mol
    rho = molar_mass / V_cell
    return rho
