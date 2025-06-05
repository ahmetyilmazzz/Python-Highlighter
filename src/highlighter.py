import tkinter as tk
from tkinter import ttk
from lexer import Lexer
from parser import Parser
import re

# Tema tanımları
light_theme = {
    'name': 'light',
    'main_frame_bg': '#ffffff',
    'text_area_bg': '#f8f8f8',
    'text_area_fg': '#000000',
    'line_numbers_bg': '#e0e0e0',
    'line_numbers_fg': '#666666',
    'select_bg': '#316AC5',
    'scrollbar_bg': '#e0e0e0',
    'scrollbar_troughcolor': '#ffffff',
    'output_area_bg': '#f0f0f0',
    'output_area_fg': '#000000',
    'analysis_bg': '#f8f8f8',
    'analysis_fg': '#000000',
    'highlighter_colors': {
        'KEYWORD': '#3a45cb',
        'BUILTIN': '#FF9900',
        'IDENTIFIER': '#1E0F0F',
        'OPERATOR': '#D01F1F',
        'ASSIGN': '#B5711D',
        'NUMBER': '#36A016',
        'STRING': '#063970',
        'STRING_QUOTE': '#063970',
        'STRING_CONTENT': '#063970',
        'ESCAPE_CHAR': '#FF6600',
        'COLON': '#DAA520',
        'LPAREN': '#1E0F0F',
        'RPAREN': '#1E0F0F',
        'COMMA': '#1E0F0F',
        'LBRACKET': '#1E0F0F',
        'RBRACKET': '#1E0F0F',
        'COMMENT': '#6F5F5F'
    },
    'error_tag_bg': '#ffcccc',
    'error_label_fg_ok': 'green',
    'error_label_fg_error': 'red',
    'error_label_fg_default': 'black',
    'bracket_match_bg': '#90EE90',
    'bracket_match_fg': 'black',
    'bracket_mismatch_bg': '#FFB6C1',
    'bracket_mismatch_fg': 'black',
    'completer_bg': '#ffffff',
    'completer_fg': 'black',
    'completer_select_bg': '#e0e0e0',
    'completer_select_fg': 'black',
}

dark_theme = {
    'name': 'dark',
    'main_frame_bg': '#1a1a1a',
    'text_area_bg': '#2d2d2d',
    'text_area_fg': '#d3d3d3',
    'line_numbers_bg': '#333333',
    'line_numbers_fg': '#a9b7c6',
    'select_bg': '#0078D7',
    'scrollbar_bg': '#555555',
    'scrollbar_troughcolor': '#1a1a1a',
    'output_area_bg': '#333333',
    'output_area_fg': '#d3d3d3',
    'analysis_bg': '#2d2d2d',
    'analysis_fg': '#d3d3d3',
    'highlighter_colors': {
        'KEYWORD': '#FF8C00',
        'BUILTIN': '#DA70D6',
        'IDENTIFIER': '#A9B7C6',
        'OPERATOR': '#FF6B68',
        'ASSIGN': '#A9B7C6',
        'NUMBER': '#6897BB',
        'STRING': '#6A8759',
        'STRING_QUOTE': '#6A8759',
        'STRING_CONTENT': '#6A8759',
        'ESCAPE_CHAR': '#E6A23C',
        'COLON': '#A9B7C6',
        'LPAREN': '#A9B7C6',
        'RPAREN': '#A9B7C6',
        'COMMA': '#A9B7C6',
        'LBRACKET': '#A9B7C6',
        'RBRACKET': '#A9B7C6',
        'COMMENT': '#808080'
    },
    'error_tag_bg': '#7f0000',
    'error_label_fg_ok': '#77dd77',
    'error_label_fg_error': '#ff6961',
    'error_label_fg_default': '#d3d3d3',
    'bracket_match_bg': '#3b873b',
    'bracket_match_fg': '#d3d3d3',
    'bracket_mismatch_bg': '#8b0000',
    'bracket_mismatch_fg': '#d3d3d3',
    'completer_bg': '#333333',
    'completer_fg': '#d3d3d3',
    'completer_select_bg': '#4b6eaf',
    'completer_select_fg': '#d3d3d3',
}

active_theme = light_theme.copy()

class Highlighter:
    def __init__(self, text_area, error_label):
        self.text_area = text_area
        self.error_label = error_label
        self.lexer = Lexer()
        self.syntax_colors = {}
        self.error_background_color = ''
        self.last_code = ""
        self.last_error_message = ""
        self.highlight_scheduled = False
        self.update_theme_settings()
        self.bind_events()
        self.text_area.after(50, self.initial_highlight)

    def bind_events(self):
        events = ['<KeyRelease>', '<Button-1>', '<ButtonRelease-1>',
                  '<Configure>', '<Expose>', '<FocusIn>', '<MouseWheel>',
                  '<Control-z>', '<Control-y>']
        for event in events:
            self.text_area.bind(event, self.schedule_highlight, add='+')
        self.text_area.bind('<Control-v>', self.on_paste, add='+')

    def initial_highlight(self):
        if self.text_area.winfo_exists():
            self.highlight()

    def update_theme_settings(self):
        global active_theme
        self.syntax_colors = active_theme['highlighter_colors'].copy()
        self.error_background_color = active_theme['error_tag_bg']
        for tag_name, color_value in self.syntax_colors.items():
            try:
                self.text_area.tag_configure(tag_name, foreground=color_value)
            except tk.TclError:
                return
        try:
            self.text_area.tag_configure('ERROR', background=self.error_background_color)
            self.text_area.tag_raise('ERROR')
        except tk.TclError:
            return
        if self.text_area.winfo_exists():
            self.last_code = ""
            self.schedule_highlight()

    def on_paste(self, event=None):
        self.text_area.after_idle(self.schedule_highlight)

    def schedule_highlight(self, event=None):
        if not self.highlight_scheduled:
            if not self.text_area.winfo_exists():
                return
            self.highlight_scheduled = True
            self.text_area.after(100, self.perform_highlight)

    def perform_highlight(self):
        if not self.text_area.winfo_exists():
            self.highlight_scheduled = False
            return
        self.highlight_scheduled = False
        self.highlight()

    def highlight(self, event=None):
        if not self.text_area.winfo_exists():
            return
        try:
            code = self.text_area.get('1.0', tk.END).rstrip('\n')
        except tk.TclError:
            return
        if code == self.last_code:
            return
        self.clear_syntax_tags()
        if not code.strip():
            self.update_error_label_display("", 'default')
            self.clear_error_tag()
            self.last_code = code
            self.last_error_message = ""
            return
        try:
            tokens_with_positions = self.tokenize_code_with_positions(code)
            tokens_for_parser = [(t[0], t[1], t[2]) for t in tokens_with_positions]
            parser = Parser(tokens_for_parser)
            parser.parse()
            self.apply_syntax_highlighting(tokens_with_positions)
            self.clear_error_tag()
            new_status_message = "✓ Syntax OK"
            if self.last_error_message != new_status_message:
                self.update_error_label_display(new_status_message, 'ok')
            self.last_error_message = new_status_message
        except (ValueError, SyntaxError) as e:
            error_msg_text = str(e)
            try:
                if 'tokens_with_positions' not in locals() or not tokens_with_positions:
                    tokens_with_positions = self.tokenize_code_with_positions(code, suppress_errors=True)
                self.apply_syntax_highlighting(tokens_with_positions)
            except:
                pass
            if error_msg_text != self.last_error_message:
                self.update_error_label_display(f"Error: {error_msg_text}", 'error')
            self.last_error_message = error_msg_text
            self.apply_error_tag()
        finally:
            self.last_code = code

    def update_error_label_display(self, message, status_key):
        global active_theme
        if not self.error_label.winfo_exists():
            return
        color_code = active_theme.get(f'error_label_fg_{status_key}', active_theme['error_label_fg_default'])
        bg_color = active_theme.get('main_frame_bg', 'SystemButtonFace')
        try:
            self.error_label.config(text=message, foreground=color_code, background=bg_color)
        except tk.TclError:
            pass

    def tokenize_code_with_positions(self, code, suppress_errors=False):
        tokens_with_pos = []
        try:
            basic_tokens = self.lexer.tokenize_with_escape_highlighting(code)
        except ValueError as e:
            if suppress_errors:
                return tokens_with_pos
            raise
        for token_type, token_value, (line, col) in basic_tokens:
            char_pos = self.find_char_position(code, line, col)
            start_tk_pos = self.char_to_tkinter_pos(code, char_pos)
            end_tk_pos = self.char_to_tkinter_pos(code, char_pos + len(token_value))
            tokens_with_pos.append((token_type, token_value, (line, col), start_tk_pos, end_tk_pos))
        return tokens_with_pos

    def find_char_position(self, code, target_line, target_col):
        lines = code.split('\n')
        char_pos = 0
        for i in range(target_line - 1):
            if i < len(lines):
                char_pos += len(lines[i]) + 1
        char_pos += target_col - 1
        return char_pos

    def char_to_tkinter_pos(self, text, char_index):
        if char_index > len(text):
            char_index = len(text)
        text_until_pos = text[:char_index]
        lines = text_until_pos.split('\n')
        return f"{len(lines)}.{len(lines[-1])}"

    def apply_syntax_highlighting(self, tokens_with_positions):
        for token_type, _, _, start_pos, end_pos in tokens_with_positions:
            if token_type in self.syntax_colors:
                try:
                    self.text_area.tag_add(token_type, start_pos, end_pos)
                except tk.TclError:
                    pass

    def clear_syntax_tags(self):
        if not self.text_area.winfo_exists():
            return
        try:
            for tag_key in self.syntax_colors.keys():
                self.text_area.tag_remove(tag_key, '1.0', tk.END)
        except tk.TclError:
            pass

    def clear_error_tag(self):
        if not self.text_area.winfo_exists():
            return
        try:
            self.text_area.tag_remove('ERROR', '1.0', tk.END)
        except tk.TclError:
            pass

    def apply_error_tag(self):
        if not self.text_area.winfo_exists():
            return
        try:
            self.text_area.tag_add('ERROR', '1.0', tk.END)
        except tk.TclError:
            pass

class BracketMatcher:
    def __init__(self, text_area):
        self.text_area = text_area
        self.bracket_pairs = {'(': ')', '[': ']', '{': '}', ')': '(', ']': '[', '}': '{'}
        self.open_brackets = {'(', '[', '{'}
        self.close_brackets = {')', ']', '}'}
        self.check_scheduled = False
        self.update_theme_settings()
        self.bind_events()

    def bind_events(self):
        events = ['<KeyRelease>', '<Button-1>', '<ButtonRelease-1>']
        for event in events:
            self.text_area.bind(event, self.schedule_bracket_check, add='+')

    def update_theme_settings(self):
        global active_theme
        if not self.text_area.winfo_exists():
            return
        try:
            self.text_area.tag_configure('BRACKET_MATCH',
                                         background=active_theme['bracket_match_bg'],
                                         foreground=active_theme['bracket_match_fg'])
            self.text_area.tag_configure('BRACKET_MISMATCH',
                                         background=active_theme['bracket_mismatch_bg'],
                                         foreground=active_theme['bracket_mismatch_fg'])
            self.schedule_bracket_check()
        except tk.TclError:
            pass

    def schedule_bracket_check(self, event=None):
        if not self.check_scheduled:
            if not self.text_area.winfo_exists():
                return
            self.check_scheduled = True
            self.text_area.after(100, self.perform_bracket_check)

    def perform_bracket_check(self):
        if not self.text_area.winfo_exists():
            self.check_scheduled = False
            return
        self.check_scheduled = False
        self.check_bracket_at_cursor()

    def check_bracket_at_cursor(self):
        if not self.text_area.winfo_exists():
            return
        try:
            self.text_area.tag_remove('BRACKET_MATCH', '1.0', tk.END)
            self.text_area.tag_remove('BRACKET_MISMATCH', '1.0', tk.END)
        except tk.TclError:
            return
        try:
            cursor_pos = self.text_area.index(tk.INSERT)
            left_pos = self.text_area.index(f"{cursor_pos}-1c")
            try:
                left_char = self.text_area.get(left_pos, cursor_pos)
            except tk.TclError:
                left_char = ""
            try:
                right_char = self.text_area.get(cursor_pos, f"{cursor_pos}+1c")
            except tk.TclError:
                right_char = ""
            if left_char in self.bracket_pairs:
                match_pos = self.find_matching_bracket(left_pos, left_char)
                if match_pos:
                    self.text_area.tag_add('BRACKET_MATCH', left_pos, cursor_pos)
                    self.text_area.tag_add('BRACKET_MATCH', match_pos, f"{match_pos}+1c")
                else:
                    self.text_area.tag_add('BRACKET_MISMATCH', left_pos, cursor_pos)
            elif right_char in self.bracket_pairs:
                match_pos = self.find_matching_bracket(cursor_pos, right_char)
                if match_pos:
                    self.text_area.tag_add('BRACKET_MATCH', cursor_pos, f"{cursor_pos}+1c")
                    self.text_area.tag_add('BRACKET_MATCH', match_pos, f"{match_pos}+1c")
                else:
                    self.text_area.tag_add('BRACKET_MISMATCH', cursor_pos, f"{cursor_pos}+1c")
        except tk.TclError:
            pass

    def find_matching_bracket(self, start_pos, bracket_char):
        text = self.text_area.get('1.0', tk.END)
        start_line, start_col = map(int, start_pos.split('.'))
        start_idx = sum(len(line) + 1 for line in text.split('\n')[:start_line - 1]) + start_col
        target_bracket = self.bracket_pairs[bracket_char]
        stack = []
        if bracket_char in self.open_brackets:
            for i in range(start_idx + 1, len(text)):
                if text[i] == bracket_char:
                    stack.append(text[i])
                elif text[i] == target_bracket:
                    if stack:
                        stack.pop()
                    else:
                        return self.char_to_tkinter_pos(text, i)
            return
        else:
            for i in range(start_idx - 1, -1, -1):
                if text[i] == bracket_char:
                    stack.append(text[i])
                elif text[i] == target_bracket:
                    if stack:
                        stack.pop()
                    else:
                        return self.char_to_tkinter_pos(text, i)
            return

    def char_to_tkinter_pos(self, text, char_index):
        if char_index > len(text):
            char_index = len(text)
        text_until_pos = text[:char_index]
        lines = text_until_pos.split('\n')
        return f"{len(lines)}.{len(lines[-1])}"

class AutoCompleter:
    def __init__(self, text_area):
        self.text_area = text_area
        self.completion_window = None
        self.completion_listbox = None
        self.current_word = ""
        self.word_start_pos = None
        # Python anahtar kelimeleri ve yerleşik fonksiyonlar
        self.completions = [
            'if', 'else', 'elif', 'while', 'for', 'in', 'def', 'class', 'return',
            'break', 'continue', 'and', 'or', 'not', 'try', 'except', 'finally',
            'raise', 'import', 'from', 'as', 'with', 'lambda', 'global', 'nonlocal',
            'True', 'False', 'None', 'pass', 'del', 'yield', 'assert', 'async', 'await',
            'match', 'case',
            'print', 'input', 'len', 'str', 'int', 'float', 'list', 'dict', 'tuple',
            'set', 'range', 'enumerate', 'zip', 'open', 'abs', 'max', 'min', 'sum',
            'all', 'any', 'sorted', 'reversed', 'map', 'filter', 'type', 'isinstance',
            'hasattr', 'getattr', 'setattr', 'dir', 'help', 'id', 'hex', 'oct', 'bin',
            'format'
        ]
        self.lexer = Lexer()
        self.update_theme_settings()
        self.bind_events()

    def bind_events(self):
        """Olayları bağla"""
        self.text_area.bind('<KeyRelease>', self.on_key_release, add='+')
        self.text_area.bind('<Button-1>', self.hide_completion_window, add='+')
        self.text_area.bind('<Escape>', self.hide_completion_window, add='+')
        self.text_area.bind('<Tab>', self.on_tab_press, add='+')
        self.text_area.bind('<Return>', self.on_return_press, add='+')
        self.text_area.bind('<Control-space>', self.on_ctrl_space, add='+')

    def update_theme_settings(self):
        """Tema ayarlarını güncelle"""
        global active_theme
        if self.completion_window and self.completion_listbox and self.completion_window.winfo_exists():
            try:
                self.completion_window.config(bg=active_theme['completer_bg'])
                self.completion_listbox.config(
                    bg=active_theme['completer_bg'],
                    fg=active_theme['completer_fg'],
                    selectbackground=active_theme['completer_select_bg'],
                    selectforeground=active_theme['completer_select_fg'],
                    font=("Consolas", 10)
                )
            except tk.TclError:
                pass

    def on_key_release(self, event):
        """Tuş bırakıldığında otomatik tamamlama kontrolü"""
        if not self.text_area.winfo_exists():
            return
        if event.keysym in ('Up', 'Down', 'Tab', 'Return', 'Escape', 'Control_L', 'Control_R'):
            return
        current_word = self.get_current_word()
        if len(current_word) >= 1:  # Minimum 1 karakterle öneri başlasın
            matches = self.find_matches(current_word)
            if matches:
                self.show_completion_window(matches)
            else:
                self.hide_completion_window()
        else:
            self.hide_completion_window()

    def on_ctrl_space(self, event):
        """Ctrl+Space ile manuel otomatik tamamlama tetikleme"""
        current_word = self.get_current_word()
        matches = self.find_matches(current_word or "")
        if matches:
            self.show_completion_window(matches)
        return 'break'

    def on_tab_press(self, event):
        """Tab tuşu ile tamamla"""
        if self.completion_window and self.completion_window.winfo_exists():
            self.complete_word()
            return 'break'
        return

    def on_return_press(self, event):
        """Enter tuşu ile tamamla"""
        if self.completion_window and self.completion_window.winfo_exists():
            self.complete_word()
            return 'break'
        return

    def get_current_word(self):
        """İmlecin bulunduğu yerdeki kelimeyi al"""
        try:
            cursor_pos = self.text_area.index(tk.INSERT)
            line_start = self.text_area.index(f"{cursor_pos} linestart")
            line_text = self.text_area.get(line_start, cursor_pos)
            # Kelimeyi imlecin bulunduğu yerden al, boşluk veya özel karakterle sınırlı
            match = re.search(r'\b(\w+)$', line_text)
            if match:
                self.current_word = match.group(1)
                word_start_col = len(line_text) - len(self.current_word)
                line_num = cursor_pos.split('.')[0]
                self.word_start_pos = f"{line_num}.{word_start_col}"
                return self.current_word
            else:
                self.current_word = ""
                self.word_start_pos = cursor_pos
                return ""
        except tk.TclError:
            self.current_word = ""
            self.word_start_pos = None
            return ""

    def find_matches(self, word):
        """Yazılan kelimeye uygun önerileri bul"""
        word_lower = word.lower()
        matches = []
        # Kod içindeki tanımlayıcıları da ekle
        try:
            code = self.text_area.get('1.0', tk.END).rstrip('\n')
            tokens = self.lexer.tokenize(code)
            identifiers = [token[1] for token in tokens if token[0] == 'IDENTIFIER']
            all_completions = sorted(set(self.completions + identifiers))
        except:
            all_completions = self.completions
        for completion in all_completions:
            if completion.lower().startswith(word_lower) and completion != word:
                matches.append(completion)
        return matches[:10]  # Maksimum 10 öneri göster

    def show_completion_window(self, matches):
        """Öneri penceresini göster"""
        global active_theme
        if not matches:
            self.hide_completion_window()
            return
        self.hide_completion_window()
        try:
            cursor_pos = self.text_area.index(tk.INSERT)
            x, y, _, _ = self.text_area.bbox(cursor_pos)
            x += self.text_area.winfo_rootx() + 10
            y += self.text_area.winfo_rooty() + 25
            self.completion_window = tk.Toplevel(self.text_area)
            self.completion_window.wm_overrideredirect(True)
            self.completion_window.geometry(f"+{x}+{y}")
            self.completion_window.config(bg=active_theme['completer_bg'])
            self.completion_listbox = tk.Listbox(
                self.completion_window,
                height=min(len(matches), 8),
                bg=active_theme['completer_bg'],
                fg=active_theme['completer_fg'],
                selectbackground=active_theme['completer_select_bg'],
                selectforeground=active_theme['completer_select_fg'],
                borderwidth=1,
                relief='solid',
                font=("Consolas", 10)
            )
            self.completion_listbox.pack()
            for match in matches:
                self.completion_listbox.insert(tk.END, match)
            if matches:
                self.completion_listbox.selection_set(0)
                self.completion_listbox.activate(0)
            self.completion_listbox.bind('<Double-Button-1>', lambda e: self.complete_word())
            self.completion_listbox.bind('<Return>', lambda e: self.complete_word())
            self.completion_listbox.bind('<Up>', self.on_listbox_navigate)
            self.completion_listbox.bind('<Down>', self.on_listbox_navigate)
            self.completion_listbox.bind('<Escape>', lambda e: self.hide_completion_window())
            self.completion_window.bind('<FocusOut>', lambda e: self.hide_completion_window())
            # Pencereyi üstte tut
            self.completion_window.wm_transient(self.text_area)
        except tk.TclError:
            self.hide_completion_window()

    def on_listbox_navigate(self, event):
        """Listbox'ta yukarı/aşağı navigasyon"""
        if not self.completion_listbox:
            return
        current = self.completion_listbox.curselection()
        size = self.completion_listbox.size()
        if event.keysym == 'Up':
            new_index = max(0, current[0] - 1) if current else 0
        elif event.keysym == 'Down':
            new_index = min(size - 1, current[0] + 1) if current else 0
        else:
            return
        self.completion_listbox.selection_clear(0, tk.END)
        self.completion_listbox.selection_set(new_index)
        self.completion_listbox.activate(new_index)
        return 'break'

    def complete_word(self):
        """Seçilen kelimeyi tamamla"""
        if not (self.completion_window and self.completion_listbox and self.completion_window.winfo_exists()):
            return
        try:
            selection = self.completion_listbox.curselection()
            if selection and self.word_start_pos:
                selected_word = self.completion_listbox.get(selection[0])
                self.text_area.delete(self.word_start_pos, tk.INSERT)
                self.text_area.insert(self.word_start_pos, selected_word)
                self.text_area.event_generate('<KeyRelease>')  # Syntax highlighter'ı tetikle
        except tk.TclError:
            pass
        finally:
            self.hide_completion_window()

    def hide_completion_window(self, event=None):
        """Öneri penceresini gizle"""
        if self.completion_window and self.completion_window.winfo_exists():
            try:
                self.completion_window.destroy()
            except tk.TclError:
                pass
        self.completion_window = None
        self.completion_listbox = None


def apply_theme_globally(root, text_area, line_numbers_widget, error_label_widget,
                         main_frame_widget, line_frame_widget, scrollbar_widget,
                         highlighter_instance, bracket_matcher_instance, auto_completer_instance,
                         output_area=None, output_label=None, token_tree=None, tree_tree=None):
    global active_theme
    try:
        root.config(bg=active_theme['main_frame_bg'])
        main_frame_widget.config(bg=active_theme['main_frame_bg'])
        text_area.config(
            bg=active_theme['text_area_bg'],
            fg=active_theme['text_area_fg'],
            selectbackground=active_theme['select_bg'],
            insertbackground=active_theme['text_area_fg']
        )
        if output_area and output_area.winfo_exists():
            output_area.config(
                bg=active_theme['output_area_bg'],
                fg=active_theme['output_area_fg']
            )
        if output_label and output_label.winfo_exists():
            output_label.config(bg=active_theme['main_frame_bg'])
        line_frame_widget.config(bg=active_theme['line_numbers_bg'])
        if line_numbers_widget.winfo_exists():
            line_numbers_widget.config(state='normal')
            line_numbers_widget.config(
                bg=active_theme['line_numbers_bg'],
                fg=active_theme['line_numbers_fg']
            )
            line_numbers_widget.config(state='disabled')
        if error_label_widget.winfo_exists():
            error_label_widget.config(bg=active_theme['main_frame_bg'])
        if scrollbar_widget:
            scrollbar_widget.config(
                bg=active_theme['scrollbar_bg'],
                troughcolor=active_theme['scrollbar_troughcolor']
            )
        style = ttk.Style()
        style.configure("Treeview", font=("Consolas", 10), rowheight=25, background=active_theme['analysis_bg'], foreground=active_theme['analysis_fg'])
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        for tag, color in active_theme['highlighter_colors'].items():
            style.configure(f"Treeview.{tag}", foreground=color)
        if token_tree and token_tree.winfo_exists():
            token_tree.tag_configure("comment", foreground=active_theme['highlighter_colors']['COMMENT'])
            token_tree.tag_configure("keyword", foreground=active_theme['highlighter_colors']['KEYWORD'])
            token_tree.tag_configure("identifier", foreground=active_theme['highlighter_colors']['IDENTIFIER'])
            token_tree.tag_configure("number", foreground=active_theme['highlighter_colors']['NUMBER'])
            token_tree.tag_configure("string", foreground=active_theme['highlighter_colors']['STRING'])
            token_tree.tag_configure("string_quote", foreground=active_theme['highlighter_colors']['STRING_QUOTE'])
            token_tree.tag_configure("string_content", foreground=active_theme['highlighter_colors']['STRING_CONTENT'])
            token_tree.tag_configure("escape_char", foreground=active_theme['highlighter_colors']['ESCAPE_CHAR'])
            token_tree.tag_configure("operator", foreground=active_theme['highlighter_colors']['OPERATOR'])
            token_tree.tag_configure("assign", foreground=active_theme['highlighter_colors']['ASSIGN'])
            token_tree.tag_configure("colon", foreground=active_theme['highlighter_colors']['COLON'])
            token_tree.tag_configure("lparen", foreground=active_theme['highlighter_colors']['LPAREN'])
            token_tree.tag_configure("rparen", foreground=active_theme['highlighter_colors']['RPAREN'])
            token_tree.tag_configure("lbracket", foreground=active_theme['highlighter_colors']['LBRACKET'])
            token_tree.tag_configure("rbracket", foreground=active_theme['highlighter_colors']['RBRACKET'])
            token_tree.tag_configure("comma", foreground=active_theme['highlighter_colors']['COMMA'])
        if tree_tree and tree_tree.winfo_exists():
            for node_type, color in active_theme['highlighter_colors'].items():
                tree_tree.tag_configure(node_type.lower(), foreground=color)
        if highlighter_instance:
            highlighter_instance.update_theme_settings()
        if bracket_matcher_instance:
            bracket_matcher_instance.update_theme_settings()
        if auto_completer_instance:
            auto_completer_instance.update_theme_settings()
    except tk.TclError as e:
        print(f"Tema uygulanırken TclError: {e}")
    except Exception as e:
        print(f"Tema uygulanırken genel hata: {e}")

def toggle_theme(root, text_area, line_numbers_widget, error_label_widget,
                 main_frame_widget, line_frame_widget, scrollbar_widget,
                 highlighter_instance, bracket_matcher_instance, auto_completer_instance,
                 output_area=None, output_label=None, token_tree=None, tree_tree=None):
    global active_theme
    if active_theme['name'] == 'light':
        active_theme = dark_theme.copy()
    else:
        active_theme = light_theme.copy()
    apply_theme_globally(root, text_area, line_numbers_widget, error_label_widget,
                         main_frame_widget, line_frame_widget, scrollbar_widget,
                         highlighter_instance, bracket_matcher_instance, auto_completer_instance,
                         output_area, output_label, token_tree, tree_tree)

def get_current_theme_name():
    global active_theme
    return active_theme['name']

def set_theme(theme_name, root, text_area, line_numbers_widget, error_label_widget,
              main_frame_widget, line_frame_widget, scrollbar_widget,
              highlighter_instance, bracket_matcher_instance, auto_completer_instance,
              token_tree=None, tree_tree=None):
    global active_theme
    if theme_name == 'light':
        active_theme = light_theme.copy()
    elif theme_name == 'dark':
        active_theme = dark_theme.copy()
    else:
        return False
    apply_theme_globally(root, text_area, line_numbers_widget, error_label_widget,
                         main_frame_widget, line_frame_widget, scrollbar_widget,
                         highlighter_instance, bracket_matcher_instance, auto_completer_instance,
                         token_tree=token_tree, tree_tree=tree_tree)
    return True

def get_available_themes():
    return ['light', 'dark']

if __name__ == "__main__":
    print("Highlighter modülü yüklendi.")
    print(f"Mevcut temalar: {get_available_themes()}")
    print(f"Aktif tema: {get_current_theme_name()}")