import matplotlib.pyplot as plt
import numpy as np
if __name__ == '__main__':
    categories = [
        'alt.atheism',
        'comp.graphics',
        'comp.os.ms-windows.misc',
        'comp.sys.ibm.pc.hardware',
        'comp.sys.mac.hardware',
        'comp.windows.x',
        'misc.forsale',
        'rec.autos',
        'rec.motorcycles',
        'rec.sport.baseball',
        'rec.sport.hockey',
        'sci.crypt',
        'sci.electronics',
        'sci.med',
        'sci.space',
        'soc.religion.christian',
        'talk.politics.guns',
        'talk.politics.mideast',
        'talk.politics.misc',
        'talk.religion.misc']

    res = []
    for i in categories:
        with open(i+".txt", "r", encoding='utf-8') as f:
            res_txt = (f.read()
                .split('result: ')[-1]
                .replace("vector=", '')
                .replace("jaccard=", '')
                .replace("editdistance=", '')
                .replace("total=", '')
                .split(' '))
            res.append([i, round(float(res_txt[0]),4), round(float(res_txt[1]),4), int(res_txt[2]), int(res_txt[3])])
    res.sort(key=lambda x:x[1])

    cm = plt.get_cmap('Spectral')
    colors = cm(np.linspace(0, 1, len(categories)))

    plt.title('vector similarity')
    plt.subplots_adjust(left=0.3)
    plt.grid(axis="x")
    bars = plt.barh(categories, [i[1] for i in res])
    plt.xticks(np.linspace(0, 1, num=11))
    plt.yticks(rotation=30)
    for bar, color in zip(bars, colors):
        bar.set_color(color)
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}", ha='left',
                 va='center')
    plt.savefig('vector-similarity.png', dpi=600)
    plt.cla()

    plt.title('jaccard similarity')
    plt.subplots_adjust(left=0.3)
    plt.grid(axis="x")
    bars = plt.barh(categories, [i[2] for i in res])
    plt.xticks(np.linspace(0, 1, num=11))
    plt.yticks(rotation=30)
    for bar, color in zip(bars, colors):
        bar.set_color(color)
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.2f}", ha='left',
                 va='center')
    plt.savefig('jaccard-similarity.png', dpi=600)
    plt.cla()

    plt.axis('off')
    plt.title('similarity')
    table = plt.table(cellText=res, colLabels=['category', 'vector similarity', 'jaccard similarity', 'editdistance', 'total word'], loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    for i, col in enumerate(res[0]):
        max_len = max(len(str(cell)) for cell in [row[i] for row in res])
        table.auto_set_column_width([i])  # 自动设置列宽
    plt.savefig('similarity.png', dpi=600)