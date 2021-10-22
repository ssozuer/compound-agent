from forta_agent import FindingSeverity, FindingType, create_transaction_event
from agent import  COMPOUND_LENS_ADDRESS, COMPOUND_LENS_ABI, COMPOUND_LENS_ADDRESS, CTOKENS, get_severity, get_exchange_rate, w3, process_finding


class TestCompoundExchangeRateDownAgent:

    def test_valid_compoundlens_address(self):
        assert COMPOUND_LENS_ADDRESS == '0xA1Bd4a10185F30932C78185f86641f11902E873F'

    def test_can_get_compoundlens_abi(self):
        assert len(COMPOUND_LENS_ABI) > 0

    def test_returns_severity_info(self):
        assert FindingSeverity.Info == get_severity(1)

    def test_returns_severity_medium(self):
        assert FindingSeverity.Medium == get_severity(7)

    def test_returns_severity_high(self):
        assert FindingSeverity.High == get_severity(15)

    def test_returns_severity_critical(self):
        assert FindingSeverity.Critical == get_severity(30)

    def test_returns_exchange_rate_of_ctoken(self):
        cCOMP = "0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4"
        blockNumber = w3.eth.block_number
        assert get_exchange_rate(cCOMP, blockNumber) > 0

    def test_valid_ctoken_addresses(self):
        assert CTOKENS['cAAVE']  == "0xe65cdb6479bac1e22340e4e755fae7e509ecd06c"
        assert CTOKENS['cBAT']   == "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e"
        assert CTOKENS['cCOMP']  == "0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4"
        assert CTOKENS['cDAI']   == "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643"
        assert CTOKENS['cETH']   == "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5"
        assert CTOKENS['cLINK']  == "0xface851a4921ce59e912d19329929ce6da6eb0c7"
        assert CTOKENS['cMKR']   == "0x95b4ef2869ebd94beb4eee400a99824bf5dc325b"
        assert CTOKENS['cREP']   == "0x158079ee67fce2f58472a96584a73c7ab9ac95c1"
        assert CTOKENS['cSUSHI'] == "0x4b0181102a0112a2ef11abee5563bb4a3176c9d7"
        assert CTOKENS['cTUSD']  == "0x12392f67bdf24fae0af363c24ac620a2f67dad86"
        assert CTOKENS['cUNI']   == "0x35a18000230da775cac24873d00ff85bccded550"
        assert CTOKENS['cUSDC']  == "0x39aa39c021dfbae8fac545936693ac917d5e7563"
        assert CTOKENS['cUSDT']  == "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9"
        assert CTOKENS['cWBTC']  == "0xc11b1268c1a384e55c48c2391d8d480264a3a7f4"
        assert CTOKENS['cYFI']   == "0x80a2ae356fc9ef4305676f7a3e2ed04e12c33946"
        assert CTOKENS['cZRX']   == "0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407"

    def test_returns_finding_none(self):
        cToken = CTOKENS['cCOMP']
        blockNumber = w3.eth.block_number
        exchangeRatePrevious = get_exchange_rate(cToken, blockNumber)
        exchangeRateCurrent = get_exchange_rate(cToken,  blockNumber)
        finding =  process_finding('cCOMP', cToken, blockNumber, exchangeRateCurrent, exchangeRatePrevious)
        assert finding is None

    def test_returns_valid_finding(self):
        cToken = CTOKENS['cCOMP']
        blockNumber = w3.eth.block_number
        exchangeRatePrevious = 100
        exchangeRateCurrent = 80
        finding =  process_finding('cCOMP', cToken, blockNumber, exchangeRateCurrent, exchangeRatePrevious)
        assert finding is not None
        assert finding.name == 'cToken Exchange Rate Goes Down'
        assert finding.description == 'The exchange rate for cCOMP goes down from 100 to 80'
        assert finding.alert_id == 'FORTA-6'
        assert finding.severity == FindingSeverity.High
        assert finding.type == FindingType.Suspicious
        assert finding.metadata['blockNumber'] == blockNumber
        assert finding.metadata['cToken'] == 'cCOMP'
        assert finding.metadata['cTokenAddress'] == CTOKENS['cCOMP']
        assert finding.metadata['prevExchangeRate'] == 100
        assert finding.metadata['currentExchangeRate'] == 80
        assert finding.metadata['diff'] == 20
        assert finding.metadata['dropPercentage'] == 20
