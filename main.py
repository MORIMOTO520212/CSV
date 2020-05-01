
# I/Oバウンドプログラムの高速化は並列処理では改善しませんでした。ぴえん。 #

import pandas as pd
import shutil as sh
import os,time

# # # # # # # # 初期設定 # # # # # # # # #

COPY = True # True - ファイルコピー, False - ファイル移動

# # # # # # # # # # # # # # # # # # # # #

error_cnt = 0

def copy(classification_dir_path: str, master_file_path: str):
    '''masterファイルパスから分類フォルダパスにコピーする。\n`classification_dir_path` : 分類フォルダパス\n`master_file_path` : masterファイルパス'''

    global error_cnt # ←ここは知識不足でglobal使いました許してください。

    try: sh.copy(master_file_path, classification_dir_path) # copy(コピー元ファイル, コピー先フォルダ)
    except:
        error_cnt += 1
        print(master_file_path+"は存在しません。")


def move(classification_dir_path: str, master_file_path: str):
    '''masterファイルパスから分類フォルダパスに移動する。\n`classification_dir_path` : 分類フォルダパス\n`master_file_path` : masterファイルパス'''

    global error_cnt
    
    try: sh.move(master_file_path, classification_dir_path) # copy(移動元ファイル, 移動先フォルダ)
    except:
        error_cnt += 1
        print(master_file_path+"は存在しません。")


def process(data, master_dir_path: str, output_dir_path: str):
    global error_cnt
    #↓分類フォルダ名#     #↓分類するファイル名#
    classification_name, output_file_name = data[1], data[2]

    master_file_path        = join(master_dir_path, output_file_name)    # コピー元ファイルパス
    classification_dir_path = join(output_dir_path, classification_name) # 分類フォルダパス

    # 分類フォルダが存在しない場合
    if not exists(classification_dir_path): 
        os.mkdir(classification_dir_path) # 分類フォルダ作成

        if COPY:       copy(classification_dir_path, master_file_path) # コピーする
        elif not COPY: move(classification_dir_path, master_file_path) # 移動する
            

    # 分類フォルダが存在する場合
    elif not exists(join(classification_dir_path, output_file_name)):  # 分類フォルダに同じ名前のファイルが存在しない場合

        if COPY:       copy(classification_dir_path, master_file_path) # コピーする
        elif not COPY: move(classification_dir_path, master_file_path) # 移動する
            

    # 分類フォルダ内に同じ名前のファイルが存在する場合
    else:
        print(master_file_path+"はすでに存在しています。")
        error_cnt+=1


if __name__=="__main__":
    
    cur_dir = os.getcwd()    # カレントディレクトリ取得
    join    = os.path.join   # 省略名の付与
    exists  = os.path.exists # 省略名の付与

    master_dir_path = join(cur_dir, "master")
    output_dir_path = join(cur_dir, "output")
    input_csv_path  = join(cur_dir, "input.csv")

    df       = pd.read_csv(input_csv_path) # ファイル読み込み input.csv
    file_cnt = len(list(df.itertuples()))  # ファイル数カウント

    if not exists(master_dir_path): os.mkdir(master_dir_path) # ディレクトリが存在しない場合作成
    if not exists(output_dir_path): os.mkdir(output_dir_path) # ディレクトリが存在しない場合作成
    if not exists(input_csv_path):  exit("input.csvファイルが存在しません")

    start = time.time() # ~処理速度計測用コード~ #

    for data in df.itertuples(): process(data, master_dir_path, output_dir_path)

    process_time = time.time() - start  # ~処理速度計測用コード~ #

    print('処理速度:'+str(process_time)) # ループ内の処理速度
    print("総ファイル数:" + str(file_cnt))
    print("エラーファイル数:" + str(error_cnt))