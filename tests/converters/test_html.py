import pytest

from oterm.tools.rag.converters.html import from_html


@pytest.mark.asyncio
async def test_html_to_text():

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

    text = from_html(html_text)
    assert (
        text
        == "Test\nTest paragraph\nitem 1\nitem 2\nexample\nHeader 1\nHeader 2\nRow 1, Column 1\nRow 1, Column 2\nRow 2, Column 1\nRow 2, Column 2"
    )
