# TODO: Title page.

import html
import os
from html import escape as html_escape
from zipfile import ZipFile
from os.path import join, relpath

CHAPTER_PREFIX = "## "
MONO = "```"

input = open('c:/Users/lucas nate/Downloads/marked_after_facebook.txt', mode='r', encoding='utf-8')
html = open('c:/Users/lucas nate/Downloads/hungry_ghosts.html', mode='w', encoding='utf-8')
epub_root = 'c:/Users/lucas nate/Downloads/hungry_ghosts_epub'
epub_zip = 'c:/Users/lucas nate/Downloads/hungry_ghosts.epub'
first_page = '''<h1>רוחות רעבות</h1>
	<h2>מאת: לוקאס נייט</h2>
	<h3>עריכה: אביבית משמרי</h3>
	<h3>עריכה לשונית: אביבית משמרי, מיכאל פטלן, נועה לביא, רמיאל וולדניצקי, דורון צור</h3>
	'''

chapter_idx = 1
chapter_titles = []
chapter_epub_file = None

def finish_existing_paragraph():
	global in_paragraph
	if in_paragraph:
		for f in [html, chapter_epub_file]:
			f.write("</p>\n")
	in_paragraph = False
	
def finish_existing_epub_chapter():
	if chapter_epub_file:
		finish_existing_paragraph()
		chapter_epub_file.write("</body></html>")
		close_epub_file(chapter_epub_file)

def begin_chapter_epub(line):
	global chapter_epub_file
	finish_existing_epub_chapter()
	chapter_epub_file = open_epub_file(f'chapter_{chapter_idx}.xhtml')
	chapter_epub_file.write(f'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="he" xml:lang="he" dir="rtl">
  <head>
    <style>
		.mono {{
		    font-family: Monospace;
		}}
	</style>
    <title>{html_escape(line)}</title>
  </head>
  <body>
  <h2>{html_escape(line)}</h2>''')

def begin_chapter(line):
	assert not in_mono and not in_paragraph
	line = line[len(CHAPTER_PREFIX):]
	begin_chapter_html(line)
	begin_chapter_epub(line)

	global chapter_titles
	global chapter_idx
	chapter_idx += 1
	chapter_titles.append(html_escape(line))
  
def begin_chapter_html(line):
	html.write(f'<h2 id="chapter{chapter_idx}">' + html_escape(line) + "</h2>\n")

in_mono = False
	
def begin_or_end_mono():
	global in_mono
	in_mono = not in_mono
			
in_paragraph = False
	
def begin_paragraph_if_not_existing():
	global in_paragraph
	if not in_paragraph:
		for f in [html, chapter_epub_file]:
			if in_mono:
				f.write(f'<p class="mono">')
			else:
				f.write("<p>")
		in_paragraph = True
	
def add_text_to_paragraph(line):
	br = "<br/>" if in_mono and in_paragraph else ""
	begin_paragraph_if_not_existing()
	for f in [html, chapter_epub_file]:
		f.write(br + html_escape(line) + "\n")

def open_epub_file(fn):
	return open(join(epub_root, fn), 'w', encoding='utf-8')
	
def close_epub_file(f):
	fn = relpath(f.name, epub_root)
	f.close()
	with ZipFile(epub_zip, 'a') as z:
		z.write(join(epub_root, fn), arcname=fn)
	
def write_to_epub_file(fn, txt):
	f = open_epub_file(fn)
	f.write(txt)
	close_epub_file(f)
	
def begin_document():
	begin_document_html()
	begin_document_epub()
	
def begin_document_epub():
	os.makedirs(join(epub_root, 'META-INF'), exist_ok=True)
	ZipFile(epub_zip, 'w').close()
	write_to_epub_file("mimetype", 'application/epub+zip')
	write_to_epub_file(join("META-INF", "container.xml"), '''<?xml version='1.0' encoding='utf-8'?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile media-type="application/oebps-package+xml" full-path="content.opf"/>
  </rootfiles>
</container>
	''')
	
def begin_document_html():
	html.write(f'''
	<html>
	<head>
	<style>
		body {{
			direction: rtl;
			font-family: Arial, Tahoma, Helvetica, FreeSans, sans-serif;
			font-size: 21px;
			line-height: 1.5;
			background-color: #292929; 
			color: #eeeeee;
		}}
		.mono {{
		    font-family: Courier, "Courier New", Monospace;
		}}
		a {{
			background-color: inherit; 
			color: inherit;		
		}}
		
		@media only screen and (min-width: 210mm) {{
  		.main {{
		    width: 148mm;
			margin: auto;
		}}
		.stylechanger {{
		    position: fixed;
			left: 0px;
			top: 0px;
			width: 30mm;
			z-index: 1000;
			font-size: 75%;
		}}
		.toc {{
		    position: fixed;
			right: 0px;
			top: 0px;
			width: 20mm;
			z-index: 1000;
			font-size: 75%;
		}}
		.footer {{
		    display: none;
		}}
		}}
		@media only screen and (max-width: 210mm) {{
		.stylechanger{{
			display: none;
		}}
		.toc {{
			display: none;
		}}
		.footer {{
		    position: fixed;
			bottom: 0px;
			height: 10mm;
			z-index: 1000;
			background-color: #314571;
			overflow: hidden;
			color: #ffec6c;
			width: 100%;
			left: 0;
		}}
		.footer_left {{
		    right: 0;
			display: inline;
			position: absolute;
		}}
		.footer_right {{
		    left: 0;
			display: inline;
			position: absolute;
		}}
		body {{
		    min-height: 30mm;
			margin-bottom: 10mm;
		}}
		}}
	</style>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
	<meta charset="UTF-8"/>
	</head>
	<body>
	<div class="stylechanger">
	  <h1>תצוגה</h1>
	  <a href="javascript:night()">לבן על גבי שחור</a><br/>
	  <a href="javascript:soft()">שחור על גבי לבן</a><br/>
	  <noscript>לא עובד בלי גאווהסקריפט</noscript>
	</div>
	<script>
	function night() {{
	  var style = document.createElement('style');
	  style.innerHTML = `
	  body {{ background-color: #292929; color: #eeeeee; }}
	  `;
	  document.head.appendChild(style);
	  document.getElementById('darkmode').checked = true;
	}}
	function soft() {{
	  var style = document.createElement('style');
	  style.innerHTML = `
	  body {{ background-color: #ffeccc; color: #000000; }}
	  `;
	  document.head.appendChild(style);
	  document.getElementById('darkmode').checked = false;
	}}
	function nightModeClick() {{
	  if (document.getElementById('darkmode').checked) {{
	    night();
	  }} else {{
	    soft();
	  }}
	}}
	</script>
	<div class="main">
	{first_page}
	''')
	
def end_document():
	end_document_html()
	end_document_epub()
	
def end_document_html():
	if in_paragraph:
		html.write("</p>")
	html.write('''
	</div>
    <div class="toc"><h1>פרקים</h1>
	''')
	for i in range(1, chapter_idx):
		html.write(f'<a href="#chapter{i}" onclick="document.getElementById(\'chapter\').value = \'#chapter{i}\'">{chapter_titles[i - 1]}</a><br/>\n')
	html.write('''
	</div><div class="footer">
	<div class="footer_left">פרק: <select id="chapter" onchange="window.location.href=this.value">
	''')
	for i in range(1, chapter_idx):
		html.write(f'<option value="#chapter{i}">{chapter_titles[i - 1]}</option>')
	html.write('''
	</select></div>
	<div class="footer_right" onclick="nightModeClick()">מצב לילה: <input id="darkmode" type="checkbox" checked/></div>
	</div>
	<script>
	document.getElementById("chapter").value = window.location.href.substr(window.location.href.indexOf('#'));
	</script>
	</body></html>
	''')

def end_document_epub():
	chapters = [f'<item href="chapter_{i}.xhtml" id="chapter_{i}" media-type="application/xhtml+xml"/>' for i in range(1, chapter_idx)]
	chapters2 = [f'<itemref idref="chapter_{i}"/>' for i in range(1, chapter_idx)]
	chapters3 = [f'''<navPoint id="chapter_{i}">
                       <navLabel>
                         <text>{chapter_titles[i-1]}</text>
                       </navLabel>
                       <content src="chapter_{i}.xhtml"/>
                     </navPoint>
				  ''' for i in range(1, chapter_idx)]
	chapters4 = [f'''<li>
                       <a href="chapter_{i}.xhtml">{chapter_titles[i-1]}</a>
                     </li>''' for i in range(1, chapter_idx)]
	lf = '\n'
	write_to_epub_file("content.opf", f'''<?xml version='1.0' encoding='utf-8'?>
<package unique-identifier="id" version="3.0" xmlns="http://www.idpf.org/2007/opf" prefix="rendition: http://www.ipdf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <meta property="dcterms:modified">2018-09-12T00:23:24Z</meta>
    <dc:identifier id="id">THERE_IS_NO_UNIQUE_IDENTIFIER_BECAUSE_THIS_IS_UNDERGROUND_LITERATURE</dc:identifier>
    <dc:creator id="creator">לוקאס נייט</dc:creator>
    <dc:language>he</dc:language>
    <dc:title>רוחות רעבות</dc:title>
  </metadata>
  <manifest>
    {lf.join(chapters)}
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
    <item href="nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine toc="ncx" page-progression-direction="rtl">
    <itemref idref="nav"/>
	{lf.join(chapters2)}
  </spine>
</package>
	''')
	write_to_epub_file("toc.ncx", f'''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta content="THERE_IS_NO_UNIQUE_IDENTIFIER_BECAUSE_THIS_IS_UNDERGROUND_LITERATURE" name="dtb:uid"/>
    <meta content="0" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>רוחות רעבות</text>
  </docTitle>
  <navMap>
	{lf.join(chapters3)}  
  </navMap>
</ncx>
    ''')
	write_to_epub_file("nav.xhtml", f'''<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="he" xml:lang="he" dir="rtl">
  <head>
    <title>רוחות רעבות</title>
    <style type="text/css">
     ul {{
      list-style-type: none;
     }}
    </style>
  </head>
  <body>
    <nav id="id" epub:type="toc">
      {first_page}
	  <h2>תוכן עניינים</h2>
      <ul>
	     {lf.join(chapters4)}
      </ul>
    </nav>
  </body>
</html>
    ''')

def main():	
	begin_document()
	for line in input:
		line = line.rstrip()
		if line.startswith(CHAPTER_PREFIX):
			begin_chapter(line)
		elif line == MONO:
			begin_or_end_mono()
		elif line == "" or line.isspace():
			finish_existing_paragraph()
		else:
			add_text_to_paragraph(line)
	finish_existing_epub_chapter()
	end_document()		

main()	
