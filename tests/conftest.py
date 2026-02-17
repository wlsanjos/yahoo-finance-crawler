import pytest
from src.parser import YahooFinanceParser
from src.storage import DataStorage

@pytest.fixture
def mock_html_content():
    return """
    <html>
        <body>
            <table>
                <tbody>
                    <tr>
                        <td><input type="checkbox"></td>
                        <td>AAPL</td>
                        <td>Apple Inc.</td>
                        <td><span class="graph"></span></td>
                        <td>150.00</td>
                    </tr>
                    <tr>
                        <td><input type="checkbox"></td>
                        <td>GOOGL</td>
                        <td>Alphabet Inc.</td>
                        <td><span class="graph"></span></td>
                        <td>2,800.00</td>
                    </tr>
                    <tr>
                        <td><input type="checkbox"></td>
                        <td>INVALID</td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """

@pytest.fixture
def parser(mock_html_content):
    return YahooFinanceParser(mock_html_content)

@pytest.fixture
def storage():
    return DataStorage()
