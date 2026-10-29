from docx import Document
from pathlib import Path
p=Path(r'C:\Users\cheel\Downloads\lost-item-intelligence-network\PROJECT_REPORT.docx')
d=Document(p)
print('paragraphs', len(d.paragraphs), 'tables', len(d.tables), 'sections', len(d.sections))
for para in d.paragraphs:
    if para.style.name.startswith('Heading') or para.style.name == 'Title':
        print(para.style.name + ': ' + para.text)
print('WORD_COUNT', sum(len(x.text.split()) for x in d.paragraphs)+sum(len(c.text.split()) for t in d.tables for row in t.rows for c in row.cells))
