from pdfminer.high_level import extract_text_to_fp

def pdf(fin_path, fout_path):
    with open(fin_path, 'rb') as fin:
        with open(fout_path, 'wb') as fout:
            extract_text_to_fp(fin, fout, output_type='text')

if __name__ == '__main__':
    pdf("C:\\Users\\micr1\\Desktop\\pumpkin_book.pdf", "C:\\Users\\micr1\\Desktop\\test.txt")