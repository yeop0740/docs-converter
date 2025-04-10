from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("로그 설정.pdf")
print(result.text_content)
