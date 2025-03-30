import re
import csv
import glob

def export_requirement_id_list_to_csv():
    # 初期化
    output_data = []
    # 3.5 No3.1～3.4の処理を、すべての.adocファイルに対し実施する
    adoc_files = glob.glob("**/*.adoc", recursive=True) # 再帰的に.adocファイルを検索
    for file in adoc_files:
        # 3.1 .adocファイルを開く
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 3.2 要求IDに関連する下記文字が含まれる行を抽出したリストを作成
        extracted_lines = []
        for line in lines:
            if re.search(r":id:\s*SYSRS\d+-\d+", line):
                extracted_lines.append(line)
            elif re.search(r"\{id\}::", line):
                extracted_lines.append(line)
            elif re.search(r"\{id\}-\d+.*::", line):
                extracted_lines.append(line)
            elif re.search(r"\{id\}-\d+-\d+.*::", line):
                extracted_lines.append(line)

        # 3.3 抽出したリストについて、{id}の文字列を要求ID名に置換する
        upper_id = None
        for idx, line in enumerate(extracted_lines):
            if ":id:" in line:
                upper_id = re.search(r"SYSRS\d+-\d+", line).group()
            elif "{id}" in line and upper_id:
                extracted_lines[idx] = line.replace("{id}", upper_id)

        # 3.4 要求ID名に置換したリストから要求ID、HMI担当に依頼したいラベルを抽出する
        for line in extracted_lines:
            if ":id:" in line:
                continue
            # 出力用要求IDを抽出
            req_id_patterns = [
                r"SYSRS\d+-\d+-\d+-\d+",
                r"SYSRS\d+-\d+-\d+",
                r"SYSRS\d+-\d+"
            ]
            req_id = ""
            for pattern in req_id_patterns:
                req_id_match = re.search(pattern, line)
                if req_id_match:
                    req_id = req_id_match.group()
                    break
            # 出力用HMIラベルを抽出
            hmi_label_match = re.search(r"\[HMI:.*\]", line)
            hmi_label_tmp = hmi_label_match.group() if hmi_label_match else ""
            hmi_label_tmp = re.sub(r"(\d+)", r"disp\1", hmi_label_tmp)            #数字の前にdispを付与
            hmi_label = hmi_label_tmp.replace("[HMI:", "").replace("]", "")       #[HMI: と ] の文字列を空欄に置換
            # CSV出力用リストを更新
            output_data.append([req_id, hmi_label, file])

    # 3.6 出力用要求ID、出力用HMIラベルをCSVに出力する
    with open("output_req_id_list.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["要求ID", "HMIラベル", "ファイル名"])
        writer.writerows(output_data)

export_requirement_id_list_to_csv()
