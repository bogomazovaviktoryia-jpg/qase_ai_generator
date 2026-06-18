import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import subprocess
import os

from app.config import INPUT_DIR, OUTPUT_DIR, TEMPLATES_DIR
from app.pipeline import run_pipeline
from app.llm.prompts import get_available_profiles


def ensure_dirs():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)


def add_docs():
    ensure_dirs()
    files = filedialog.askopenfilenames(
        title="Choose documentation files",
        filetypes=[
            ("Supported files", "*.txt *.md *.pdf *.docx *.xlsx"),
            ("All files", "*.*"),
        ],
    )

    if not files:
        return

    for file in files:
        shutil.copy(file, INPUT_DIR)

    messagebox.showinfo("Done", f"Added files: {len(files)}")


def generate_prompt(profile_var):
    try:
        os.environ["PROMPT_PROFILE"] = profile_var.get()
        run_pipeline()
        messagebox.showinfo(
            "Done",
            f"Prompt generated with profile: {profile_var.get()}\n\n"
            "File:\ndata/output/prompt_for_chatgpt.txt",
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def save_response_and_generate_csv():
    try:
        result = subprocess.run(
            ["pbpaste"],
            capture_output=True,
            text=True,
            check=False,
        )

        text = result.stdout.strip()

        if not text:
            raise ValueError("Clipboard is empty. Copy ChatGPT JSON response first.")

        response_path = OUTPUT_DIR / "manual_response.json"
        response_path.write_text(text, encoding="utf-8")

        from app.pipeline import run_manual_finalize

        run_manual_finalize()

        messagebox.showinfo(
            "Done",
            "CSV generated:\ndata/output/qase_import.csv",
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

def clean_output():
    ensure_dirs()

    for file in OUTPUT_DIR.glob("*"):
        if file.name == ".gitkeep":
            continue
        if file.is_file():
            file.unlink()

    messagebox.showinfo("Done", "Output folder cleaned")


def open_output_folder():
    ensure_dirs()
    subprocess.run(["open", str(OUTPUT_DIR)])


def main():
    ensure_dirs()

    root = tk.Tk()
    root.title("Qase AI Test Case Generator")
    root.geometry("480x430")

    title = tk.Label(
        root,
        text="Qase AI Test Case Generator",
        font=("Arial", 18, "bold"),
    )
    title.pack(pady=18)

    subtitle = tk.Label(
        root,
        text="Hybrid mode: documentation → ChatGPT → CSV for Qase",
        font=("Arial", 11),
    )
    subtitle.pack(pady=5)

    profile_label = tk.Label(root, text="Prompt profile:")
    profile_label.pack(pady=(15, 2))

    profiles = get_available_profiles()
    profile_var = tk.StringVar(value=os.getenv("PROMPT_PROFILE", "general"))

    profile_menu = tk.OptionMenu(root, profile_var, *profiles)
    profile_menu.config(width=25)
    profile_menu.pack(pady=5)

    tk.Button(root, text="1. Add documentation files", width=38, command=add_docs).pack(pady=8)

    tk.Button(
        root,
        text="2. Generate prompt",
        width=38,
        command=lambda: generate_prompt(profile_var),
    ).pack(pady=8)

    tk.Button(
        root,
        text="3. Save ChatGPT response and generate CSV",
        width=38,
        command=save_response_and_generate_csv,
    ).pack(pady=8)

    tk.Button(root, text="Open output folder", width=38, command=open_output_folder).pack(pady=8)
    tk.Button(root, text="Clean output", width=38, command=clean_output).pack(pady=8)

    note = tk.Label(
        root,
        text="Before step 3: copy the full JSON response from ChatGPT.",
        font=("Arial", 10),
        fg="gray",
    )
    note.pack(pady=12)

    root.mainloop()


if __name__ == "__main__":
    main()