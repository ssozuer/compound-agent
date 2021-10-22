from forta_agent import Finding, FindingType, FindingSeverity, get_json_rpc_url
from web3 import Web3
import json
import sys

MIN_NUMBER = -sys.maxsize - 1

# CompoundLens abi
with open("src/abi/ICompoundLens.json") as f:
    COMPOUND_LENS_ABI = json.load(f)

CTOKENS = {
    "cAAVE":  "0xe65cdb6479bac1e22340e4e755fae7e509ecd06c",
    "cBAT":   "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e", 
    "cCOMP":  "0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4", 
    "cDAI":   "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643",
    "cETH":   "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5",
    "cLINK":  "0xface851a4921ce59e912d19329929ce6da6eb0c7",
    "cMKR":   "0x95b4ef2869ebd94beb4eee400a99824bf5dc325b",
    "cREP":   "0x158079ee67fce2f58472a96584a73c7ab9ac95c1",
    "cSUSHI": "0x4b0181102a0112a2ef11abee5563bb4a3176c9d7",
    "cTUSD":  "0x12392f67bdf24fae0af363c24ac620a2f67dad86",
    "cUNI":   "0x35a18000230da775cac24873d00ff85bccded550",
    "cUSDC":  "0x39aa39c021dfbae8fac545936693ac917d5e7563",
    "cUSDT":  "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9",
    "cWBTC":  "0xc11b1268c1a384e55c48c2391d8d480264a3a7f4",
    "cYFI":   "0x80a2ae356fc9ef4305676f7a3e2ed04e12c33946",
    "cZRX":   "0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407",
}


# CompoundLends address
COMPOUND_LENS_ADDRESS = "0xA1Bd4a10185F30932C78185f86641f11902E873F"
w3 = Web3(Web3.HTTPProvider(get_json_rpc_url()))
compoundLens = w3.eth.contract(address=Web3.toChecksumAddress(COMPOUND_LENS_ADDRESS), abi=COMPOUND_LENS_ABI)

def provide_handle_block():
    def handle_block(block_event):
        findings = []

        for key, value in CTOKENS.items():
            exchangeRatePrevious = get_exchange_rate(key, int(block_event.block_number)-1)
            exchangeRateCurrent = get_exchange_rate(key, int(block_event.block_number))
            finding = process_finding(key, value, int(block_event.block_number), exchangeRateCurrent, exchangeRatePrevious)
            if finding is not None:
                findings.append(finding)
           
        return findings
    return handle_block

def process_finding(cToken, cTokenAddress, blockNumber, currentExchangeRate, prevExchangeRate):
    dropPercentage = float(round(1 - currentExchangeRate / prevExchangeRate, 4) * 100)
    if currentExchangeRate < prevExchangeRate:
        return Finding({
            'name': "cToken Exchange Rate Goes Down",
            'description': f'The exchange rate for {cToken} goes down from {prevExchangeRate} to {currentExchangeRate}',
            'alert_id': "FORTA-6",
            'severity': get_severity(dropPercentage),
            'type': FindingType.Suspicious,
            'metadata': {
                'blockNumber': blockNumber,
                'cToken': cToken,
                'cTokenAddress': cTokenAddress,
                'prevExchangeRate': prevExchangeRate,
                'currentExchangeRate': currentExchangeRate,
                'diff': (prevExchangeRate - currentExchangeRate),
                'dropPercentage': dropPercentage 
            }
        })
    return None

def get_exchange_rate(cToken, block_number):
    metadata = compoundLens.functions.cTokenMetadata(Web3.toChecksumAddress(cToken)).call(block_identifier=block_number)
    exchangeRate = int(metadata[1])
    return exchangeRate

def get_severity(dropPercentage):
    if dropPercentage >= 5 and dropPercentage < 15:
        return FindingSeverity.Medium
    elif dropPercentage >= 15 and dropPercentage < 30:
        return FindingSeverity.High
    elif dropPercentage >= 30:
        return FindingSeverity.Critical
    else:
        return FindingSeverity.Info

real_handle_block = provide_handle_block()

def handle_block(block_event):
    return real_handle_block(block_event)
