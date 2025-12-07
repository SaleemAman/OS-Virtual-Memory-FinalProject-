import tkinter as tk
from tkinter import messagebox

# === 1. TOOLTIP CLASS (Hover Effect) ===
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        # Bind mouse events
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        "Display text in tooltip window"
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True) # Remove border
        
        # Tooltip Styling
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                       background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                       font=("Segoe UI", "9", "normal"))
        label.pack(ipadx=1)
        tw.geometry(f"+{x}+{y}")

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# === 2. LOGIC FUNCTIONS (Backend Logic) ===

def get_fifo_steps(n, pages):
    steps = []
    memory = [-1] * n
    pointer = 0
    faults = 0
    hits = 0
    for x in pages:
        status = ""
        if x in memory:
            status = "HIT"
            hits += 1
        else:
            status = "MISS"
            faults += 1
            memory[pointer] = x
            pointer = (pointer + 1) % n
            if pointer == n: pointer = 0
        steps.append((x, status, list(memory)))
    return steps, faults, hits

def get_lru_steps(n, pages):
    steps = []
    memory = []
    faults = 0
    hits = 0
    for x in pages:
        status = ""
        if x in memory:
            status = "HIT"
            hits += 1
            memory.remove(x)
            memory.append(x)
        else:
            status = "MISS"
            faults += 1
            if len(memory) == n:
                memory.pop(0)
            memory.append(x)
        temp_view = list(memory)
        while len(temp_view) < n: temp_view.append(-1)
        steps.append((x, status, temp_view))
    return steps, faults, hits

def get_optimal_steps(n, pages):
    steps = []
    memory = []
    faults = 0
    hits = 0
    for i in range(len(pages)):
        x = pages[i]
        status = ""
        if x in memory:
            status = "HIT"
            hits += 1
        else:
            status = "MISS"
            faults += 1
            if len(memory) < n:
                memory.append(x)
            else:
                farthest = -1
                target = -1
                for page_in_mem in memory:
                    found = False
                    for j in range(i + 1, len(pages)):
                        if pages[j] == page_in_mem:
                            if j > farthest:
                                farthest = j
                                target = page_in_mem
                            found = True
                            break
                    if not found:
                        target = page_in_mem
                        break
                if target == -1: target = memory[0]
                idx = memory.index(target)
                memory[idx] = x
        temp_view = list(memory)
        while len(temp_view) < n: temp_view.append(-1)
        steps.append((x, status, temp_view))
    return steps, faults, hits

# === 3. GUI DRAWING FUNCTIONS ===

def draw_result_row(container, page, status, frames):
    row_frame = tk.Frame(container, bg="white", pady=2)
    row_frame.pack(fill="x", pady=2)

    # Page Box
    tk.Label(row_frame, text=f"Page {page}", width=8, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    # Status Box (Color Coding)
    color = "#27ae60" if status == "HIT" else "#c0392b" # Green / Red
    tk.Label(row_frame, text=status, width=8, bg=color, fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    # Arrow
    tk.Label(row_frame, text="➜", bg="white", fg="#7f8c8d").pack(side="left", padx=5)

    # Frames (Blue Boxes)
    for f in frames:
        val = str(f) if f != -1 else "-"
        tk.Label(row_frame, text=val, width=4, height=1, bg="#3498db", fg="white", font=("Arial", 10, "bold"), relief="raised").pack(side="left", padx=2)

def run_simulation(algo_type):
    # Clear previous results
    for widget in result_container.winfo_children():
        widget.destroy()
    status_label.config(text="")

    try:
        n = int(entry_frames.get())
        inp_str = entry_pages.get()
        pages = [int(x) for x in inp_str.split()]
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")
        return

    steps = []
    faults = 0
    hits = 0
    
    if algo_type == "FIFO":
        steps, faults, hits = get_fifo_steps(n, pages)
    elif algo_type == "LRU":
        steps, faults, hits = get_lru_steps(n, pages)
    elif algo_type == "Optimal":
        steps, faults, hits = get_optimal_steps(n, pages)

    # Header in Scroll Area
    header_lbl = tk.Label(result_container, text=f"Simulation Results: {algo_type}", 
                         font=("Segoe UI", 12, "bold"), bg="white", fg="#2980b9")
    header_lbl.pack(pady=10)

    for page, status, frames in steps:
        draw_result_row(result_container, page, status, frames)

    total = len(pages)
    ratio = (hits/total)*100 if total > 0 else 0
    summary_text = f"Total Pages: {total}   |   Faults: {faults}   |   Hits: {hits}   |   Ratio: {ratio:.1f}%"
    status_label.config(text=summary_text, fg="#2c3e50")

# === 4. MAIN WINDOW SETUP ===

root = tk.Tk()
root.title("OS Project - Visual Memory Manager")
root.geometry("750x650")
root.configure(bg="#ecf0f1")

# --- HEADER ---
header_frame = tk.Frame(root, bg="#2c3e50", pady=15)
header_frame.pack(fill="x")
tk.Label(header_frame, text="Virtual Memory Simulator", font=("Segoe UI", 20, "bold"), fg="white", bg="#2c3e50").pack()

# --- INPUT SECTION ---
input_frame = tk.Frame(root, bg="#ecf0f1", pady=15)
input_frame.pack()

def create_input(label_text, col):
    tk.Label(input_frame, text=label_text, bg="#ecf0f1", font=("Segoe UI", 11), fg="#2c3e50").grid(row=0, column=col, padx=5)

create_input("Frames:", 0)
entry_frames = tk.Entry(input_frame, width=5, font=("Segoe UI", 11), justify="center", bd=2, relief="groove")
entry_frames.grid(row=0, column=1, padx=5)

create_input("Pages (e.g., 1 2 3):", 2)
entry_pages = tk.Entry(input_frame, width=35, font=("Segoe UI", 11), bd=2, relief="groove")
entry_pages.grid(row=0, column=3, padx=5)

# --- BUTTONS ---
btn_frame = tk.Frame(root, bg="#ecf0f1", pady=5)
btn_frame.pack()

def create_styled_button(parent, text, command, tip_text):
    container = tk.Frame(parent, bg="#ecf0f1")
    container.pack(side="left", padx=15)
    
    # Button
    btn = tk.Button(container, text=text, command=command, 
                    bg="#2980b9", fg="white", 
                    font=("Segoe UI", 10, "bold"), 
                    width=10, relief="raised", cursor="hand2")
    btn.pack(side="left")
    
    # Icon
    info_lbl = tk.Label(container, text="ℹ", font=("Segoe UI", 12, "bold"), 
                        bg="#ecf0f1", fg="#7f8c8d", cursor="question_arrow")
    info_lbl.pack(side="left", padx=2)
    
    # Tooltip
    ToolTip(info_lbl, tip_text)

# Tooltips in ENGLISH now
create_styled_button(btn_frame, "FIFO", lambda: run_simulation("FIFO"), 
                     "First-In-First-Out:\nReplaces the oldest page in memory.")

create_styled_button(btn_frame, "LRU", lambda: run_simulation("LRU"), 
                     "Least Recently Used:\nReplaces the page that hasn't been\nused for the longest time.")

create_styled_button(btn_frame, "OPTIMAL", lambda: run_simulation("Optimal"), 
                     "Optimal Algorithm:\nReplaces the page that will not be\nused for the longest period in future.")

# --- RESULT AREA ---
main_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(main_frame, bg="white")
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
result_container = tk.Frame(canvas, bg="white")

result_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=result_container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- FOOTER ---
bottom_frame = tk.Frame(root, bg="#ecf0f1")
bottom_frame.pack(fill="x", pady=5)

status_label = tk.Label(bottom_frame, text="Ready to Simulate...", font=("Segoe UI", 12, "bold"), fg="#7f8c8d", bg="#ecf0f1")
status_label.pack()

# Footer Text Color -> WHITE
footer_label = tk.Label(root, text="Project By: Saleem Aman (53526) | Muammar Rayyan (54766)", 
                        font=("Consolas", 10), bg="#2c3e50", fg="white", pady=8)
footer_label.pack(side="bottom", fill="x")

# --- START ---
root.mainloop()