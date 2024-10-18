from pathlib import Path

from oterm.tools.rag.reader import FileReader


def test_docx_to_text(test_files: Path):

    text = FileReader().read(test_files / "sample.docx")
    assert text == "Hello world."


def test_pdf_to_text(test_files: Path):

    text = FileReader().read(test_files / "sample.pdf")
    print(text)
    assert text == " \n Hello world. "


def test_text_to_text(test_files: Path):

    text = FileReader().read(test_files / "sample.txt")
    assert text == "Hello world."


def test_html_to_text():

    html_text = """
    <html>
        <body>
            <h1>Test</h1>
            <p>Test paragraph</p>
            <ul>
                <li>item 1</li>
                <li>item 2</li>
            </ul>
            <a href="https://example.com">example</a>
            <table>
                <thead>
                    <tr>
                        <th>Header 1</th>
                        <th>Header 2</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Row 1, Column 1</td>
                        <td>Row 1, Column 2</td>
                    </tr>
                    <tr>
                        <td>Row 2, Column 1</td>
                        <td>Row 2, Column 2</td>
                    </tr>
                </tbody>
        </body>
    </html>"""

    text = FileReader.from_html(html_text)
    assert (
        text
        == "Test\nTest paragraph\nitem 1\nitem 2\nexample\nHeader 1\nHeader 2\nRow 1, Column 1\nRow 1, Column 2\nRow 2, Column 1\nRow 2, Column 2"
    )
