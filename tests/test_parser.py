from src.parser import YahooFinanceParser

def test_extract_equity_data_success(parser):
    results = parser.extract_equity_data()

    assert len(results) == 2

    assert results[0]["symbol"] == "AAPL"
    assert results[0]["name"] == "Apple Inc."
    assert results[0]["price"] == "150.00"

    assert results[1]["symbol"] == "GOOGL"
    assert results[1]["name"] == "Alphabet Inc."
    assert results[1]["price"] == "2,800.00"

def test_extract_equity_data_malformed_html():
    html = "<html><body><div>No Table Here</div></body></html>"
    parser = YahooFinanceParser(html)
    results = parser.extract_equity_data()
    assert results == []

def test_extract_equity_data_empty_table():
    html = "<html><body><table><tbody></tbody></table></body></html>"
    parser = YahooFinanceParser(html)
    results = parser.extract_equity_data()
    assert results == []
