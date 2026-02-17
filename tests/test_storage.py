import os
import csv
import pytest
from unittest.mock import patch, mock_open
from src.storage import DataStorage

def test_save_to_csv_success(storage):
    data = [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": "150.00"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "price": "2,800.00"}
    ]
    filename = "test_output.csv"

    m = mock_open()
    with patch("builtins.open", m):
        storage.save_to_csv(data, filename)

    m.assert_called_once_with(filename, mode='w', newline='', encoding='utf-8')

    handle = m()
    handle.write.assert_any_call("symbol,name,price\r\n")
    handle.write.assert_any_call("AAPL,Apple Inc.,150.00\r\n")
    handle.write.assert_any_call("GOOGL,Alphabet Inc.,\"2,800.00\"\r\n")

def test_save_to_csv_empty_data(storage, capsys):
    storage.save_to_csv([], "test.csv")
    captured = capsys.readouterr()
    assert "Nenhum dado para salvar." in captured.out

def test_save_to_csv_io_error(storage, capsys):
    data = [{"symbol": "A", "name": "B", "price": "1"}]

    with patch("builtins.open", side_effect=IOError("Permission denied")):
        storage.save_to_csv(data, "test.csv")

    captured = capsys.readouterr()
    assert "Erro ao salvar arquivo: Permission denied" in captured.out
