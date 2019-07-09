from abc import ABC, abstractmethod
from typing import NamedTuple, Tuple, Iterable

import requests

from eth_typing import ChecksumAddress, Hash32

from eth_utils import (
    to_bytes,
    to_tuple,
    to_checksum_address,
)


class Transaction(NamedTuple):
    hash: Hash32
    sender: ChecksumAddress
    to: ChecksumAddress
    timestamp: int
    value: int


class TransactionProviderAPI(ABC):
    @abstractmethod
    def get_transactions(self, to_address: ChecksumAddress) -> Tuple[Transaction, ...]:
        ...


class BlockscoutTransactionProvider(TransactionProviderAPI):
    @to_tuple
    def get_transactions(self, from_address: ChecksumAddress) -> Iterable[Transaction]:
        response = requests.get(
            f'https://blockscout.com/poa/core/api?module=account&action=txlist&address={from_address}',  # noqa: E501
        )
        # TODO: handle http errors here
        response.raise_for_status()
        response_data = response.json()
        if response_data['status'] != "1":
            raise Exception("TODO: real exception and message")
        for raw_transaction in response_data['result']:
            if raw_transaction['txreceipt_status'] == '1':
                yield Transaction(
                    hash=to_bytes(hexstr=raw_transaction['hash']),
                    sender=to_checksum_address(raw_transaction['from']),
                    to=to_checksum_address(raw_transaction['to']),
                    timestamp=int(raw_transaction['timeStamp']),
                    value=int(raw_transaction['value']),
                )


class Transfer(NamedTuple):
    sender: ChecksumAddress
    timestamp: int
    value: int


class TokenProviderAPI(ABC):
    @abstractmethod
    def get_ERC20_transfers(self, to_address: ChecksumAddress) -> Tuple[Transfer, ...]:
        ...


class BlockscoutTokenProvider(TokenProviderAPI):
    def get_ERC20_transfers(self, to_address: ChecksumAddress) -> Tuple[Transfer, ...]:
        response = requests.get(
            f'https://blockscout.com/poa/dai/api?module=account&action=txlist&address={to_address}',  # noqa: E501
        )
        response.raise_for_status()
        transfer_data = response.json()
        for raw_transfer in transfer_data['result']:
            if raw_transfer['txreceipt_status'] == '1':
                yield Transfer(
                    sender=to_checksum_address(raw_transfer['from']),
                    timestamp=raw_transfer['timestamp'],
                    value=raw_transfer['value'],
                )
