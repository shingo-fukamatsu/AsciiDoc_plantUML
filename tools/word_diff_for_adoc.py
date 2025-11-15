import os
import subprocess
import win32com.client
import tkinter as tk
from tkinter import filedialog, messagebox

#【事前にインストールするもの】
# pywin32とasciidoctorのインストールが必要です
# ・pywin32のインストール方法：コマンドプロンプトで「pip install pywin32」を実行してください。※許可済みソフトです
# ・asciidoctorのインストール方法：管理者に確認してください

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

def create_docinfo_file(adoc_path):
    """docinfo.htmlファイルを作成。
    adocからHTMLを生成する際に、HTMLの横幅を広げたり、HTMLをdocxに変換したときに型崩れないよう、styleを設定するためのファイル"""
    docinfo_path = os.path.join(os.path.dirname(adoc_path), "docinfo.html")
    with open(docinfo_path, "w", encoding="utf-8") as f:
        f.write("<style>\n")
        f.write("#header,\n")
        f.write("#content,\n")
        f.write("#footnotes,\n")
        f.write("#footer {\n")
        f.write("  max-width: 200.5em;\n")
        f.write("}\n")
        f.write("</style>")
    return docinfo_path

def convert_asciidoc_to_docx():
    """AsciidocファイルをHTMLに変換し、さらにDocxに変換"""
    adoc_path = asciidoc_entry.get()

    if not adoc_path:
        messagebox.showerror("エラー", "Asciidocファイルを選択してください")
        return
    
    html_path = adoc_path.replace(".adoc", "_base.html")
    docx_path = adoc_path.replace(".adoc", "_base.docx")

    success_html = False
    success_docx = False

    # adocをHTMLに変換
    try:
        docinfo_path = create_docinfo_file(adoc_path) #HTMLの横幅を広くする設定ファイルを作成
        subprocess.run(["asciidoctor", "-a", "scripts=cjk", "-a" , "docinfo=shared" , adoc_path], check=True, shell=True) #HTML変換
        html_path_tmp = adoc_path.replace(".adoc", ".html")
        os.rename(html_path_tmp, html_path) #HTMLのファイル名を変更
        success_html = True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"Asciidoc変換に失敗しました: {e}")
        return
    finally:
        # 一時ファイルを削除
        if os.path.exists(docinfo_path):
            os.remove(docinfo_path)

    # HTMLをdocxに変換
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        # HTMLファイルをWordに変換
        new_doc = word.Documents.Open(html_path)
        new_doc.SaveAs2(docx_path, FileFormat=12)  # docxフォーマットで保存
        new_doc.Close()
        success_docx = True
    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")
    finally:
        word.Quit()

    # 両方が成功した場合に通知
    if success_html and success_docx:
        messagebox.showinfo("成功", f"HTMLおよびDocxファイルの作成が完了しました\nHTML: {html_path}\nDocx: {docx_path}")

def compare_documents():
    """HTMLとWordを比較。
    adocをHTMLに変換し、さらにHTMLをWordに変換。その後、ベースのWordファイルと比較し、比較結果をWordファイルで出力する"""
    adoc_path = adoc_entry.get()
    old_doc_path = docx_entry.get()
    result_doc_path = result_entry.get()

    # 入力チェック
    if not adoc_path or not old_doc_path or not result_doc_path:
        messagebox.showerror("エラー", "全てのファイルを選択してください")
        return

    # adocをHTMLに変換
    try:
        docinfo_path = create_docinfo_file(adoc_path) #HTMLの横幅を広くする設定ファイルを作成
        subprocess.run(["asciidoctor", "-a", "scripts=cjk", "-a" , "docinfo=shared" ,adoc_path], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"Asciidoc変換に失敗しました: {e}")
        return
    finally:
        # 一時ファイルを削除
        if os.path.exists(docinfo_path):
            os.remove(docinfo_path)
    html_path = adoc_path.replace(".adoc", ".html")

    # HTMLをdocxに変換し、さらにベースのdocxと比較
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    new_doc_path = html_path.replace('.html', '.docx')

    try:
        # HTMLファイルをWordで開く
        new_doc = word.Documents.Open(html_path)
        new_doc.SaveAs2(new_doc_path, FileFormat=12)  # docxフォーマットで保存
        new_doc.Close()

        # Wordファイルを開いて比較
        doc1 = word.Documents.Open(new_doc_path)
        doc2 = word.Documents.Open(old_doc_path)
        compare_result = word.CompareDocuments(doc2, doc1)

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
        #if os.path.exists(new_doc_path):
           # os.remove(new_doc_path)

# GUIの作成
root = tk.Tk()
root.title(" Word ⇔ Asciidoc 比較ツール ")
root.geometry("550x350")

# 文字やボタン等の配置
# row=0
tk.Label(root, text="比較_ベースファイル(*.adoc):").grid(row=0, column=0, padx=10, pady=5)
asciidoc_entry = tk.Entry(root, width=50)
asciidoc_entry.grid(row=0, column=1)
tk.Button(root, text="選択", command=lambda: select_file(asciidoc_entry, [("Asciidoc Files", "*.adoc")])).grid(row=0, column=2)

# row=1
tk.Button(root, text="HTMLとdocxに変換", command=convert_asciidoc_to_docx).grid(row=1, column=1, pady=5)

# row=2
tk.Label(root, text="比較_ベースファイル(*.docx):").grid(row=2, column=0, padx=10, pady=5)
docx_entry = tk.Entry(root, width=50)
docx_entry.grid(row=2, column=1)
tk.Button(root, text="選択", command=lambda: select_file(docx_entry, [("Word Files", "*.docx")])).grid(row=2, column=2)

# row=3
tk.Label(root, text="比較_変更後ファイル(*.adoc):").grid(row=3, column=0, padx=10, pady=5)
adoc_entry = tk.Entry(root, width=50)
adoc_entry.grid(row=3, column=1)
tk.Button(root, text="選択", command=lambda: select_file(adoc_entry, [("Asciidoc Files", "*.adoc")])).grid(row=3, column=2)

# row=4
tk.Label(root, text="比較結果の保存先:").grid(row=4, column=0, padx=10, pady=5)
result_entry = tk.Entry(root, width=50)
result_entry.grid(row=4, column=1)
tk.Button(root, text="選択", command=lambda: select_save_file(result_entry)).grid(row=4, column=2)

# row=5
tk.Button(root, text="比較を実行", command=compare_documents).grid(row=5, column=1, pady=20)
root.mainloop()