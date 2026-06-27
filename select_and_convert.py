import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# 固定輸出資料夾
OUTPUT_DIR = Path(r"D:\markitdown_output")

# 可選檔案類型
FILE_TYPES = [
    ("Supported files", "*.pdf *.docx *.pptx *.xlsx *.xls *.mp3 *.wav *.m4a *.html *.txt"),
    ("PDF files", "*.pdf"),
    ("Word files", "*.docx"),
    ("PowerPoint files", "*.pptx"),
    ("Excel files", "*.xlsx *.xls"),
    ("Audio files", "*.mp3 *.wav *.m4a"),
    ("All files", "*.*"),
]

def make_unique_output_path(output_dir, stem):
    """
    避免同名檔案被覆蓋。
    例如 paper.md 已存在，就輸出 paper_1.md、paper_2.md。
    """
    output_path = output_dir / f"{stem}.md"
    counter = 1

    while output_path.exists():
        output_path = output_dir / f"{stem}_{counter}.md"
        counter += 1

    return output_path

def main():
    root = tk.Tk()
    root.withdraw()

    input_files = filedialog.askopenfilenames(
        title="選擇要轉換的檔案，可一次選多個",
        filetypes=FILE_TYPES
    )

    if not input_files:
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_files = []

    for input_file in input_files:
        input_path = Path(input_file)
        output_path = make_unique_output_path(OUTPUT_DIR, input_path.stem)

        try:
            subprocess.run(
                ["markitdown", str(input_path), "-o", str(output_path)],
                check=True
            )
            success_count += 1

        except subprocess.CalledProcessError:
            failed_files.append(str(input_path))

    result_message = f"成功轉換 {success_count} 個檔案。\n\n輸出資料夾：\n{OUTPUT_DIR}"

    if failed_files:
        result_message += "\n\n以下檔案轉換失敗：\n"
        result_message += "\n".join(failed_files)

    messagebox.showinfo("批次轉換完成", result_message)

    # 自動打開輸出資料夾
    subprocess.run(["explorer", str(OUTPUT_DIR)], check=False)

if __name__ == "__main__":
    main()