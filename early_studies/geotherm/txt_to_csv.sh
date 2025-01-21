#!/bin/bash

# 入力と出力ファイルを指定
input_file="${1:-prem.txt}" # デフォルトで prem.txt を使用
output_file="${2:-prem.csv}" # デフォルトで prem.csv を出力

# ファイルが存在しない場合はエラーを出す
if [[ ! -f "$input_file" ]]; then
    echo "入力ファイルが見つかりません: $input_file"
    exit 1
fi

# ヘッダー行を整形して出力
sed -n '1s/# //;1s/[[:space:]]\+/,/gp' "$input_file" > "$output_file"

# データ行をタブや空白をすべてカンマに変換して追記
tail -n +2 "$input_file" | tr -s '\t ' ',' >> "$output_file"

echo "CSVファイルに変換しました: $output_file"
