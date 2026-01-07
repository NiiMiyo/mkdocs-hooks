from os.path import split, splitext

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from mkdocs.structure.files import Files
	from mkdocs.config.defaults import MkDocsConfig

def on_files(files: 'Files', config: 'MkDocsConfig') -> 'Files | None':
	for f in files:
		if not f.is_documentation_page():
			continue

		dirpath, filename = split(f.src_uri)
		_, dirname = split(dirpath)

		filename_no_ext, ext = splitext(filename)

		if dirname == filename_no_ext and ext.lower() == '.md':
			f.name = 'index'

			f.url = split(f.url)[0]
			f.dest_uri = split(f.dest_uri)[0] + '/index.html'
			f.abs_dest_path = split(f.abs_dest_path)[0] + '/index.html'
