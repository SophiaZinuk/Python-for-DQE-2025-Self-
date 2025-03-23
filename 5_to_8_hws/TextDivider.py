class TextDivider:
    def __init__(self, divider):
        self.divider = divider

    def split_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
 
        return self.split_text(text)
 
    def split_text(self, text):
        return [block.strip() for block in text.split(self.divider) if block.strip()]
 