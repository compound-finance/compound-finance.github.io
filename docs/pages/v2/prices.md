---
layout: docs-content
title: Compound v2 Docs | Price Feed
permalink: /v2/prices/
docs_namespace: v2

## Element ID: In-page Heading
sidebar_nav_data:
  introduction: Introduction
  architecture: Architecture
  underlying-price: Get Underlying Price
  config: Get Config
---

# Compound v2 Price Feed

## Introduction

The Compound v2 Price Feed accounts price data for the protocol. The protocol's Comptroller contract uses it as a source of truth for prices. Prices are updated by [Chainlink Price Feeds](https://data.chain.link/){:target="_blank"}. The codebase is hosted on [GitHub](https://github.com/smartcontractkit/open-oracle/blob/master/contracts/PriceOracle/PriceOracle.sol){:target="_blank"}, and maintained by the community.

The Compound v2 Price Feed fetches prices directly from Chainlink price feeds for valid cTokens when requested. Price feed addresses can be updated by the Compound multisig. The price feeds configured for each cToken can be found below:

| Contract name | address |
|---------------|---------|
| AAVE Price Feed  | [0x547a514d5e3769680ce22b2361c10ea13619e8a9](https://etherscan.io/address/0x547a514d5e3769680ce22b2361c10ea13619e8a9){:target="_blank"} |
| BAT Price Feed   | [0x9441D7556e7820B5ca42082cfa99487D56AcA958](https://etherscan.io/address/0x9441D7556e7820B5ca42082cfa99487D56AcA958){:target="_blank"} |
| COMP Price Feed  | [0xdbd020caef83efd542f4de03e3cf0c28a4428bd5](https://etherscan.io/address/0xdbd020caef83efd542f4de03e3cf0c28a4428bd5){:target="_blank"} |
| DAI Price Feed   | [0xaed0c38402a5d19df6e4c03f4e2dced6e29c1ee9](https://etherscan.io/address/0xaed0c38402a5d19df6e4c03f4e2dced6e29c1ee9){:target="_blank"} |
| ETH Price Feed   | [0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419](https://etherscan.io/address/0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419){:target="_blank"} |
| LINK Price Feed  | [0x2c1d072e956affc0d435cb7ac38ef18d24d9127c](https://etherscan.io/address/0x2c1d072e956affc0d435cb7ac38ef18d24d9127c){:target="_blank"} |
| MKR Price Feed   | [0xec1d1b3b0443256cc3860e24a46f108e699484aa](https://etherscan.io/address/0xec1d1b3b0443256cc3860e24a46f108e699484aa){:target="_blank"} |
| SUSHI Price Feed | [0xcc70f09a6cc17553b2e31954cd36e4a2d89501f7](https://etherscan.io/address/0xcc70f09a6cc17553b2e31954cd36e4a2d89501f7){:target="_blank"} |
| UNI Price Feed   | [0x553303d460ee0afb37edff9be42922d8ff63220e](https://etherscan.io/address/0x553303d460ee0afb37edff9be42922d8ff63220e){:target="_blank"} |
| WBTC Price Feed  | [0x45939657d1CA34A8FA39A924B71D28Fe8431e581](https://etherscan.io/address/0x45939657d1CA34A8FA39A924B71D28Fe8431e581){:target="_blank"} |
| YFI Price Feed   | [0xa027702dbb89fbd58938e4324ac03b58d812b0e1](https://etherscan.io/address/0xa027702dbb89fbd58938e4324ac03b58d812b0e1){:target="_blank"} |
| ZRX Price Feed   | [0x2885d15b8af22648b98b122b22fdf4d2a56c6023](https://etherscan.io/address/0x2885d15b8af22648b98b122b22fdf4d2a56c6023){:target="_blank"} |
| Price Feed       | [0x8CF42B08AD13761345531b839487aA4d113955d9](https://etherscan.io/address/0x8CF42B08AD13761345531b839487aA4d113955d9){:target="_blank"} |

The Compound v2 Price Feed also supports fixed prices for cTokens. This feature is required for cTokens that do not have a price feed. One such scenario is when a cToken is deprecated but the price at deprecation still needs to be reported. Below are cTokens using fixed prices:

| cToken | Fixed Price |
|--------|-------------|
| FEI | 1001094000000000000 |
| REP | 6433680000000000000 |
| SAI | 14426337000000000000 |

## Architecture

The Compound v2 Price Feed refers to a single contract.
* `PriceOracle` fetches prices from Chainlink Price Feeds when requested for a specific cToken. Also contains logic that upscales the fetched price into the format that Compound's Comptroller expects. The code is accessible on [GitHub](https://github.com/smartcontractkit/open-oracle/blob/master/contracts/PriceOracle/PriceOracle.sol){:target="_blank"}.

The [Compound community multisig](https://etherscan.io/address/0xbbf3f1421d886e9b2c5d716b5192ac998af2012c){:target="_blank"} has the ability to update the configs on the Price Feed. The multisig has the flexibility to make the following changes:

* **Add new markets**: The Price Feed contract's `addConfig` function enables the multisig to add a new cToken with an associated price feed or fixed price to support new markets.
* **Update price feed for markets**: The Price Feed contract's `updateConfigPriceFeed` function enables the multisig to update the price feed for an existing cToken. It can also be used to switch the configs from fixed price to a price feed.
* **Update fixed price for markets**: The Price Feed contract's `updateConfigFixedPrice` enables the multisig to update the fixed price for an existing cToken. It can also be used to switch the configs from a price feed to a fixed price such as in the case of deprecation.
* **Remove old markets**: The Price Feed contract's `removeConfig` function enables the multisig to remove configs for a deprecated market that the Comptroller no longer needs prices for.

## Underlying Price

Get the most recent price for a token in USD with the Chainlink price feed's decimals of precision.

* `cToken`: The address of the cToken contract of the underlying asset.
* `RETURNS`: The price of the asset in USD as an unsigned integer scaled up by `10 ^ (36 - underlying asset decimals)`. E.g. WBTC has 8 decimal places, so the return value is scaled up by `1e28`.

#### PriceFeed

```solidity
function getUnderlyingPrice(address cToken) external view returns (uint)
```

#### Solidity

```solidity
PriceFeed view = PriceFeed(0xABCD...);
uint price = view.getUnderlyingPrice(0x1230...);
```

#### Web3 1.0

```js
const view = PriceFeed.at("0xABCD...");
//eg: returns 400e6
const price = await view.methods.getUnderlyingPrice("0x1230...").call();
```

## Config

Each token the Compound v2 Price Feed supports needs corresponding configuration metadata. The configuration for each token is stored in the Price Feed contract and can be updated by the multisig.

The fields of the config are:

* `cToken`: The address of the underlying token's corresponding cToken. This is a required field.
* `underlyingAssetDecimals`: The decimals of the underlying asset. E.g. 18 for ETH. This field is required when using price feeds but optional when using fixed price.
* `priceFeed`: The address of the Chainlink price feed. This field is set to the 0 address when using a fixed price.
* `fixedPrice`: The fixed dollar amount to use as the price. This field is set to 0 if a price feed is being used.

#### PriceFeed

```solidity
function getConfig(address cToken) external view returns (TokenConfig memory)
```

#### Web3 1.0

```js
const view = PriceFeed.at("0xABCD...");
const config = await view.methods.getConfig("0x1230...").call();
```

#### Solidity

```solidity
PriceFeed view = PriceFeed(0xABCD...);
TokenConfig memory config = view.getConfig("0x1230...");
```
