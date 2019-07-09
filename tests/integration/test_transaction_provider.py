from pretix_eth.providers import EthplorerTransactionProvider

from eth_utils import is_checksum_address, is_bytes, is_integer


ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'


def test_ethplorer_transaction_provider():
    provider = EthplorerTransactionProvider()
    transactions = provider.get_transactions(ZERO_ADDRESS)
    assert len(transactions) > 0
    assert all(
        is_bytes(tx.hash) and len(tx.hash) == 32
        for tx in transactions
    )
    assert all(
        is_checksum_address(tx.sender)
        for tx in transactions
    )
    assert all(tuple(
        is_integer(tx.value)
        for tx in transactions
    ))
    assert all(
        is_integer(tx.timestamp)
        for tx in transactions
    )
