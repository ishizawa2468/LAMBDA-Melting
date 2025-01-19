import os

import pandas as pd
import streamlit as st

import json

# それぞれのページで共通レイアウト・設定を作る
def set_common_setting(has_link_in_page=True):
    # 共通の設定
    st.set_page_config(
        page_title="LAMBDA Melting",
        layout="wide",
    )

    # 共通のサイドバー(ページリンク)
    st.set_option('client.showSidebarNavigation', False) # デフォルトのサイドバー表示を一旦無効にする。自分でlabelをつけるため。
    with st.sidebar:
        st.page_link("home.py", label="About app", icon="🏠")
        st.page_link("pages/run_selector.py", label="Run Selector", icon="📂")
        # st.page_link("pages/hdf_viewer.py", label="HDF Viewer", icon="👀")
        # st.page_link("pages/calc_by_2color.py", label="2 Color Pyrometer", icon="🎨")
        # ページ内のリンクが渡された場合、それを表示する
        if has_link_in_page:
            st.divider()
            st.sidebar.markdown("ページ内リンク")

# 設定をjsonで管理
class Setting:
    PATH_TO_JSON = 'settings/run_selector.json'

    def __init__(self):
        self.setting_json = self._get_setting()

    # 設定jsonを読み込むメソッド
    def _get_setting(self) -> dict:
        try:
            with open(self.PATH_TO_JSON, 'r') as f:
                setting_json = json.load(f)
        except FileNotFoundError:
            print(f'File {self.PATH_TO_JSON} not found.')
            st.write(f"ファイル {self.PATH_TO_JSON}が見つかりません")
        return setting_json

    # 設定jsonを更新するメソッド
    def _update_setting(self, *, key, value):
        setting_json = self._get_setting() # 読み込み。エラー処理を書いてるのでこれを使う
        setting_json[key] = value  # 追加
        with open(self.PATH_TO_JSON, 'w') as f:  # 追加したものを書き込み
            json.dump(setting_json, f, ensure_ascii=False)
            print(f"{self.PATH_TO_JSON} の {key} に {value} が追加されました。")

    def update_setting(self, key, value):
        self._update_setting(key=key, value=value)


class RunListMaster:
    PATH_TO_RUN_LIST = 'ref_data/run_list.xlsx'

    def __init__(self):
        try:
            self.master = pd.read_excel(self.PATH_TO_RUN_LIST)
        except FileNotFoundError:
            print(f'File {self.PATH_TO_RUN_LIST} not found.')
            pass

    def find_run_year_month(self, run_name):
        """
        指定された run_name に対応する year と month を返す。
        """
        # run_name でフィルタリング
        filtered = self.master[self.master['run_name'] == run_name]
        if not filtered.empty:
            year = filtered['year'].iloc[0]
            month = filtered['month'].iloc[0] if 'month' in filtered.columns else None
            return year, month
        else:
            return None, None

    def use_from_notebook(self, repository_root):
        self.path_from_notebook = os.path.join(repository_root, self.PATH_TO_RUN_LIST)
        self.master = pd.read_excel(self.path_from_notebook)
        print(f'{self.path_from_notebook} にパスが変更され、Excelファイルが読み込まれました。')

    def update_adopt_side(self, run_name, new_adopted_steram):
        """
        指定された run_name の adopt_side を更新する。
        更新が成功した場合は True を返す。
        """
        # run_name で該当行を探す
        index = self.master[self.master['run_name'] == run_name].index

        if not index.empty:
            self.master['adopted_stream'] = self.master['adopted_stream'].astype(object)
            self.master.loc[index, 'adopted_stream'] = new_adopted_steram
            return True
        else:
            return False

    def save_to_excel(self):
        """
        現在のデータを Excel ファイルに保存する。
        """
        self.master.to_excel(self.path_from_notebook, index=False)
        print('Excelファイルの更新成功')

class PoniMaster:
    PATH_TO_PONI_MASTER = 'ref_data/poni_period.xlsx'

    def __init__(self):
        self.master = pd.read_excel(self.PATH_TO_PONI_MASTER)

    def find_poni_year_month(self, year, month):
        """
        指定された year と month に一致する PONI 校正フォルダを返す。
        """
        filtered = self.master[(self.master['year'] == year) & (self.master['month'] == month)]
        if not filtered.empty:
            return filtered['poni'].iloc[0]
        else:
            return None


