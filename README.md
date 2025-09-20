# CSVデータフィルタ（CSV Filter Tool）

シンプルなGUIアプリで、CSVファイルを読み込み、特定の列と値でフィルタし、結果を表示・保存できるツールです。  
Python（Tkinter + pandas）で実装されています。

---

## 主な機能

- CSVファイルを読み込み、列ごとのユニークな値を自動取得
- ドロップダウンで列と値を選択してフィルタリング
- フィルタ結果をTreeviewで表示
- 結果を別CSVとして保存（UTF-8 BOM付き）

---

## 使用ライブラリ

- `tkinter`（GUI構築）
- `pandas`（CSV読み込み・データ処理）
- `ttk.Treeview`（フィルタ結果表示）

---

## 使い方

1. 「ファイル選択」でCSVファイルを読み込む  
2. 「列を選択」「値を選択」でフィルタ条件を設定  
3. 「フィルタ実行」で結果表示  
4. 「出力保存」でフィルタ後のCSVを保存  

※ UTF-8 / Shift-JIS どちらでも読み込み可能（BOM付き保存）

<img width="986" height="831" alt="datafilter" src="https://github.com/user-attachments/assets/c32f275f-d3d0-48f7-94b0-94a964dc713c" />


---

## 今後の改善案（Future Improvements）

- [ ] 複数条件でのフィルタ機能（例：「プロジェクト＝PJ-A」かつ「種別＝交通費」）
- [ ] フィルタ条件のリセットボタンの追加
- [ ] フィルタ結果の集計表示（件数や金額合計など）
- [ ] GUIデザインの改善（ttk.Styleやテーマ活用）
- [ ] 保存時のエンコーディング選択機能（UTF-8 / Shift-JISなど）

---

## ライセンス

MIT License
