import streamlit as st

import modules.app_utils.setting_handler as setting_handler

st.set_option('client.showSidebarNavigation', False) # デフォルトのサイドバー表示を一旦無効にする。自分でlabelをつけるため。
setting_handler.set_common_setting()

print('log: Homeを表示')

# 共通の表示
st.title("Welcome to LAMBDA-Melting notebooks!")
st.markdown(
    """
    ### 【概要】
    - BL10XUにおいてLAMBDAを使って得られた(温度, XRD) = (.spe/.hdf, .nxs)のペアを解析します。
        - 生の.speから温度が計算されている必要があります。(現在計算された温度ファイルはhdfのみ対応)
    - 以下のようにページが分かれています。←から選択してください。
        1. Run Selector: 解析するRunを選択します。each-runフォルダにあるnotebookで利用します。
        2. Setting Editor:
        3. HDF Viewer: .hdfのファイルの中身を閲覧したり、ダウンロードしたりできます。
    """
)

