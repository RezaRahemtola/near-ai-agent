import os

from dotenv import load_dotenv


class _Config:
    near_rpc_url: str
    near_account_id: str
    near_account_private_key: str

    def __init__(self):
        load_dotenv()

        self.near_rpc_url = os.getenv("NEAR_RPC_URL")
        self.near_account_id = os.getenv("NEAR_ACCOUNT_ID")
        self.near_account_private_key = os.getenv("NEAR_ACCOUNT_PRIVATE_KEY")


env = _Config()
