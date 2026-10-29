from docx import Document
p=r'C:\Users\cheel\Downloads\lost-item-intelligence-network\PROJECT_REPORT.docx'
d=Document(p)
for i,x in enumerate(d.paragraphs):
 t=x.text.strip()
 if any(q in t.lower() for q in ['not run','not been run','unavailable','not verified','verification record','jenkins','sonarqube','student1','lazy','csrf','port 8091','localhost:8080','docker build','external integration','17 tests','18 tests','dashboard']):
  print(f'{i}: {t}')
