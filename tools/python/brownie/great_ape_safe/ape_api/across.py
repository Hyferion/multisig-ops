import requests
from helpers.addresses import registry, r



class Across:
    def __init__(self, safe):
        self.safe = safe

        # See https://docs.across.to/v/developer-docs/developers/across-api#calculating-suggested-fees
        # Any chain's token address can be used
        self.api_url = "https://across.to/api/suggested-fees"
        self.spokepool = self.safe.contract(r.across.spoke_pool)


    def get_token_bridge_info(self, token_address, dest_chain_id, amount):
        # https://github.com/anyswap/CrossChain-Router/wiki/How-to-integrate-AnySwap-Router
        params = {"destinationChainId": dest_chain_id, "token": token_address, "amount": amount}
        r = requests.get(self.api_url, params=params).json()
        return r

    def bridge_token(self, recipient_address, origin_token, dest_chain_id, amount):
        info = self.get_token_bridge_info(origin_token.address, dest_chain_id, amount)
        timestamp = info["timestamp"]
        relayerFeePct = info["relayFeePct"]
        origin_token.approve(self.spokepool.address, amount)
        self.spokepool.deposit(recipient_address, origin_token.address, amount, dest_chain_id, relayerFeePct, timestamp)


