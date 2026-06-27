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

def main():
    root = tk.Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(
        title="選擇要轉換的檔案",
        filetypes=FILE_TYPES
    )

    if not input_file:
        return

    input_path = Path(input_file)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / f"{input_path.stem}.md"

    try:
        subprocess.run(
            ["markitdown", str(input_path), "-o", str(output_path)],
            check=True
        )

        messagebox.showinfo(
            "轉換完成",
            f"已輸出到：\n{output_path}"
        )

        # 自動用 VS Code 打開結果
        subprocess.run(["code", str(output_path)], check=False)

    except subprocess.CalledProcessError as e:
        messagebox.showerror(
            "轉換失敗",
            f"MarkItDown 執行失敗。\n\n錯誤：{e}"
        )

if __name__ == "__main__":
    main()