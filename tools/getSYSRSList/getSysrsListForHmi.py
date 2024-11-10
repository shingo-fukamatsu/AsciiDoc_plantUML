import re
import csv
import glob

def export_requirement_id_list_to_csv():
    # 3.5	No3.1～3.4の処理を、すべての.adocファイルに対し実施する
    adoc_files = glob.glob("*.adoc")
    for file in adoc_files:
        # 3.1	.adocファイルを開く
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 3.2	要求IDに関連する下記文字が含まれる行を抽出したリストを作成
        extracted_lines = []
        for line in lines:
            if re.search(r":id:\s*SYSRS\d+-\d+", line):
                extracted_lines.append(line)
            elif re.search(r"\{id\}-\d+.*::", line):
                extracted_lines.append(line)
            elif re.search(r"\{id\}-\d+-\d+.*::", line):
                extracted_lines.append(line)

        # 3.3	抽出したリストについて、{id}の文字列を要求ID名に置換する
        for idx, line in enumerate(extracted_lines):
            if ":id:" in line:
                upper_id = re.search(r"SYSRS\d+-\d+", line).group()
            else:
                extracted_lines[idx] = line.replace("{id}", upper_id)
        for line in extracted_lines:
            print(line)

        # 3.4	要求ID名に置換したリストから要求ID、HMI担当に依頼したいラベルを抽出し、CSVとして出力する
        output_data = []
        for line in extracted_lines:
            if ":id:" in line:
                continue
            req_id_match = re.search(r"SYSRS(\d+-\d+-\d+-\d+|-\d+-\d+|-\d+)", line)
            req_id = req_id_match.group() if req_id_match else ""
            hmi_label_match = re.search(r"\[HMI:(\d+|,|-)*\]", line)
            hmi_label = hmi_label_match.group(1) if hmi_label_match else ""
            output_data.append([req_id, hmi_label])

        csv_file = file.replace(".adoc", ".csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["要求ID", "HMIラベル"])
            writer.writerows(output_data)

export_requirement_id_list_to_csv()
