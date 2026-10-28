import re
from html.parser import HTMLParser

class MarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.skip = False
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.list_stack = []
        self.in_code = False
        
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
            return
        if tag == 'h1':
            self.markdown.append('\n# ')
        elif tag == 'h2':
            self.markdown.append('\n## ')
        elif tag == 'h3':
            self.markdown.append('\n### ')
        elif tag == 'h4':
            self.markdown.append('\n#### ')
        elif tag == 'p':
            self.markdown.append('\n')
        elif tag in ['strong', 'b']:
            self.markdown.append('**')
        elif tag in ['em', 'i']:
            self.markdown.append('*')
        elif tag == 'code':
            self.markdown.append('`')
            self.in_code = True
        elif tag == 'pre':
            self.markdown.append('\n```')
        elif tag == 'a':
            href = dict(attrs).get('href', '')
            if href:
                self.markdown.append('[')
        elif tag == 'img':
            src = dict(attrs).get('src', '')
            alt = dict(attrs).get('alt', '')
            if src:
                self.markdown.append(f'![{alt}]({src})')
        elif tag == 'br':
            self.markdown.append('\n')
        elif tag == 'hr':
            self.markdown.append('\n---\n')
        elif tag in ['ul', 'ol']:
            self.list_stack.append(tag)
        elif tag == 'li':
            if self.list_stack and self.list_stack[-1] == 'ul':
                self.markdown.append('\n- ')
            elif self.list_stack and self.list_stack[-1] == 'ol':
                self.markdown.append('\n1. ')
        elif tag == 'blockquote':
            self.markdown.append('\n> ')
        elif tag == 'table':
            self.markdown.append('\n')
        elif tag == 'tr':
            self.markdown.append('| ')
        elif tag in ['td', 'th']:
            self.markdown.append(' | ')
            
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
            return
        if tag in ['strong', 'b']:
            self.markdown.append('**')
        elif tag in ['em', 'i']:
            self.markdown.append('*')
        elif tag == 'code':
            self.markdown.append('`')
            self.in_code = False
        elif tag == 'pre':
            self.markdown.append('\n```')
        elif tag == 'a':
            self.markdown.append(']')
        elif tag in ['ul', 'ol']:
            self.list_stack.pop()
        elif tag == 'p':
            self.markdown.append('\n')
        elif tag == 'tr':
            self.markdown.append(' |\n')
        elif tag == 'table':
            self.markdown.append('\n')
            
    def handle_data(self, data):
        if not self.skip:
            self.markdown.append(data)

with open('/Users/deane/Documents/workspace-other/robot-engineer-learning-path/index.html', 'r') as f:
    html = f.read()

converter = MarkdownConverter()
converter.feed(html)
text = ''.join(converter.markdown)

# Clean up excessive whitespace
text = re.sub(r'\n{3,}', '\n\n', text)
text = text.strip()

with open('/Users/deane/Documents/workspace-other/robot-engineer-learning-path/content.md', 'w') as f:
    f.write(text)

print(f'Converted to {len(text)} characters')
print('First 800 chars:')
print(text[:800])
