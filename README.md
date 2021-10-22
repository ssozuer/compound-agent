# cToken Exchange Rate Goes Down

## Description

This agent detects `Compound` **cToken** exchange rate drops.

## Supported Chains

- Ethereum
- List any other chains this agent can support e.g. BSC

## Alerts

Describe each of the type of alerts fired by this agent

- FORTA-6
  - Fired when a cToken exchange drop is found
  - It calculates drop according to the previous block and current block exchange rate values
  - Type is always set to "suspicious"
  - Mention any other type of metadata fields included with this alert
    - `blockNumber`: The current block number
    - `cToken`: The cToken name
    - `cTokenAddress`: The cToken address
    - `prevExchangeRate`: The previous exchange rate of the `cToken`
    - `currentExchangeRate`: The current exchange rate of the `cToken`
    - `diff`: The difference between previous and current exchange rates
    - `dropPercentage`: The drop percentage
