import os
from asyncio import set_event_loop

import pandas as pd
import streamlit as st

from modules.app_utils import setting_handler
from modules.app_utils import display_handler
from modules.app_utils.file_proceccer import get_files_list
from modules.app_utils.setting_handler import RunListMaster, PoniMaster

# 共通の設定
setting_handler.set_common_setting(has_link_in_page=True)

st.title("📂 Run Selector")

# 調査するファイルを選択
display_handler.display_title_with_link(
    title="1. データフォルダを選択",
    link_title="1. データフォルダを選択",
    tag="select_folder"
)

# 設定インスタンスを作成しておく。これを通してフォルダパスを読み込んだり保存したりする
setting = setting_handler.Setting()

st.markdown('') # 表示上のスペース確保
st.markdown('##### 読み込むフォルダを設定')
st.markdown(
    """
    - ここで設定したフォルダから`.spe`ファイルを選択できます。
        - Macの場合、Finderでフォルダを選択して `option + command + c`
        - Windowsの場合、エクスプローラーでフォルダを選択して `shift + control + c`
    """
)
data_root_path = st.text_input(
    label='フォルダまでのfull path',
    value=setting.setting_json['data_root_path']
)
if st.button('読み込み先を更新'):
    setting.update_setting(key='data_root_path', value=data_root_path)
    setting = setting_handler.Setting()

# 調査するファイルを選択
display_handler.display_title_with_link(
    title="2. Runを選択",
    link_title="2. Runを選択",
    tag="select_run"
)
# Sample -> Cell -> Runの順に選択
sample_col, cell_col, run_col = st.columns(3)
# sample
with sample_col:
    samples = get_files_list(path=data_root_path)
    samples.sort()
    selected_sample = st.selectbox(label='試料', options=samples)
# cell
with cell_col:
    cells = get_files_list(
        path=os.path.join(data_root_path, selected_sample),
        excludes=['.jpg']
    )
    cells.sort(reverse=True) # 気分なのでリバースじゃなくていい
    selected_cell = st.selectbox(label='セル', options=cells)
# run
with run_col:
    runs = get_files_list(path=os.path.join(data_root_path, selected_sample, selected_cell))
    runs.sort(reverse=True)
    selected_run = st.selectbox(label='Run', options=runs)
# 選択されていないものがあれば止める
if any(x == [] for x in [selected_sample, selected_cell, selected_run]):
    st.stop()

path_to_run = os.path.join(data_root_path, selected_sample, selected_cell, selected_run)
run_name = "_".join([selected_cell, selected_run]) # OIbDia08_2ndみたいな

# それぞれのファイル名を辞書にする
if os.listdir(path_to_run) is not []:
    T_dist_file = get_files_list(path=path_to_run, includes=['dist.hdf'])[0]
    raw_radiation_file = get_files_list(path=path_to_run, includes=['.spe'])[0]
    xrd_file = get_files_list(path=path_to_run, includes=['.nxs'])[0]

# run_nameをもとに、Excelから情報を取得
run_master = RunListMaster()
poni_master = PoniMaster()
year, month = run_master.find_run_year_month(run_name)
print(f"Run: {run_name}, Year: {year}, Month: {month}")
# 指定された year と month に一致する PONI 校正フォルダを検索
if year and month:
    poni_file = poni_master.find_poni_year_month(year, month)
    print(f"PONI file: {poni_file}")

run_files = {
    'Temperature': {
        'raw_raidation': raw_radiation_file,
        'dist': T_dist_file,
    },
    'XRD': {
        'data': xrd_file,
        'calibration': poni_file,
    }
}

# 保存
if st.button('Runを設定', type='primary'):
    setting.update_setting(key='current_run', value=run_name)
    setting.update_setting(key='path_to_run_files', value=path_to_run)
    setting.update_setting(key='selected_files', value=run_files)
    setting = setting_handler.Setting()

# 選択されたRun情報を表示
st.markdown('') # 表示上のスペース確保
st.markdown('##### Runのファイル・情報を表示')
st.write(run_files)

