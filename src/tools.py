import requests
from py_near.account import Account
from py_near.dapps.core import NEAR
from py_near.providers import JsonProvider

from src.config import env


async def get_testnet_tokens(receiver: str) -> str:
    """
      Send some Near testnet tokens to a Near account.

      Args:
          receiver: The receiver of the tokens
      Returns:
          Message explaining what happened.
      """
    response = requests.post(
        "https://near-faucet.io/api/faucet/tokens",
        json={"contractId": "near_faucet", "receiverId": receiver, "amount": "10000000000000000000000000"}
    )
    data = response.json()

    error_message = data.get('error')
    if error_message is None:
        return f"Successfully sent 10 Near tokens with transaction hash {data.get('txh')}"
    else:
        return f"An error occurred: {error_message}"


async def mint_near_nft(receiver: str) -> str:
    """
    Create an NFT and send it to a Near account

    Args:
        receiver: The receiver of the NFT
    Returns:
        Message explaining what happened.
    """
    account = Account(env.near_account_id, env.near_account_private_key, env.near_rpc_url)
    await account.startup()

    existing_nfts = await account.view_function(env.near_account_id, "nft_tokens", {})

    result = await account.function_call(
        env.near_account_id,
        "nft_mint",
        {
            "token_id": str(len(existing_nfts.result)),  # Generating a new ID incrementally
            "receiver_id": receiver,
            "token_metadata": {
                "title": "AI minted NFT",
                "description": "Hello World from nearaibot.testnet!",
                "media": "https://ipfs.io/ipfs/QmQMZcwxrYF499EL1gvJ5Anw4UqAugoYv5XmQwmnoFS3eM",
                "copies": 1
            }
        },
        amount=int(0.1 * NEAR)
    )
    status = result.status
    if status.get('SuccessValue', None) is not None:
        return f"Successfully minted and sent NFT with transaction hash {result.transaction.hash}"
    elif status.get('Failure', None) is not None:
        return f"An error occurred: {status.get('Failure')}"
    else:
        return "An unknown error occurred"


async def get_near_transaction_info(tx_hash: str, sender_account: str):
    """
    Get information about a Near transaction

    Args:
        tx_hash: Hash of the transaction
        sender_account: Account that sent the transaction
    Returns:
        Transaction object
    """
    near_provider = JsonProvider(env.near_rpc_url)

    tx = await near_provider.json_rpc("EXPERIMENTAL_tx_status", [tx_hash, sender_account])
    return tx


TOOLS = [get_testnet_tokens, mint_near_nft, get_near_transaction_info]
