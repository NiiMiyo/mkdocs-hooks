import unicodedata
import regex
from urllib.parse import quote
from os.path import splitext, split, relpath

from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files, File
from mkdocs.config.defaults import MkDocsConfig

WIKILINK_PATTERN = regex.compile(r"\[\[([^\]|]+)(?:\|([^\]]*))?\]\]")

available_files: Files = None # type: ignore - will be initialized later

def on_files(files: Files, config: MkDocsConfig) -> Files | None:
	global available_files

	available_files = files

def on_page_markdown(markdown: str, *, page: Page, **_):
	global WIKILINK_PATTERN

	wikilink_matches = WIKILINK_PATTERN.finditer(markdown)

	while True:
		match = next(wikilink_matches, None)
		if match is None: break

		start, end = match.start(0), match.end(0)
		filename, text = match.group(1), match.group(2)

		replacement = get_wikilink_replacement(page.file, filename, text)
		markdown = markdown[:start] + replacement + markdown[end:]
		wikilink_matches = WIKILINK_PATTERN.finditer(markdown)

	return markdown


def get_wikilink_replacement(origin: File, destination_uri: str, text: str | None) -> str:
	destination_uri, fragment = remove_fragment(destination_uri)
	destination_file = get_file_from_filepath(destination_uri, origin)

	if destination_file is not None:
		destination_uri = destination_file.src_uri
		href = quote(relpath(destination_uri, origin.src_uri + '/..').replace('\\', '/')) + parse_fragment(fragment)

		page = destination_file.page

		if page is not None:
			tooltip: str = page.title or "" # type: ignore
			# page.title marked as of type 'weak_property | Unknown' instead of 'str | None'
		else:
			tooltip = ''

		if fragment:
			tooltip += f" > {fragment[1:]}"

	else:
		href = destination_uri
		tooltip = ""
		page = None

	if not text:
		if fragment is not None:
			text = fragment[1:]

		elif destination_file is None:
			text = destination_uri

		elif page is not None:
			filename, _ = splitext( split(destination_file.src_uri)[1] )
			text = filename


	if not tooltip or (text and tooltip.lower() == text.lower()):
		tooltip = ""
	else:
		tooltip = f" \"{tooltip}\""

	return f"[{text or ""}]({href}{tooltip})"

def remove_fragment(filepath: str) -> tuple[str, str | None]:
	fragment_start = filepath.find("#")
	if fragment_start == -1:
		return filepath, None

	return filepath[:fragment_start], filepath[fragment_start:]

def get_file_from_filepath(filepath: str, origin: File) -> File | None:
	global available_files

	filepath, _ = remove_fragment(filepath.strip())

	if filepath == "":
		filepath = origin.src_uri

	filepath_no_ext, ext = splitext(filepath)
	if ext == "":
		ext = ".md"

	filepath_upper = (filepath_no_ext + ext).upper()
	_, filename_upper = split(filepath_upper)

	for f in available_files:
		f_filename_upper = split(f.src_uri)[1].upper()

		if f_filename_upper == filename_upper and f.src_uri.upper().endswith(filepath_upper):
			return f

	return None

def parse_fragment(fragment: str | None) -> str:
	if fragment is None or fragment == "":
		return ""

	parsed = unicodedata.normalize('NFD', fragment) \
		.encode('ascii', 'ignore') \
		.decode('utf-8') \
		.lower() \
		.replace('(', '') \
		.replace(')', '') \
		.replace('+', '') \
		.replace(' - ', '-') \
		.replace(' ', '-') \
		.replace('--', '-') \
		.strip( "-" )

	if not parsed.startswith("#"):
		parsed = "#" + parsed

	return parsed
