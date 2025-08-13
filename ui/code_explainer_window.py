import threading
from gi.repository import Gtk, Gdk, GObject

from api.gemini_api import get_code_explanation
from utils.syntax_highlighting import apply_syntax_highlighting


class CodeExplainerWindow(Gtk.Window):
    def __init__(self, selected_code):
        super().__init__(title="🔍 Code Explainer")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.selected_code = selected_code
        self.apply_css()
        self.connect("key-press-event", self.on_key_press)
        self.set_can_focus(True)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_left(20)
        main_box.set_margin_right(20)
        # Add CSS class to main_box for background styling
        main_box.get_style_context().add_class("main-container")
        
        title_label = Gtk.Label()
        
        main_box.pack_start(title_label, False, False, 0)
        code_frame = Gtk.Frame(label="Selected code")
        code_frame.get_label_widget().set_markup('<span weight="bold" color="#FF9800">Selected code</span>')
        code_frame.get_style_context().add_class("code-frame")
        code_scrolled = Gtk.ScrolledWindow()
        code_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        code_scrolled.set_min_content_height(300)
        
        self.code_textview = Gtk.TextView()
        self.code_textview.set_editable(False)
        self.code_textview.get_style_context().add_class("code-view")
        self.code_textview.set_top_margin(15)
        self.code_textview.set_left_margin(10)
        self.code_textview.set_right_margin(10)
        self.code_textview.set_bottom_margin(15)
        self.code_textview.set_wrap_mode(Gtk.WrapMode.NONE)
        
        apply_syntax_highlighting(self.code_textview, selected_code)
        code_scrolled.add(self.code_textview)
        code_frame.add(code_scrolled)
        main_box.pack_start(code_frame, True, True, 0)
        
        explanation_frame = Gtk.Frame(label="Description")
        explanation_frame.get_label_widget().set_markup('<span weight="bold" color="#4CAF50">Description</span>')
        explanation_scrolled = Gtk.ScrolledWindow()
        explanation_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        explanation_scrolled.set_min_content_height(220)
        
        self.explanation_textview = Gtk.TextView()
        self.explanation_textview.set_editable(False)
        self.explanation_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.explanation_textview.get_style_context().add_class("explanation-view")
        
        explanation_scrolled.add(self.explanation_textview)
        explanation_frame.add(explanation_scrolled)
        main_box.pack_start(explanation_frame, True, True, 0)
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_text("Explaining the code...")
        self.progress_bar.set_show_text(True)
        
        main_box.pack_start(self.progress_bar, False, False, 0)
        self.close_button = Gtk.Button(label="Close")
        self.close_button.connect("clicked", self.on_close_clicked)
        self.close_button.get_style_context().add_class("close-button")
        
        main_box.pack_start(self.close_button, False, False, 0)
        self.add(main_box)
        self.start_explanation()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_space:
            self.on_close_clicked(None)
            return True
        return False

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_data = """
        /* Set window background to dark color matching the code view */
        window {
            background-color: #1e1e1e;
        }
        
        /* Set main container background to match */
        .main-container {
            background-color: #1e1e1e;
        }
        
        .code-view {
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 16px;
        }
        .explanation-view {
            background-color: #e8f5e8;
            color: #2d5016;
            font-family: 'Tahoma', sans-serif;
            font-size: 18px;
        }
        .explanation-view text {
            padding: 14px;
            margin: 0px;
        }
        .close-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            font-weight: bold;
            border-radius: 8px;
            min-height: 50px;
            font-size: 14px;
        }
        """
        css_provider.load_from_data(css_data.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def insert_formatted_text(self, buffer, text, bold_tag, italic_tag, rtl_tag):
        import re
        bold_pattern = r'\*\*(.*?)\*\*'
        italic_pattern = r'\*(.*?)\*'
        last_end = 0
        all_matches = []
        for match in re.finditer(bold_pattern, text):
            all_matches.append((match.start(), match.end(), 'bold', match.group(1)))
        for match in re.finditer(italic_pattern, text):
            is_inside_bold = False
            for bold_match in re.finditer(bold_pattern, text):
                if bold_match.start() <= match.start() and match.end() <= bold_match.end():
                    is_inside_bold = True
                    break
            if not is_inside_bold:
                all_matches.append((match.start(), match.end(), 'italic', match.group(1)))
        all_matches.sort(key=lambda x: x[0])
        if not all_matches:
            buffer.insert_with_tags(buffer.get_end_iter(), text, rtl_tag)
            return
        for start, end, format_type, content in all_matches:
            if start > last_end:
                buffer.insert_with_tags(buffer.get_end_iter(), text[last_end:start], rtl_tag)
            if format_type == 'bold':
                buffer.insert_with_tags(buffer.get_end_iter(), content, bold_tag, rtl_tag)
            elif format_type == 'italic':
                buffer.insert_with_tags(buffer.get_end_iter(), content, italic_tag, rtl_tag)
            last_end = end
        if last_end < len(text):
            buffer.insert_with_tags(buffer.get_end_iter(), text[last_end:], rtl_tag)

    def start_explanation(self):
        def explain_in_thread():
            explanation = get_code_explanation(self.selected_code)
            GObject.idle_add(self.update_explanation, explanation)
        thread = threading.Thread(target=explain_in_thread)
        thread.daemon = True
        thread.start()
        GObject.timeout_add(100, self.pulse_progress)

    def pulse_progress(self):
        if self.progress_bar.get_visible():
            self.progress_bar.pulse()
            return True
        return False

    def update_explanation(self, explanation):
        self.progress_bar.hide()
        explanation_buffer = self.explanation_textview.get_buffer()
        explanation_buffer.delete(explanation_buffer.get_start_iter(), explanation_buffer.get_end_iter())
        bold_tag = explanation_buffer.create_tag("bold", weight=700)
        italic_tag = explanation_buffer.create_tag("italic", style=3)
        rtl_tag = explanation_buffer.create_tag("rtl", direction=2)
        self.insert_formatted_text(explanation_buffer, explanation, bold_tag, italic_tag, rtl_tag)

    def on_close_clicked(self, button):
        self.destroy()