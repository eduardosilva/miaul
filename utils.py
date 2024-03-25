import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension

def convert_to_html(markdown_content):
    """
    Converts Markdown content to HTML with syntax highlighting for code blocks.

    Args:
        markdown_content (str): The Markdown content to convert.

    Returns:
        str: The HTML content with syntax highlighting.
    """
    # Define Markdown extensions for syntax highlighting
    extensions = [
        CodeHiliteExtension(noclasses=True, pygments_style="colorful"),  # Syntax highlighting for code blocks
        FencedCodeExtension(),  # Ensure code blocks are wrapped in <pre><code>
    ]

    # Convert Markdown content to HTML
    result = markdown.markdown(markdown_content, extensions=extensions)

    return result

