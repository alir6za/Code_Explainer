try:
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.lexers.special import TextLexer
    from pygments.token import Token
    PYGMENTS_AVAILABLE = True
except Exception:
    PYGMENTS_AVAILABLE = False
    print("Warning: Pygments not installed. Install with: pip install pygments")

def detect_language(code):
    code_lower = code.lower()
    code_lines = code.split('\n')
    
    # Python detection 
    python_indicators = ['def ', 'import ', 'from ', 'class ', 'if __name__', 'print(', 
                        '"""', "'''", 'self.', 'elif ', '@', 'lambda ', 'with ', 'as ']
    if any(indicator in code for indicator in python_indicators):
        return 'python'
    
    # C/C++ detection
    c_indicators = ['#include', '#define', 'int main', 'void main', 'printf(', 'scanf(',
                   'malloc(', 'free(', 'struct ', 'typedef ', '#pragma', 'cout<<', 'cin>>',
                   'std::', 'namespace ', 'class ', 'public:', 'private:', 'protected:']
    if any(indicator in code for indicator in c_indicators):
        if 'cout' in code or 'cin' in code or 'std::' in code or 'namespace' in code:
            return 'cpp'
        return 'c'
    
    # Java detection
    java_indicators = ['public class', 'private class', 'protected class', 'import java',
                      'System.out.', 'public static void main', 'extends ', 'implements ',
                      'package ', '@Override', 'ArrayList', 'HashMap']
    if any(indicator in code for indicator in java_indicators):
        return 'java'
    
    # JavaScript/TypeScript detection
    js_indicators = ['function ', 'var ', 'let ', 'const ', '=>', 'console.log',
                    'document.', 'window.', 'addEventListener', 'querySelector',
                    'require(', 'module.exports', 'export ', 'import {', '$(']
    if any(indicator in code for indicator in js_indicators):
        if 'interface ' in code or ': string' in code or ': number' in code:
            return 'typescript'
        return 'javascript'
    
    # HTML detection
    html_indicators = ['<html', '<!doctype', '<head>', '<body>', '<div', '<p>', '<a ',
                      '<script>', '<style>', '<link', '<meta']
    if any(indicator in code_lower for indicator in html_indicators):
        return 'html'
    
    # CSS detection
    css_indicators = ['{', '}', ':', ';', 'background:', 'color:', 'margin:', 'padding:',
                     '@media', '.class', '#id', 'font-family:', 'display:']
    if code.count('{') > 0 and code.count('}') > 0 and any(indicator in code for indicator in css_indicators):
        return 'css'
    
    # SQL detection
    sql_keywords = ['select ', 'insert ', 'update ', 'delete ', 'create ', 'drop ',
                   'alter ', 'from ', 'where ', 'join ', 'group by', 'order by',
                   'having ', 'union ', 'exists ', 'count(']
    if any(keyword in code_lower for keyword in sql_keywords):
        return 'sql'
    
    # Shell/Bash detection
    bash_indicators = ['#!/bin/bash', '#!/bin/sh', 'echo ', 'ls ', 'cd ', 'mkdir ',
                      'rm ', 'cp ', 'mv ', 'grep ', 'awk ', 'sed ', 'chmod ',
                      'if [ ', 'fi', 'do', 'done', 'case ', 'esac']
    if any(indicator in code for indicator in bash_indicators):
        return 'bash'
    
    # Go detection
    go_indicators = ['package ', 'func ', 'import (', 'var ', 'type ', 'struct {',
                    'interface {', 'go ', 'defer ', 'chan ', 'goroutine']
    if any(indicator in code for indicator in go_indicators):
        return 'go'
    
    # Rust detection
    rust_indicators = ['fn ', 'let ', 'mut ', 'struct ', 'enum ', 'impl ',
                      'trait ', 'use ', 'mod ', 'pub ', 'match ', '&str']
    if any(indicator in code for indicator in rust_indicators):
        return 'rust'
    
    # PHP detection
    php_indicators = ['<?php', '<?=', '$_GET', '$_POST', 'echo ', 'function ',
                     'class ', 'public function', 'private function', 'require_once']
    if any(indicator in code for indicator in php_indicators):
        return 'php'
    
    # JSON detection
    if code.strip().startswith('{') and code.strip().endswith('}') and '"' in code:
        try:
            import json
            json.loads(code)
            return 'json'
        except:
            pass
    
    # XML detection
    if code.strip().startswith('<') and code.strip().endswith('>') and '</' in code:
        return 'xml'
    
    return 'text'

def create_syntax_tags(buffer):
    tag_table = buffer.get_tag_table()

    def ensure_tag(name, **kwargs):
        if not tag_table.lookup(name):
            buffer.create_tag(name, **kwargs)

    ensure_tag("keyword", foreground="#569cd6", weight=700)
    ensure_tag("string", foreground="#ce9178")
    ensure_tag("comment", foreground="#6a9955", style=3)
    ensure_tag("number", foreground="#b5cea8")
    ensure_tag("operator", foreground="#d4d4d4")
    ensure_tag("function", foreground="#dcdcaa", weight=600) 
    ensure_tag("function-builtin", foreground="#4fc1ff", weight=600)
    ensure_tag("class", foreground="#4ec9b0", weight=600)
    ensure_tag("variable", foreground="#9cdcfe")
    ensure_tag("name", foreground="#9cdcfe") 
    ensure_tag("decorator", foreground="#ffd700", weight=600) 
    ensure_tag("punctuation", foreground="#d4d4d4")
    ensure_tag("text", foreground="#d4d4d4")

def get_tag_for_token_type(token_type):
    token_str = str(token_type)
    
    if 'Name.Function' in token_str:
        return "function"
    elif 'Name.Builtin' in token_str:
        return "function-builtin"
    elif 'Name.Decorator' in token_str:
        return "decorator"
    elif 'Keyword' in token_str:
        return "keyword"
    elif 'Name.Class' in token_str:
        return "class"
    elif 'String' in token_str:
        return "string"
    elif 'Comment' in token_str:
        return "comment"
    elif 'Number' in token_str or 'Literal.Number' in token_str:
        return "number"
    elif 'Operator' in token_str:
        return "operator"
    elif 'Punctuation' in token_str:
        return "punctuation"
    elif 'Name' in token_str:
        return "name"
    else:
        return "text"

def apply_syntax_highlighting(code_textview, code):
    code_buffer = code_textview.get_buffer()
    if not PYGMENTS_AVAILABLE:
        code_buffer.set_text(code)
        return
    
    try:
        lexer = None
        detected_language = None
        
        try:
            lexer = guess_lexer(code)
            print(f"Pygments detected language: {lexer.name}")
        except Exception as e:
            print(f"Pygments guess failed: {e}")
            
        if lexer is None or isinstance(lexer, TextLexer):
            detected_language = detect_language(code)
            print(f"Manual detection: {detected_language}")
            try:
                if detected_language != 'text':
                    lexer = get_lexer_by_name(detected_language)
                    print(f"Using lexer for: {detected_language}")
                else:
                    lexer = TextLexer()
            except Exception as e:
                print(f"Failed to get lexer for {detected_language}: {e}")
                lexer = TextLexer()

        code_buffer.delete(code_buffer.get_start_iter(), code_buffer.get_end_iter())
        create_syntax_tags(code_buffer)
        tag_table = code_buffer.get_tag_table()

        tokens = list(lexer.get_tokens(code))
        print(f"Generated {len(tokens)} tokens")
        
        for i, (token_type, value) in enumerate(tokens):
            if value.strip():
                tag_name = get_tag_for_token_type(token_type)
                
                if tag_name in ["name", "text"]:
                    next_tokens = tokens[i+1:i+4] if i+1 < len(tokens) else []
                    for j, (next_token_type, next_value) in enumerate(next_tokens):
                        if next_value.strip() == '(':
                            tag_name = "function"
                            break
                        elif next_value.strip() and next_value.strip() not in [' ', '\n', '\t', '.']:
                            break
                
                tag = tag_table.lookup(tag_name) if tag_name else None
                if tag is not None:
                    code_buffer.insert_with_tags(code_buffer.get_end_iter(), value, tag)
                else:
                    code_buffer.insert(code_buffer.get_end_iter(), value)
            else:
                code_buffer.insert(code_buffer.get_end_iter(), value)
                
    except Exception as e:
        print(f"Syntax highlighting error: {e}")
        code_buffer.delete(code_buffer.get_start_iter(), code_buffer.get_end_iter())
        code_buffer.set_text(code)