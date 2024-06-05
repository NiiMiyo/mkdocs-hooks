import regex
from mkdocs.structure.pages import Page


COMMENT_PATTERN = regex.compile(r"%%[^%]%%")

def on_page_markdown(markdown: str, *, page: Page, **_):
	remove_text: list[tuple[int, int]] = []

	start = 0
	inside_comment = False

	while True:
		found_at = markdown.find("%%", start)

		if found_at == -1:
			if inside_comment:
				remove_text.append((start - 1, len(markdown) - 1))
			break

		inside_comment = not inside_comment

		if not inside_comment:
			remove_text.append((start - 1, found_at + 1))

		start = found_at + 1

	return "".join(
		l
		for i, l in enumerate(markdown)
		if not any( s <= i <= end for s, end in remove_text)
	)
