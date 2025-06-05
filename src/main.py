import tkinter as tk
from tkinter import ttk
from highlighter import Highlighter, BracketMatcher, AutoCompleter, apply_theme_globally, toggle_theme, active_theme
from lexer import Lexer
from parser import Parser
import sys
from io import StringIO

# ana pencereyi oluştur
root = tk.Tk()
root.title("Python Code Editor")
root.geometry("1000x600")

# üüt çubuk için alan
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# ana çerçeve
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Content frame (editör ve analiz için)
content_frame = tk.Frame(main_frame)
content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# editör çerçevesi (sol taraf)
editor_frame = tk.Frame(content_frame)
editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# satır numaralarının bulunduğu alan
line_frame = tk.Frame(editor_frame, width=46)
line_frame.pack(side=tk.LEFT, fill=tk.Y)

# satır numaraları
line_numbers = tk.Text(line_frame, width=4, padx=3, takefocus=0, border=0, font=("Consolas", 12), state='disabled')
line_numbers.pack(fill=tk.Y)

# kod alanı ve kaydırma çubukları için iç çerçeve
text_frame = tk.Frame(editor_frame)
text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# yatay kaydırma çubuğu
horizontal_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# kod alanı
text_area = tk.Text(text_frame, wrap=tk.NONE, undo=True, font=("Consolas", 12))
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_area.config(xscrollcommand=horizontal_scrollbar.set)

# dikey çubuğu kaydırma
vertical_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.config(yscrollcommand=vertical_scrollbar.set)
horizontal_scrollbar.config(command=text_area.xview)
vertical_scrollbar.config(command=lambda *args: on_vertical_scroll(*args))

# çıktı bölmesi
output_frame = tk.Frame(main_frame, height=150)
output_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

# çıktı etiketi ve alanı
output_label = tk.Label(output_frame, text="Output:", anchor="w")
output_label.pack(side=tk.TOP, fill=tk.X)
output_area = tk.Text(output_frame, height=5, wrap=tk.WORD, state='disabled')
output_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

error_label = tk.Label(editor_frame, text="Ready", anchor="w")
error_label.pack(side=tk.BOTTOM, fill=tk.X)

analysis_frame = tk.Frame(content_frame, width=300)
analysis_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[10, 5])
notebook = ttk.Notebook(analysis_frame)
notebook.pack(fill=tk.BOTH, expand=True)

# token analizi sekmesi
token_frame = tk.Frame(notebook)
notebook.add(token_frame, text="Token’lar")
token_tree = ttk.Treeview(token_frame, columns=("Type", "Value", "Line", "Column"), show="headings", selectmode="browse")
token_tree.heading("Type", text="Tür")
token_tree.heading("Value", text="Değer")
token_tree.heading("Line", text="Satır")
token_tree.heading("Column", text="Sütun")
token_tree.column("Type", width=150, anchor="w")
token_tree.column("Value", width=200, anchor="w")
token_tree.column("Line", width=50, anchor="w")
token_tree.column("Column", width=50, anchor="w")
token_tree.pack(fill=tk.BOTH, expand=True)
token_scroll = tk.Scrollbar(token_frame, orient=tk.VERTICAL, command=token_tree.yview)
token_scroll.pack(side=tk.RIGHT, fill=tk.Y)
token_tree.configure(yscrollcommand=token_scroll.set)

# oarse tree sekmesi
tree_frame = tk.Frame(notebook)
notebook.add(tree_frame, text="Ağaç Yapısı")
tree_tree = ttk.Treeview(tree_frame, columns=("Node", "Detail", "Description"), show="headings")
tree_tree.heading("Node", text="Düğüm")
tree_tree.heading("Detail", text="Detay")
tree_tree.heading("Description", text="Açıklama")
tree_tree.column("Node", width=150, anchor="w")
tree_tree.column("Detail", width=150, anchor="w")
tree_tree.column("Description", width=200, anchor="w")
tree_tree.pack(fill=tk.BOTH, expand=True)
tree_scroll = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_tree.yview)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree_tree.configure(yscrollcommand=tree_scroll.set)

# highlighter, bracket matcher ve autocompleter örnekleri
highlighter = Highlighter(text_area, error_label)
bracket_matcher = BracketMatcher(text_area)
auto_completer = AutoCompleter(text_area)

# Token türü çevirileri
TOKEN_TYPE_MAP = {
    "COMMENT": "yorum",
    "KEYWORD": "anahtar kelime",
    "IDENTIFIER": "tanımlayıcı",
    "NUMBER": "sayı",
    "STRING": "metin",
    "STRING_QUOTE": "tırnak",
    "STRING_CONTENT": "metin içeriği",
    "ESCAPE_CHAR": "kaçış karakteri",
    "OPERATOR": "operatör",
    "ASSIGN": "atama",
    "COLON": "iki nokta",
    "LPAREN": "sol parantez",
    "RPAREN": "sağ parantez",
    "LBRACKET": "sol köşeli parantez",
    "RBRACKET": "sağ köşeli parantez",
    "COMMA": "virgül"
}

# Token’a tıklayınca kodda vurgulama
def highlight_token_in_code(event):
    selection = token_tree.selection()
    if selection:
        values = token_tree.item(selection[0])["values"]
        line = values[2]  # Satır
        text_area.tag_remove("sel", "1.0", tk.END)
        text_area.see(f"{line}.0")
        text_area.tag_add("sel", f"{line}.0", f"{line}.end")
        text_area.tag_configure("sel", background=active_theme["select_bg"])

# Parse tree düğümüne tıklayınca kodda vurgulama
def highlight_node_in_code(event):
    selection = tree_tree.selection()
    if selection:
        tags = tree_tree.item(selection[0])["tags"]
        if tags and tags[0].startswith("line_"):
            line = int(tags[0].split("_")[1])
            text_area.tag_remove("sel", "1.0", tk.END)
            text_area.see(f"{line}.0")
            text_area.tag_add("sel", f"{line}.0", f"{line}.end")
            text_area.tag_configure("sel", background=active_theme["select_bg"])

token_tree.bind("<Double-1>", highlight_token_in_code)
tree_tree.bind("<<TreeviewSelect>>", highlight_node_in_code)

# Kod çalıştırma fonksiyonu
def run_code():
    output_area.config(state='normal')
    output_area.delete('1.0', tk.END)
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        code = text_area.get('1.0', tk.END).rstrip('\n')
        exec(code, {})
        output = redirected_output.getvalue()
        output_area.insert('1.0', output or "No output")
        error_label.config(text="✓ Code executed successfully",
                           foreground=active_theme['error_label_fg_ok'])
    except Exception as e:
        output_area.insert('1.0', f"Error: {str(e)}")
        error_label.config(text=f"Error: {str(e)}",
                           foreground=active_theme['error_label_fg_error'])
    finally:
        sys.stdout = old_stdout
        output_area.config(state='disabled')
    update_analysis()

# Kaydırma fonksiyonu
def on_vertical_scroll(*args):
    text_area.yview(*args)
    line_numbers.yview(*args)
    update_line_numbers()

def update_analysis(event=None):
    code = text_area.get('1.0', tk.END).rstrip('\n')
    lexer = Lexer()

    # yoken analizi
    token_tree.delete(*token_tree.get_children())
    try:
        tokens = lexer.tokenize_with_escape_highlighting(code)
        for token_type, token_value, (line, col) in tokens:
            token_type_display = TOKEN_TYPE_MAP.get(token_type, token_type)
            tag = token_type.lower()
            token_tree.insert("", "end", values=(token_type_display, token_value, line, col), tags=(tag,))
    except ValueError as e:
        token_tree.insert("", "end", values=("Hata", str(e), "-", "-"))

    # parse tree
    tree_tree.delete(*tree_tree.get_children())
    try:
        tokens = lexer.tokenize(code)
        parser = Parser(tokens)
        parser.parse()
        parser.populate_treeview(tree_tree)
    except (ValueError, SyntaxError) as e:
        tree_tree.insert("", "end", values=("Hata", str(e), ""))

# Üstte butonlar ve başlık
button_frame = tk.Frame(top_frame)
button_frame.pack(side=tk.TOP, fill=tk.X)
run_button = tk.Button(button_frame, text="Run Code", command=run_code, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED, bd=3, padx=10, pady=5)
run_button.pack(side=tk.LEFT, padx=5, pady=5)
toggle_button = tk.Button(button_frame,
                          text="Toggle Theme",
                          command=lambda: toggle_theme(
                              root, text_area, line_numbers, error_label,
                              main_frame, line_frame, None,
                              highlighter, bracket_matcher, auto_completer,
                              output_area, output_label),
                          bg="#2196F3",
                          fg="white",
                          font=("Arial", 10, "bold"),
                          relief=tk.RAISED,
                          bd=3,
                          padx=10,
                          pady=5)
toggle_button.pack(side=tk.LEFT, padx=5, pady=5)

# Python Code Editor etiketi
editor_label = tk.Label(top_frame, text="Python Code Editor", font=("Arial", 12, "bold"))
editor_label.pack(side=tk.TOP, pady=5)

apply_theme_globally(
    root, text_area, line_numbers, error_label, main_frame, line_frame, None,
    highlighter, bracket_matcher, auto_completer, output_area, output_label
)

def update_line_numbers(event=None):
    top_visible_line = int(text_area.index('@0,0').split('.')[0])
    bottom_visible_line = int(text_area.index('@0,%d' % text_area.winfo_height()).split('.')[0])
    total_lines = int(text_area.index('end-1c').split('.')[0])
    line_numbers.config(state='normal')
    line_numbers.delete('1.0', tk.END)
    start_line = max(1, top_visible_line)
    end_line = min(total_lines, bottom_visible_line)
    line_numbers.insert('1.0', '\n'.join(str(i) for i in range(start_line, end_line + 1)))
    line_numbers.config(state='disabled')
    update_analysis()

# olayları bağla
text_area.bind('<KeyRelease>', update_line_numbers, add='+')
text_area.bind('<Button-1>', update_line_numbers, add='+')
text_area.bind('<MouseWheel>', update_line_numbers, add='+')
text_area.bind('<Configure>', update_line_numbers, add='+')
update_line_numbers()

root.mainloop()