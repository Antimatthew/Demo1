import PyPDF2
import os

def read_pdf_content(pdf_path):
    """
    读取PDF文件内容并返回文本
    
    Args:
        pdf_path: PDF文件路径
    
    Returns:
        str: 提取的文本内容
    """
    if not os.path.exists(pdf_path):
        print(f"错误：文件 '{pdf_path}' 不存在")
        return ""
    
    try:
        with open(pdf_path, 'rb') as file:
            # 创建PDF读取器对象
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 获取PDF页数
            num_pages = len(pdf_reader.pages)
            print(f"PDF文件包含 {num_pages} 页")
            
            # 提取所有页的文本
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                text += f"\n\n--- 第 {page_num + 1} 页 --\n{page_text}"
            
            return text
    
    except PyPDF2.errors.PdfReadError:
        print("错误：无法读取PDF文件，可能是损坏或加密的文件")
        return ""
    except Exception as e:
        print(f"读取PDF时发生错误：{str(e)}")
        return ""

if __name__ == "__main__":
    # PDF文件路径
    pdf_file = "YourFirstWebapp.pdf"
    
    # 读取PDF内容
    print(f"正在读取文件: {pdf_file}")
    content = read_pdf_content(pdf_file)
    
    # 打印部分内容作为示例（避免输出过长）
    if content:
        print("\n=== PDF内容预览 ===")
        # 只显示前500个字符作为预览
        preview = content[:500] + ("..." if len(content) > 500 else "")
        print(preview)
        
        # 保存完整内容到文本文件
        output_file = "pdf_content.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n完整内容已保存到 '{output_file}'")
    else:
        print("未能提取PDF内容")