---
layout: docs-content
title: Compound II | Docs - Getting Started
permalink: /v2/
docs_version: v2

## Element ID: In-page Heading
sidebar_nav_data:
  getting-started: Getting Started
  guides: Guides
  networks: Networks
  protocol-math: Protocol Math

deployments:
  Ethereum Mainnet - Compound v2: ## this becomes the header text
    tab_text: Mainnet
    blockscan_origin: 'https://etherscan.io/'
    contracts:
      cAAVE: '0xe65cdB6479BaC1e22340E4E755fAE7E509EcD06c'
      cBAT: '0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E'
      cCOMP: '0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4'
      cDAI: '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643'
      cETH: '0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5'
      cFEI: '0x7713DD9Ca933848F6819F38B8352D9A15EA73F67'
      cLINK: '0xFAce851a4921ce59e912d19329929CE6da6EB0c7'
      cMKR: '0x95b4eF2869eBD94BEb4eEE400a99824BF5DC325b'
      cREP: '0x158079Ee67Fce2f58472A96584A73C7Ab9AC95c1'
      cSAI: '0xF5DCe57282A584D2746FaF1593d3121Fcac444dC'
      cSUSHI: '0x4B0181102A0112A2ef11AbEE5563bb4a3176c9d7'
      cTUSD: '0x12392F67bdf24faE0AF363c24aC620a2f67DAd86'
      cUNI: '0x35A18000230DA775CAc24873d00Ff85BccdeD550'
      cUSDC: '0x39AA39c021dfbaE8faC545936693aC917d5E7563'
      cUSDP: '0x041171993284df560249B57358F931D9eB7b925D'
      cUSDT: '0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9'
      cWBTC: '0xC11b1268C1A384e55C48c2391d8d480264A3A7F4'
      cWBTC2: '0xccF4429DB6322D5C611ee964527D42E5d685DD6a'
      cYFI: '0x80a2AE356fc9ef4305676f7a3E2Ed04e12C33946'
      cZRX: '0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407'
      COMP: '0xc00e94Cb662C3520282E6f5717214004A7f26888'
      Comptroller: '0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B'
      Governance: '0xc0Da02939E1441F497fd74F78cE7Decb17B66529'
      Timelock: '0x6d903f6003cca6255D85CcA4D3B5E5146dC33925'

  Ethereum Goerli Testnet - Compound v2:
    tab_text: Goerli
    blockscan_origin: 'https://goerli.etherscan.io/'
    contracts:
      cBAT: '0xCCaF265E7492c0d9b7C2f0018bf6382Ba7f0148D'
      cDAI: '0x822397d9a55d0fefd20F5c4bCaB33C5F65bd28Eb'
      cETH: '0x20572e4c090f15667cF7378e16FaD2eA0e2f3EfF'
      cREP: '0x1d70B01A2C3e3B2e56FcdcEfe50d5c5d70109a5D'
      cSAI: '0x5D4373F8C1AF21C391aD7eC755762D8dD3CCA809'
      cUSDC: '0xCEC4a43eBB02f9B80916F1c718338169d6d5C1F0'
      cWBTC: '0x6CE27497A64fFFb5517AA4aeE908b1E7EB63B9fF'
      cZRX: '0xA253295eC2157B8b69C44b2cb35360016DAa25b1'
      COMP: '0xe16C7165C8FeA64069802aE4c4c9C320783f2b6e'
      Comptroller: '0x627EA49279FD0dE89186A58b8758aD02B6Be2867'
      Timelock: '0x25e46957363e16C4e2D5F2854b062475F9f8d287'

  Ethereum Sepolia Testnet - Deployment Coming Soon:
    tab_text: Sepolia
    blockscan_origin: 'https://sepolia.etherscan.io/'
    contracts:
      Contract: '0x'
---

# Getting Started

## Introduction to Compound v2

<div class="new-docs-banner">
  <div class="center">
    <span class="message">Compound III is now live, you're currently viewing Compound v2 documentation.</span>
    <a href="/">
      <span class="button">Compound III Documentation</span>
    </a>
  </div>
</div>

The Compound protocol is based on the [Compound Whitepaper](https://compound.finance/documents/Compound.Whitepaper.pdf){:target="_blank"} (2019); the codebase is [open-source](https://github.com/compound-finance/compound-protocol){:target="_blank"}, and maintained by the community.

The app.compound.finance interface is [open-source](https://github.com/compound-finance/palisade){:target="_blank"}, and maintained by the community.

Please join the #development room in the Compound community [Discord](https://discord.com/invite/compound){:target="_blank"} server; Compound Labs and members of the community look forward to helping you build an application on top of Compound. Your questions help us improve, so please don't hesitate to ask if you can't find what you are looking for here.

## Guides

1. [Setting up an Ethereum Development Environment](https://medium.com/compound-finance/setting-up-an-ethereum-development-environment-7c387664c5fe){:target="_blank"}
2. [Supplying Assets to the Compound Protocol](https://medium.com/compound-finance/supplying-assets-to-the-compound-protocol-ec2cf5df5aa){:target="_blank"}
3. [Borrowing Assets from the Compound Protocol](https://medium.com/compound-finance/borrowing-assets-from-compound-quick-start-guide-f5e69af4b8f4){:target="_blank"}
4. [Create a Compound API with Infura](https://medium.com/compound-finance/compound-ethereum-api-with-infura-1f5c555fd4a2){:target="_blank"}
5. [Building a Governance Interface](https://medium.com/compound-finance/building-a-governance-interface-474fc271588c){:target="_blank"}
6. [Delegation & Voting](https://medium.com/compound-finance/delegation-and-voting-with-eip-712-signatures-a636c9dfec5e){:target="_blank"}
7. [Contributing to the Protocol](https://medium.com/compound-finance/a-walkthrough-of-contributing-to-the-compound-protocol-9450cbe2133a){:target="_blank"}
{: .mega-ordered-list }

## Networks

The Compound Protocol is currently deployed on the following networks:

<div id="networks-widget-container"></div>

You can also see a full list of all deployed contract addresses [here](https://github.com/compound-finance/compound-config){:target="_blank"}.

## Protocol Math

The Compound protocol contracts use a system of exponential math, [ExponentialNoError.sol](https://github.com/compound-finance/compound-protocol/blob/master/contracts/ExponentialNoError.sol){:target="_blank"}, in order to represent fractional quantities with sufficient precision.

Most numbers are represented as a *mantissa*, an unsigned integer scaled by `1 * 10 ^ 18`, in order to perform basic math at a high level of precision.

### cToken and Underlying Decimals

Prices and exchange rates are scaled by the decimals unique to each asset; cTokens are ERC-20 tokens with 8 decimals, while their underlying tokens vary, and have a public member named *decimals*.

| cToken | cToken Decimals | Underlying | Underlying Decimals |
| ------ | --------------- | ---------- | ------------------- |
| cETH   | 8               | ETH        | 18                  |
| cAAVE  | 8               | AAVE       | 18                  |
| cBAT   | 8               | BAT        | 18                  |
| cCOMP  | 8               | COMP       | 18                  |
| cDAI   | 8               | DAI        | 18                  |
| cFEI   | 8               | FEI        | 18                  |
| cLINK  | 8               | LINK       | 18                  |
| cMKR   | 8               | MKR        | 18                  |
| cSUSHI | 8               | SUSHI      | 18                  |
| cTUSD  | 8               | TUSD       | 18                  |
| cUNI   | 8               | UNI        | 18                  |
| cUSDC  | 8               | USDC       | 6                   |
| cUSDP  | 8               | USDP       | 18                  |
| cUSDT  | 8               | USDT       | 6                   |
| cWBTC  | 8               | WBTC       | 8                   |
| cYFI   | 8               | YFI        | 18                  |
| cZRX   | 8               | ZRX        | 18                  |
{: .decimals-events-table }

### Interpreting Exchange Rates

The cToken [Exchange Rate](/v2/ctokens#exchange-rate) is scaled by the difference in decimals between the cToken and the underlying asset.

```
oneCTokenInUnderlying = exchangeRateCurrent / (1 * 10 ^ (18 + underlyingDecimals - cTokenDecimals))
```

Here is an example of finding the value of 1 cBAT in BAT with Web3.js JavaScript.

```js
const cTokenDecimals = 8; // all cTokens have 8 decimal places
const underlying = new web3.eth.Contract(erc20Abi, batAddress);
const cToken = new web3.eth.Contract(cTokenAbi, cBatAddress);
const underlyingDecimals = await underlying.methods.decimals().call();
const exchangeRateCurrent = await cToken.methods.exchangeRateCurrent().call();
const mantissa = 18 + parseInt(underlyingDecimals) - cTokenDecimals;
const oneCTokenInUnderlying = exchangeRateCurrent / Math.pow(10, mantissa);
console.log('1 cBAT can be redeemed for', oneCTokenInUnderlying, 'BAT');
```

There is no underlying contract for ETH, so to do this with cETH, set `underlyingDecimals` to 18.

To find the number of underlying tokens that can be redeemed for cTokens, multiply the number of cTokens by the above value `oneCTokenInUnderlying`.

```
underlyingTokens = cTokenAmount * oneCTokenInUnderlying
```

### Calculating Accrued Interest

Interest rates for each market update on any block in which the ratio of borrowed assets to supplied assets in the market has changed. The amount interest rates are changed depends on the interest rate model smart contract implemented for the market, and the amount of change in the ratio of borrowed assets to supplied assets in the market.

See the interest rate data visualization notebook on [Observable](https://observablehq.com/@jflatow/compound-interest-rates){:target="_blank"} to visualize which interest rate model is currently applied to each market.

Historical interest rates can be retrieved from the [MarketHistoryService API](/v2/api#MarketHistoryService).

Interest accrues to all suppliers and borrowers in a market when any Ethereum address interacts with the market’s cToken contract, calling one of these functions: mint, redeem, borrow, or repay. Successful execution of one of these functions triggers the `accrueInterest` method, which causes interest to be added to the underlying balance of every supplier and borrower in the market. Interest accrues for the current block, as well as each prior block in which the `accrueInterest` method was not triggered (no user interacted with the cToken contract). Interest compounds only during blocks in which the cToken contract has one of the aforementioned methods invoked.

Here is an example of supply interest accrual:

Alice supplies 1 ETH to the Compound protocol. At the time of supply, the `supplyRatePerBlock` is 37893605 Wei, or 0.000000000037893605 ETH per block. No one interacts with the cEther contract for 3 Ethereum blocks. On the subsequent 4th block, Bob borrows some ETH. Alice’s underlying balance is now 1.000000000151574420 ETH (which is 37893605 Wei times 4 blocks, plus the original 1 ETH). Alice’s underlying ETH balance in subsequent blocks will have interest accrued based on the new value of 1.000000000151574420 ETH instead of the initial 1 ETH. Note that the `supplyRatePerBlock` value may change at any time.

### Calculating the APY Using Rate Per Block

The Annual Percentage Yield (APY) for supplying or borrowing in each market can be calculated using the value of `supplyRatePerBlock` (for supply APY) or `borrowRatePerBlock` (for borrow APY) in this formula:

```
Rate = cToken.supplyRatePerBlock(); // Integer
Rate = 37893566
ETH Mantissa = 1 * 10 ^ 18 (ETH has 18 decimal places)
Blocks Per Day = 6570 (13.15 seconds per block)
Days Per Year = 365

APY = ((((Rate / ETH Mantissa * Blocks Per Day + 1) ^ Days Per Year)) - 1) * 100
```

Here is an example of calculating the supply and borrow APY with Web3.js JavaScript:

```js
const ethMantissa = 1e18;
const blocksPerDay = 6570; // 13.15 seconds per block
const daysPerYear = 365;

const cToken = new web3.eth.Contract(cEthAbi, cEthAddress);
const supplyRatePerBlock = await cToken.methods.supplyRatePerBlock().call();
const borrowRatePerBlock = await cToken.methods.borrowRatePerBlock().call();
const supplyApy = (((Math.pow((supplyRatePerBlock / ethMantissa * blocksPerDay) + 1, daysPerYear))) - 1) * 100;
const borrowApy = (((Math.pow((borrowRatePerBlock / ethMantissa * blocksPerDay) + 1, daysPerYear))) - 1) * 100;
console.log(`Supply APY for ETH ${supplyApy} %`);
console.log(`Borrow APY for ETH ${borrowApy} %`);
```