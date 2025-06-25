from markitdown import MarkItDown

def main():
    md = MarkItDown()
    result = md.convert("../resources/test.docx")
    print(result.text_content)

if __name__ == '__main__':
    main()