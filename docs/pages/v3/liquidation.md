---
layout: docs-content
title: Compound III Docs | Liquidation
permalink: /v3/liquidation/
docs_version: v3

## Element ID: In-page Heading
sidebar_nav_data:
  liquidation: Liquidation
  liquidatable-accounts: Liquidatable Accounts
  absorb: Absorb
  buy-collateral: Buy Collateral
  ask-price: Ask Price
  liquidator-points: Liquidator Points
  reserves: Protocol Reserves
  target-reserves: Target Reserves
---

# Liquidation

Liquidation is determined by *[liquidation collateral factors](../helper-functions/#get-asset-info-by-address)*, which are separate and higher than borrow collateral factors (used to determine initial borrowing capacity), which protects borrowers & the protocol by ensuring a price buffer for all new positions. These also enable governance to reduce borrow collateral factors without triggering the liquidation of existing positions.

When an account's borrow balance exceeds the limits set by liquidation collateral factors, it is eligible for liquidation. A liquidator (a bot, contract, or user) can call the *[absorb](#absorb)* function, which relinquishes ownership of the accounts collateral, and returns the value of the collateral, minus a penalty (*[liquidationFactor](../helper-functions/#get-asset-info-by-address)*), to the user in the base asset. The liquidated user has no remaining debt, and typically, will have an excess (interest earning) balance of the base asset.

Each absorption is paid for by the protocol's reserves of the base asset. In return, the protocol receives the collateral assets. If the remaining reserves are less than a governance-set *[target](#target-reserves)*, liquidators are able to *[buy](#buy-collateral)* the collateral at a *[discount](#ask-price)* using the base asset, which increases the protocol's base asset reserves.

### Liquidatable Accounts

This function returns true if the account passed to it has negative liquidity based on the liquidation collateral factor. A return value of true indicates that the account is presently liquidatable.

#### Comet

```solidity
function isLiquidatable(address account) public view returns (bool)
```

* `account`: The account to examine liquidatability.
* `RETURNS`: Returns true if the account is presently able to be liquidated.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
bool isLiquidatable = comet.isLiquidatable(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const isLiquidatable = await comet.callStatic.isLiquidatable('0xAccount');
```

### Absorb

This function can be called by any address to liquidate an underwater account. It transfers the account's debt to the protocol account, decreases cash reserves to repay the account's borrows, and adds the collateral to the protocol's own balance. The caller has the amount of gas spent noted. In the future, they could be compensated via governance.

#### Comet

```solidity
function absorb(address absorber, address[] calldata accounts)
```

* `absorber`:  The account that is issued liquidator points during successful execution.
* `accounts`:  An array of underwater accounts that are to be liquidated.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.absorb(0xMyAddress, [ 0xUnderwaterAddress ]);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.absorb('0xMyAddress', [ '0xUnderwaterAddress' ]);
```

### Buy Collateral

This function allows any account to buy collateral from the protocol, at a discount from the Price Feed's price, using base tokens. A minimum collateral amount should be specified to indicate the maximum slippage acceptable for the buyer.

This function can be used after an account has been liquidated and there is collateral available to be purchased. Doing so increases protocol reserves. The amount of collateral available can be found by calling the *[Collateral Balance](../collateral-and-borrowing/#collateral-balance)* function. The price of the collateral can be determined by using the *[quoteCollateral](#ask-price)* function.

#### Comet

```solidity
function buyCollateral(address asset, uint minAmount, uint baseAmount, address recipient) external
```

* `asset`: The address of the collateral asset.
* `minAmount`: The minimum amount of collateral tokens that are to be received by the buyer, scaled up by 10 to the "decimals" integer in the collateral asset's contract.
* `baseAmount`: The amount of base tokens used to buy collateral scaled up by 10 to the "decimals" integer in the base asset's contract.
* `recipient`: The address that receives the purchased collateral.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.buyCollateral(0xAssetAddress, 5e18, 5e18, 0xRecipient);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.buyCollateral('0xAssetAddress', 5e18, 5e18, '0xRecipient');
```

### Ask Price

In order to repay the borrows of absorbed accounts, the protocol needs to sell the seized collateral. The *Ask Price* is the price of the asset to be sold at a discount (configured by governance). This function uses the price returned by the protocol's price feed. The discount of the asset is derived from the `StoreFrontPriceFactor` and the asset's `LiquidationFactor` using the following formula.

```
DiscountFactor = StoreFrontPriceFactor * (1e18 - Asset.LiquidationFactor)
```

#### Comet

```solidity
function quoteCollateral(address asset, uint baseAmount) public view returns (uint)
```

* `address`:  The address of the asset which is being queried.
* `amount`:  The amount of the asset to be sold.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint askPrice = comet.quoteCollateral(0xERC20Address, 10000000000);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const askPrice = await comet.callStatic.quoteCollateral('0xERC20Address', 1000000);
```

### Liquidator Points

The protocol keeps track of the successful executions of absorb by tallying liquidator "points" and gas the liquidator has spent.

#### Comet

```solidity
mapping(address => LiquidatorPoints) public liquidatorPoints;
```

* `address`:  The address of the liquidator account.
* `RETURN`: A struct containing the stored data pertaining to the liquidator account.
* `numAbsorbs`: A Solidity `uint32` of the number of times absorb was successfully called.
* `numAbsorbed`: A Solidity `uint64` of the number of accounts successfully absorbed by the protocol as a result of the liquidators call to the absorb function.
* `approxSpend`: A Solidity `uint128` of the sum of all gas spent by the liquidator that has called the absorb function.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
LiquidatorPoints pointsData = comet.liquidatorPoints(0xLiquidatorAddress);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const [ numAbsorbs, numAbsorbed, approxSpend ] = await comet.callStatic.liquidatorPoints('0xLiquidatorAddress');
```

## Reserves

Reserves are a balance of the base asset, stored internally in the protocol, which automatically protect users from bad debt. Reserves can also be withdrawn or used through the governance process.

Reserves are generated in two ways: the difference in interest paid by borrowers, and earned by suppliers of the base asset, accrue as reserves into the protocol. Second, the [liquidation](#liquidation) process uses, and can add to, protocol reserves based on the [target reserve](#target-reserves) level set by governance.

### Get Reserves

This function returns the amount of protocol reserves for the base asset as an integer.

#### Comet

```solidity
function getReserves() public view returns (int)
```

* `RETURNS`: The amount of base asset stored as reserves in the protocol as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint reserves = comet.getReserves();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const reserves = await comet.callStatic.getReserves();
```

### Target Reserves

This immutable value represents the target amount of reserves of the base token. If the protocol holds greater than or equal to this amount of reserves, the *[buyCollateral](#buy-collateral)* function can no longer be successfully called.

#### Comet

```solidity
function targetReserves() public view returns (uint)
```

* `RETURN`: The target reserve value of the base asset as an integer, scaled up by 10 to the "decimals" integer in the base asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint targetReserves = comet.targetReserves();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const targetReserves = await comet.callStatic.targetReserves();
```
