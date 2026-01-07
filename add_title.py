from os.path import split, splitext
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from mkdocs.structure.pages import Page
	from mkdocs.structure.files import Files
	from mkdocs.config.defaults import MkDocsConfig

def on_page_markdown( markdown: str, page: 'Page', config: "MkDocsConfig", files: "Files" ):
	if ( not page.file.is_documentation_page() ) or ( page.meta.get( 'title', None ) is not None ):
		return;

	dirpath, filename = split( page.file.src_uri )
	filename_no_ext, file_ext = splitext( filename )

	if filename_no_ext == 'index' and file_ext.lower() == '.md':
		_, page.title = split( dirpath ) #type: ignore

	else:
		page.title = filename_no_ext #type: ignore
