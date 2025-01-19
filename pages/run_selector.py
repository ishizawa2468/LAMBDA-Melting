import os
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
    cells.sort()
    selected_cell = st.selectbox(label='セル', options=cells)
# run
with run_col:
    runs = get_files_list(path=os.path.join(data_root_path, selected_sample, selected_cell))
    runs.sort()
    selected_run = st.selectbox(label='Run', options=runs)
# 選択されていないものがあれば止める
if any(x == [] for x in [selected_sample, selected_cell, selected_run]):
    st.stop()

path_to_run = os.path.join(data_root_path, selected_sample, selected_cell, selected_run)
run_name = "_".join([selected_cell, selected_run]) # OIbDia08_2ndみたいな

# それぞれのファイル名を辞書にする
try:
    if os.listdir(path_to_run) is not []:
        T_dist_file = get_files_list(path=path_to_run, includes=['dist.hdf'])[0]
        raw_radiation_file = get_files_list(path=path_to_run, includes=['.spe'])[0]
        xrd_file = get_files_list(path=path_to_run, includes=['.nxs'])[0]
except:
    st.error('エラー')
    st.stop()

# run_nameをもとに、Excelから情報を取得
run_master = RunListMaster()
poni_master = PoniMaster()
year, month = run_master.find_run_year_month(run_name)
print(f"Run: {run_name}, Year: {year}, Month: {month}")
# 指定された year と month に一致する PONI 校正フォルダを検索
if year and month:
    poni_file = poni_master.find_poni_year_month(year, month)
    print(f"PONI file: {poni_file}")
else:
    st.warning(f'Runが見つかりませんでした。{run_name} が run_list.xlsx に記載されていることを確認してください。')
    st.stop()

# 上書きするかどうかをここで設定
is_overwritten = st.checkbox(label='処理データの上書きを行う (チェックを外すと、解析済みの際上書きされません)', value=True)

run_files = {
    'Temperature': {
        'raw_radiation': raw_radiation_file,
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
    setting.update_setting(key='is_overwritten', value=is_overwritten)
    setting = setting_handler.Setting()

# 選択されたRun情報を表示
st.markdown('') # 表示上のスペース確保
st.markdown('##### Runのファイル・情報を表示')
st.write(run_files)

# 保存先を選択
display_handler.display_title_with_link(
    title="3. 保存フォルダを選択",
    link_title="3. 保存フォルダを選択",
    tag="select_save_folder"
)

# 設定インスタンスを作成しておく。これを通してフォルダパスを読み込んだり保存したりする
setting = setting_handler.Setting()

st.markdown('') # 表示上のスペース確保
st.markdown('##### 保存フォルダを設定')
save_root_path = st.text_input(
    label='フォルダまでのfull path',
    value=setting.setting_json['save_root_path']
)
if st.button('保存先を更新'):
    setting.update_setting(key='save_root_path', value=save_root_path)
    setting = setting_handler.Setting()
