import os

import numpy as np
import openpyxl

# class LaserMaster:
#     PATH_TO_MASTER = ''
#
#     def __init__(self):
#         # Excel読み込み処理
#         pass
#
#     def find_run_params(self, run_name):
#         # run_nameで検索して、その行に格納されているパラメータを返す
#         pass

# 時間配列、パワー配列を組み立てるクラス。1つのRunに1つのインスタンスを想定する。
class Laser:
    def __init__(self, run_name):
        self.run_name = run_name
        self.set_from_excel()
        self.get_laser_profile_arr()

    def set_from_excel(self):
        # Excelブックの場所
        path_to_excel = '/Users/ishizawaosamu/work/MasterThesis/LAMBDA-Melting/ref_data/laser_params.xlsx'
        # ファイルを読み込んでシートをオブジェクト化
        workbook = openpyxl.load_workbook(path_to_excel)
        sheet = workbook['laser_params']
        # run_nameに一致する行を見つける
        run_row = None
        for row in range(2, sheet.max_row + 1):
            if sheet[f'C{row}'].value == self.run_name:
                run_row = row
                break
        # 見つからなかったらエラーを出す
        if run_row is None:
            raise ValueError(f"current_run.txtの {self.run_name} がlaser_params.xlsxのC列で見つかりませんでした。")
        # 見つかったらパラメータを読み込む
        # パラメータを読み込む
        self.laser_diameter_um = sheet[f"D{run_row}"].value  # D列にレーザー径の値
        self.linear = sheet[f"E{run_row}"].value  # E列に線形加熱かどうかの情報
        self.delay_ms = sheet[f"F{run_row}"].value  # F列にdelay_msの値
        self.time_adjust_ms = sheet[f"G{run_row}"].value  # G列にtime_adjust_msの値
        self.base_width_ms = sheet[f"H{run_row}"].value  # H列にbase_width_msの値
        self.whole_time_ms = sheet[f"I{run_row}"].value  # I列にwhole_time_msの値

        # 線形か定常かによってパラメータを分けて読み込む
        if self.linear:
            self.start_power_W = sheet[f"J{run_row}"].value  # J列にstart_power_Wの値
            self.goal_power_W = sheet[f"K{run_row}"].value  # K列にgoal_power_Wの値
            self.step_width_ms = sheet[f"L{run_row}"].value  # L列にstep_width_msの値
            self.linear_width_ms = sheet[f"M{run_row}"].value  # M列にlinear_width_msの値
        else:
            self.power_W = sheet[f"N{run_row}"].value  # N列にpower_Wの値

        print(f"Excelからパラメータを設定しました: {self.run_name}")

    def get_laser_profile_arr(self):
        if self.linear: # 線形加熱の場合
            print(" -- linear 加熱 --")
        else: # 定常加熱の場合
            print(" -- burst 加熱 --")
        self._compute_time_arr()
        self._compute_power_arr()

    def _compute_time_arr(self):
        # 線形加熱の場合
        if self.linear:
            if self.linear_width_ms == self.base_width_ms:
                step_num = round(self.linear_width_ms / self.step_width_ms)
                time_list = [
                    0,
                    self.delay_ms + self.time_adjust_ms,
                    self.delay_ms + self.time_adjust_ms
                ]
                for i in range(step_num):
                    ele = time_list[-1] + self.step_width_ms # 時間を進める
                    time_list.append(ele) # 追加
                    time_list.append(ele) # レーザー出力のみ上がる
                time_list.append(time_list[-1]) # クエンチ
                time_list.append(self.whole_time_ms) # 最後
            elif self.linear_width_ms < self.base_width_ms:
                step_num = round(self.linear_width_ms / self.step_width_ms)
                time_list = [
                    0,
                    self.delay_ms + self.time_adjust_ms,
                    self.delay_ms + self.time_adjust_ms
                ]
                for i in range(step_num):
                    ele = time_list[-1] + self.step_width_ms # 時間を進める
                    time_list.append(ele) # 追加
                    time_list.append(ele) # レーザー出力のみ上がる
                time_list.append(self.delay_ms + self.time_adjust_ms + self.base_width_ms) # ここまで保つ
                time_list.append(time_list[-1]) # クエンチ
                time_list.append(self.whole_time_ms) # 最後
            else:
                raise Exception("線形加熱のwidthが長い場合は実装されていません。必要であれば実装してください。")
        # 定常加熱の場合
        else:
            time_list = [
                0, # 1点目
                self.delay_ms + self.time_adjust_ms,
                self.delay_ms + self.time_adjust_ms,
                self.delay_ms + self.time_adjust_ms + self.base_width_ms,
                self.delay_ms + self.time_adjust_ms + self.base_width_ms,
                self.whole_time_ms # 最後
            ]
        time_arr = np.array(time_list)
        self.time_arr = time_arr / 1_000 # ms -> s
        print("\t時間計算終わり")

    def _compute_power_arr(self):
        # 線形加熱の場合
        if self.linear:
            if self.linear_width_ms == self.base_width_ms:
                step_num = round(self.linear_width_ms / self.step_width_ms)
                power_step = (self.goal_power_W - self.start_power_W) / step_num
                power_list = [
                    0,
                    0,
                    self.start_power_W
                ]
                for i in range(step_num):
                    ele = power_list[-1]
                    power_list.append(ele) # 時間のみ進む
                    power_list.append(ele + power_step) # エネルギー上がる
                power_list.append(0) # クエンチ
                power_list.append(0) # 最後
            elif self.linear_width_ms < self.base_width_ms:
                step_num = round(self.linear_width_ms / self.step_width_ms)
                power_step = (self.goal_power_W - self.start_power_W) / step_num
                power_list = [
                    0,
                    0,
                    self.start_power_W
                ]
                for i in range(step_num):
                    ele = power_list[-1]
                    power_list.append(ele) # 時間のみ進む
                    power_list.append(ele + power_step) # エネルギー上がる
                power_list.append(power_list[-1]) # 最後のエネルギーを保つ
                power_list.append(0) # クエンチ
                power_list.append(0) # 最後
            else:
                raise Exception("線形加熱のwidthが長い場合は実装されていません。実装してください。")
        # 定常加熱の場合
        else:
            power_list = [
                0, # 1点目
                0,
                self.power_W,
                self.power_W,
                0,
                0 # 最後
            ]
        power_arr = np.array(power_list)
        self.power_arr = power_arr
        print("\tエネルギー計算終わり")
