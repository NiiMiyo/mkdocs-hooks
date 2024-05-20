import frontmatter

from os.path import split, splitext

from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig

def on_files(files: Files, config: MkDocsConfig) -> Files | None:
	for file in files:
		if not file.is_documentation_page():
			continue

		post = frontmatter.loads(file.content_string, encoding='utf-8-sig')
		if post.get('title', None) is not None:
			continue

		dirpath, filename = split(file.src_uri)
		filename_no_ext, file_ext = splitext(filename)

		if filename_no_ext == 'index' and file_ext.lower() == '.md':
			_, post['title'] = split(dirpath)
		else:
			post['title'] = filename_no_ext

		file.content_string = frontmatter.dumps(post)
