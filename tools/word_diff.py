import os
import win32com.client
import tkinter as tk
from tkinter import filedialog, messagebox

def select_file(entry_widget, file_types):
    """ファイル選択ダイアログ"""
    file_path = filedialog.askopenfilename(filetypes=file_types)
    entry_widget.delete(0, tk.END)  # 既存の内容を削除
    entry_widget.insert(0, file_path)  # 選択したパスを入力欄に追加

def select_save_file(entry_widget):
    """保存先ファイル選択ダイアログ"""
    file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def compare_documents():
    """入力されたファイルパスを使用して比較を実行"""
    html_path = html_entry.get()
    old_doc_path = docx_entry.get()
    result_doc_path = result_entry.get()

    if not html_path or not old_doc_path or not result_doc_path:
        messagebox.showerror("エラー", "全てのファイルを選択してください")
        return

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    new_doc_path = html_path.replace('.html', '_converted.docx')

    try:
        # HTMLファイルをWordで開く
        new_doc = word.Documents.Open(html_path)
        new_doc.SaveAs2(new_doc_path, FileFormat=12)  # docxフォーマットで保存
        new_doc.Close()

        # Wordファイルを開いて比較
        doc1 = word.Documents.Open(new_doc_path)
        doc2 = word.Documents.Open(old_doc_path)
        compare_result = word.CompareDocuments(doc1, doc2)

        # 比較結果を保存
        compare_result.SaveAs2(result_doc_path, FileFormat=12)
        compare_result.Close()

        doc1.Close(False)
        doc2.Close(False)

        messagebox.showinfo("完了", f"比較結果を保存しました\n{result_doc_path}")

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")
    finally:
        word.Quit()

        # 一時ファイルを削除
        if os.path.exists(new_doc_path):
            os.remove(new_doc_path)

# GUIの作成
root = tk.Tk()
root.title("HTML ⇔ Word 比較ツール")
root.geometry("500x300")

# 各項目のラベルと入力欄
tk.Label(root, text="HTMLファイル:").grid(row=0, column=0, padx=10, pady=5)
html_entry = tk.Entry(root, width=50)
html_entry.grid(row=0, column=1)
tk.Button(root, text="選択", command=lambda: select_file(html_entry, [("HTML Files", "*.html")])).grid(row=0, column=2)

tk.Label(root, text="比較対象 Wordファイル:").grid(row=1, column=0, padx=10, pady=5)
docx_entry = tk.Entry(root, width=50)
docx_entry.grid(row=1, column=1)
tk.Button(root, text="選択", command=lambda: select_file(docx_entry, [("Word Files", "*.docx")])).grid(row=1, column=2)

tk.Label(root, text="比較結果の保存先:").grid(row=2, column=0, padx=10, pady=5)
result_entry = tk.Entry(root, width=50)
result_entry.grid(row=2, column=1)
tk.Button(root, text="選択", command=lambda: select_save_file(result_entry)).grid(row=2, column=2)

# 比較実行ボタン
tk.Button(root, text="比較を実行", command=compare_documents).grid(row=3, column=1, pady=20)

root.mainloop()