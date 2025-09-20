import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  #DPIスケーリング有効
except:
    pass


#グローバル変数
df_original = None
filtered_df = None
tree = None


#ファイル選択時：列名を読み込んで、DataFrameを保持
def load_columns(file_path):
    global df_original

    try:
        df_original = pd.read_csv(file_path)
        columns = df_original.columns.tolist()

        column_var.set("列を選択")
        option_menu["menu"].delete(0, "end")

        for col in columns:
            option_menu["menu"].add_command(
                label=col, 
                command=lambda c=col: on_column_select(c)
            )

        file_label.config(text=file_path)


    except Exception as e:
        file_label.confing(text=f"読み込み失敗：{e}")


#対象列が選択された時の処理
def on_column_select(column_name):
    column_var.set(column_name)
    update_filter_values(column_name)


#列に応じたユニーク値を表示
def update_filter_values(column_name):
    global df_original

    if df_original is None or column_name not in df_original.columns:
        return
    
    unique_values = df_original[column_name].dropna().astype(str).unique().tolist()

    filter_value_var.set("値を選択")
    filter_value_menu["menu"].delete(0, "end")

    for val in unique_values:
        filter_value_menu["menu"].add_command(
            label=val,
            command=tk._setit(filter_value_var, val)
        )


#フィルタ実行処理
def apply_filter():
    global tree, df_original, filtered_df

    if df_original is None:
        return
    
    selected_column = column_var.get()
    selected_value = filter_value_var.get()

    if selected_column not in df_original.columns or selected_value == "値を選択":
        return
    
    filtered_df = df_original[df_original[selected_column].astype(str) == selected_value]
    #Treeviewを再描画
    update_treeview(filtered_df)


#Treeviewの表示処理
def update_treeview(df):
    global tree, tree_frame
    
    #既にTreeviewがあれば削除
    for widget in tree_frame.winfo_children():
        widget.destroy()

    #スクロールバーの再設定
    tree_scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
    tree_scrollbar_y.pack(side="right", fill="y")

    tree_scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
    tree_scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
    tree.pack(fill="both", expand=True)

    tree_scrollbar_y.config(command=tree.yview)
    tree_scrollbar_x.config(command=tree.xview)


    #カラム設定
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)    #必要に応じて幅の調整

    #データ挿入
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))


#CSV出力処理
def export_csv():
    global filtered_df
    if filtered_df is None or filtered_df.empty:
        tk.messagebox.showwaring("出力エラー", "出力するデータがありません。")
        return
    
    save_path = filedialog.asksaveasfilename(
        defaultextension = ".csv",
        filetypes=[("CSV Files", "*.csv")],
        title = "CSVとして保存"
    )

    if save_path:
        try:
            filtered_df.to_csv(save_path, index=False, encoding="utf-8-sig")
            tk.messagebox.showinfo("保存完了", "CSVファイルを保存しました。")
        except Exception as e:
            tk.messagebox.showerror("保存失敗", str(e))


#ファイル選択
def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        load_columns(file_path)


# ----- UI部分 ----- #
#ウィンドウ作成
root = tk.Tk()
root.title("CSVデータフィルタ")
root.geometry("1000x800")   #ウィンドウサイズ

#Treeview内の行の高さ調整
style = ttk.Style()
style.configure("Treeview", rowheight=30)

# --- メインフレーム --- #
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)   #中央揃え

#ファイル選択ボタン
select_button = tk.Button(main_frame, text="ファイル選択", command=select_file)
select_button.grid(row=0, column=0, columnspan=2, pady=5)

#選択ファイル表示ラベル
file_label = tk.Label(main_frame, text="未選択", width=50, anchor="center")
file_label.grid(row=1, column=0, columnspan=2, pady=5)

#フィルタ列選択用ドロップダウン
column_var = tk.StringVar()
column_var.set("列を選択")
option_menu = tk.OptionMenu(main_frame, column_var, "")
option_menu.config(width=15)
option_menu.grid(row=2, column=0, padx=10, pady=5)

#ユニーク値用ドロップダウン
filter_value_var = tk.StringVar()
filter_value_var.set("値を選択")
filter_value_menu = tk.OptionMenu(main_frame, filter_value_var, "")
filter_value_menu.config(width=15)
filter_value_menu.grid(row=2, column=1, padx=10, pady=5)

#フィルタ実行ボタン
filter_button = tk.Button(main_frame, text="フィルタ実行", command=apply_filter)
filter_button.grid(row=3, column=0, padx=10, pady=5)

#出力保存ボタン
export_button = tk.Button(main_frame, text="出力保存", command=export_csv)
export_button.grid(row=3, column=1, padx=10, pady=5)


# ----- Treeview部分 ----- #
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

#スクロールバー
tree_scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
tree_scrollbar_y.pack(side="right", fill="y")

tree_scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
tree_scrollbar_x.pack(side="bottom", fill="x")

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
tree.pack(fill="both", expand=True)

tree_scrollbar_y.config(command=tree.yview)
tree_scrollbar_x.config(command=tree.xview)


# ----- メインループ ----- #
root.mainloop()