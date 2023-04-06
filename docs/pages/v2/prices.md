---
layout: docs-content
title: Compound v2 Docs | Open Price Feed
permalink: /v2/prices/
docs_namespace: v2

## Element ID: In-page Heading
sidebar_nav_data:
  open-price-feed: Open Price Feed
  architecture: Architecture
  price: Get Price
  underlying-price: Get Underlying Price
  config: Get Config
  anchor-period: Get Anchor Period
  anchor-bounds: Get Anchor Bounds
---

# Open Price Feed

## Introduction

The Open Price Feed accounts price data for the Compound protocol. The protocol's Comptroller contract uses it as a source of truth for prices. Prices are updated by [Chainlink Price Feeds](https://data.chain.link/){:target="_blank"}. The codebase is hosted on [GitHub](https://github.com/compound-finance/open-oracle){:target="_blank"}, and maintained by the community.

The Compound Protocol uses a View contract ("Price Feed") which verifies that reported prices fall within an acceptable bound of the time-weighted average price of the token/ETH pair on [Uniswap v2](https://uniswap.org/), a sanity check referred to as the Anchor price.

The Chainlink price feeds submit prices for each cToken through an individual ValidatorProxy contract. Each ValidatorProxy is the only valid reporter for the underlying asset price. The contracts can be found on-chain as follows:

| Contract name | address |
|---------------|---------|
| AAVE ValidatorProxy  | [0x0238247E71AD0aB272203Af13bAEa72e99EE7c3c](https://etherscan.io/address/0x0238247E71AD0aB272203Af13bAEa72e99EE7c3c){:target="_blank"} |
| BAT ValidatorProxy   | [0xeBa6F33730B9751a8BA0b18d9C256093E82f6bC2](https://etherscan.io/address/0xeBa6F33730B9751a8BA0b18d9C256093E82f6bC2){:target="_blank"} |
| COMP ValidatorProxy  | [0xE270B8E9d7a7d2A7eE35a45E43d17D56b3e272b1](https://etherscan.io/address/0xE270B8E9d7a7d2A7eE35a45E43d17D56b3e272b1){:target="_blank"} |
| DAI ValidatorProxy   | [0xb2419f587f497CDd64437f1B367E2e80889631ea](https://etherscan.io/address/0xb2419f587f497CDd64437f1B367E2e80889631ea){:target="_blank"} |
| ETH ValidatorProxy   | [0x264BDDFD9D93D48d759FBDB0670bE1C6fDd50236](https://etherscan.io/address/0x264BDDFD9D93D48d759FBDB0670bE1C6fDd50236){:target="_blank"} |
| FEI ValidatorProxy   | [0xDe2Fa230d4C05ec0337D7b4fc10e16f5663044B0](https://etherscan.io/address/0xDe2Fa230d4C05ec0337D7b4fc10e16f5663044B0){:target="_blank"} |
| FRAX ValidatorProxy  | [0xfAD527D1c9F8677015a560cA80b7b56950a61FE1](https://etherscan.io/address/0xfAD527D1c9F8677015a560cA80b7b56950a61FE1){:target="_blank"} |
| LINK ValidatorProxy  | [0xBcFd9b1a97cCD0a3942f0408350cdc281cDCa1B1](https://etherscan.io/address/0xBcFd9b1a97cCD0a3942f0408350cdc281cDCa1B1){:target="_blank"} |
| LUSD ValidatorProxy  | [0xBfcbADAa807E25aF90424c8173645B945a401eca](https://etherscan.io/address/0xBfcbADAa807E25aF90424c8173645B945a401eca){:target="_blank"} |
| MATIC ValidatorProxy | [0x44750a79ae69D5E9bC1651E099DFFE1fb8611AbA](https://etherscan.io/address/0x44750a79ae69D5E9bC1651E099DFFE1fb8611AbA){:target="_blank"} |
| MKR ValidatorProxy   | [0xbA895504a8E286691E7dacFb47ae8A3A737e2Ce1](https://etherscan.io/address/0xbA895504a8E286691E7dacFb47ae8A3A737e2Ce1){:target="_blank"} |
| RAI ValidatorProxy   | [0xF0148Ddd8bA74D294E67E65FE1F3f0CD2F43CA8a](https://etherscan.io/address/0xF0148Ddd8bA74D294E67E65FE1F3f0CD2F43CA8a){:target="_blank"} |
| REP ValidatorProxy   | [0x90655316479383795416B615B61282C72D8382C1](https://etherscan.io/address/0x90655316479383795416B615B61282C72D8382C1){:target="_blank"} |
| SUSHI ValidatorProxy | [0x875acA7030B75b5D8cB59c913910a7405337dFf7](https://etherscan.io/address/0x875acA7030B75b5D8cB59c913910a7405337dFf7){:target="_blank"} |
| UNI ValidatorProxy   | [0x70f4D236FD678c9DB41a52d28f90E299676d9D90](https://etherscan.io/address/0x70f4D236FD678c9DB41a52d28f90E299676d9D90){:target="_blank"} |
| WBTC ValidatorProxy  | [0x4846efc15CC725456597044e6267ad0b3B51353E](https://etherscan.io/address/0x4846efc15CC725456597044e6267ad0b3B51353E){:target="_blank"} |
| YFI ValidatorProxy   | [0xBa4319741782151D2B1df4799d757892EFda4165](https://etherscan.io/address/0xBa4319741782151D2B1df4799d757892EFda4165){:target="_blank"} |
| ZRX ValidatorProxy   | [0x5c5db112c98dbe5977A4c37AD33F8a4c9ebd5575](https://etherscan.io/address/0x5c5db112c98dbe5977A4c37AD33F8a4c9ebd5575){:target="_blank"} |
| UniswapAnchoredView  | [0x50ce56A3239671Ab62f185704Caedf626352741e](https://etherscan.io/address/0x50ce56A3239671Ab62f185704Caedf626352741e){:target="_blank"} |

## Architecture

The Open Price Feed consists of two main contracts.
* `ValidatorProxy` is a contract that calls `validate` on the `UniswapAnchoredView`. This queries Uniswap v2 to check if a new price is within the Uniswap v2 TWAP anchor. If valid, the `UniswapAnchoredView` is updated with the asset's price. If invalid, the price data is not stored.
* `UniswapAnchoredView` only stores prices that are within an acceptable bound of the Uniswap time-weighted average price and are signed by a reporter. Also contains logic that upscales the posted prices into the format that Compound's Comptroller expects.

This architecture allows multiple views to use the same underlying price data, but to verify the prices in their own way.
Stablecoins like USDC, USDT, and TUSD are fixed at $1. SAI is fixed at 0.005285 ETH.

As a precaution, the [Compound community multisig](https://etherscan.io/address/0xbbf3f1421d886e9b2c5d716b5192ac998af2012c){:target="_blank"} has the ability to engage a failover that will switch a market's primary oracle from the Chainlink Price Feeds to Uniswap v2. The multisig is able to change to a failover for single markets. The Uniswap V2 TWAP price is used as the failover. The community can enable or disable the failover using `activateFailover` or `deactivateFailover`.

## Price

Get the most recent price for a token in USD with 6 decimals of precision.
* `symbol`: Symbol as a string
* `RETURNS`: The price of the asset in USD as an unsigned integer scaled up by `10 ^ 6`.

#### UniswapAnchoredView

```solidity
function price(string memory symbol) external view returns (uint)
```

#### Solidity

```solidity
UniswapAnchoredView view = UniswapAnchoredView(0xABCD...);
uint price = view.price("ETH");
```

#### Web3 1.0

```js
const view = UniswapAnchoredView.at("0xABCD...");
//eg: returns 200e6
const price = await view.methods.price("ETH").call();
```

## Underlying Price

Get the most recent price for a token in USD with 6 decimals of precision.
* `cToken`: The address of the cToken contract of the underlying asset.
* `RETURNS`: The price of the asset in USD as an unsigned integer scaled up by `10 ^ (36 - underlying asset decimals)`. E.g. WBTC has 8 decimal places, so the return value is scaled up by `1e28`.

#### UniswapAnchoredView

```solidity
function getUnderlyingPrice(address cToken) external view returns (uint)
```

#### Solidity

```solidity
UniswapAnchoredView view = UniswapAnchoredView(0xABCD...);
uint price = view.getUnderlyingPrice(0x1230...);
```

#### Web3 1.0

```js
const view = UniswapAnchoredView.at("0xABCD...");
//eg: returns 400e6
const price = await view.methods.getUnderlyingPrice("0x1230...").call();
```

## Config

Each token the Open Price Feed supports needs corresponding configuration metadata. The configuration for each token is set in the constructor and is immutable.

The fields of the config are:

* `cToken`: The address of the underlying token's corresponding cToken. This field is null for tokens that are not supported as cTokens.
* `underlying`: Address of the token whose price is being reported.
* `symbolHash`: The `keccak256` of the byte-encoded string of the token's symbol.
* `baseUnit`: The number of decimals of precision that the underlying token has. Eg: USDC has 6 decimals.
* `PriceSource`: An enum describing the whether or not to special case the prices for this token. `FIXED_ETH` is used to set the SAI price to a fixed amount of ETH, and `FIXED_USD` is used to peg stablecoin prices to $1. `REPORTER` is used for all other assets to indicate the reported prices and Uniswap anchoring should be used.
* `fixedPrice`: The fixed dollar amount to use if `PriceSource` is `FIXED_USD` or the number of ETH in the case of `FIXED_ETH` (namely for SAI).
* `uniswapMarket`: The token's market on Uniswap, used for price anchoring. Only filled if `PriceSource` is `REPORTER`.
* `isUniswapReversed`: A boolean indicating the order of the market's reserves.
* `reporter`: The address that submits prices for a particular cToken. This is always a `ValidatorProxy` contract that is always called by a price feed reference contract for each relevant price update posted by Chainlink oracle nodes.
* `reporterMultiplier`: An unsigned integer that is used to transform the price reported by the Chainlink price feeds to the correct base unit that the `UniswapAnchoredView` expects. This is required because the price feeds report prices with different decimal placement than the `UniswapAnchoredView`.

#### UniswapAnchoredView

```solidity
 function getTokenConfigBySymbol(string memory symbol) public view returns (TokenConfig memory)
 function getTokenConfigBySymbolHash(bytes32 symbolHash) public view returns (TokenConfig memory)
 function getTokenConfigByCToken(address cToken) public view returns (TokenConfig memory)
```

#### Web3 1.0

```js
const view = UniswapAnchoredView.at("0xABCD...");
const config = await view.methods.getTokenConfigBySymbol("ETH").call();
```

#### Solidity

```solidity
UniswapAnchoredView view = UniswapAnchoredView(0xABCD...);
uint price = view.getTokenConfigBySymbol("ETH");
```

## Anchor Period

Get the anchor period, the minimum amount of time in seconds over which to take the time-weighted average price from Uniswap.

####UniswapAnchoredView

```solidity
function anchorPeriod() returns (uint)
```

#### Web3 1.0

```js
const view = UniswapAnchoredView.at("0xABCD...");
const anchorPeriod = await view.methods.anchorPeriod().call();
```

#### Solidity

```solidity
UniswapAnchoredView view = UniswapAnchoredView(0xABCD...);
uint anchorPeriod = view.anchorPeriod();
```

## Anchor Bounds

Get the highest and lowest ratio of the reported price to the anchor price that will still trigger the price to be updated. Given in 18 decimals of precision (eg: 90% => 90e16).

####UniswapAnchoredView

```solidity
function upperBoundAnchorRatio() returns (uint)
function lowerBoundAnchorRatio() returns (uint)
```

#### Web3 1.0

```js
const view = UniswapAnchoredView.at("0xABCD...");
const upperBoundRatio = await view.methods.upperBoundAnchorRatio().call();
```

#### Solidity

```solidity
UniswapAnchoredView view = UniswapAnchoredView(0xABCD...);
uint upperBoundRatio = view.upperBoundAnchorRatio();
```
