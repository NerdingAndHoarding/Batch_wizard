import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import pathlib
import threading

# === DEFAULT CONFIG ===
DEFAULT_OPTIONS = {
    "-u": "200",
    "-w": "",
    "-U": False,
    "-V": True,
    "-S": True,
    "-p": True,
    "-a": "",
    "-d": False,
    "-r": "100,300",
    "-F": "",
    "-m": "",
    "-f": "arduino",
    "-T": "tms5220",
}

PYTHON_WIZARD = pathlib.Path(__file__).parent / "python_wizard.py"


class BatchWizardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Wizard GUI")

        # === Paths ===
        self.input_folder = tk.StringVar(value=".")
        self.output_file = tk.StringVar(value="all_outputs.txt")

        # === UI ===
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Folder selection
        tk.Label(frame, text="Input Folder:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.input_folder, width=40).grid(row=0, column=1)
        tk.Button(frame, text="Browse", command=self.browse_folder).grid(row=0, column=2)

        # Output file
        tk.Label(frame, text="Output File:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.output_file, width=40).grid(row=1, column=1)
        tk.Button(frame, text="Save As", command=self.save_file).grid(row=1, column=2)

        # Options
        self.option_vars = {}
        row = 2
        tk.Label(frame, text="Options:").grid(row=row, column=0, sticky="w")
        row += 1

        for opt, val in DEFAULT_OPTIONS.items():
            if isinstance(val, bool):
                var = tk.BooleanVar(value=val)
                tk.Checkbutton(frame, text=opt, variable=var).grid(row=row, column=0, sticky="w")
            else:
                var = tk.StringVar(value=val)
                tk.Label(frame, text=opt).grid(row=row, column=0, sticky="w")
                tk.Entry(frame, textvariable=var, width=20).grid(row=row, column=1, sticky="w")

            self.option_vars[opt] = var
            row += 1

        # Run button
        tk.Button(frame, text="Run", command=self.run_thread).grid(row=row, column=0, pady=10)

        # Output log
        self.log = scrolledtext.ScrolledText(frame, height=15)
        self.log.grid(row=row + 1, column=0, columnspan=3, sticky="nsew")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            self.output_file.set(file)

    def log_write(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def build_command(self, wav_file):
        cmd = ["python", str(PYTHON_WIZARD)]

        for opt, var in self.option_vars.items():
            val = var.get()

            if isinstance(var, tk.BooleanVar):
                if val:
                    cmd.append(opt)
            else:
                if val.strip() != "":
                    cmd.extend([opt, val])

        cmd.append(str(wav_file))
        return cmd

    def run_thread(self):
        threading.Thread(target=self.run_batch).start()

    def run_batch(self):
        input_path = pathlib.Path(self.input_folder.get())
        output_file = self.output_file.get()

        wav_files = sorted(input_path.glob("*.wav"))

        if not wav_files:
            messagebox.showerror("Error", "No WAV files found.")
            return

        with open(output_file, "w", encoding="utf-8") as out:
            for wav in wav_files:
                self.log_write(f"Processing {wav.name}...")

                cmd = self.build_command(wav)

                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

                    out.write(f"//--- {wav.name} ---//\n")
                    out.write(result.stdout)
                    out.write("\n\n")

                except subprocess.CalledProcessError as e:
                    self.log_write(f"Error: {e.stderr}")

        self.log_write("Done!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BatchWizardGUI(root)
    root.mainloop()