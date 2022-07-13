---
layout: docs-content
title: Compound III
permalink: /

## Element ID: In-page Heading
sidebar_nav_data:
  compound-iii: Introduction
  interest-rates: Interest Rates
  get-supply-rate: Get Supply Rate
  get-borrow-rate: Get Borrow Rate
  get-utilization: Get Utilization
  reserves: Protocol Reserves
  target-reserves: Target Reserves
---

# Compound III

## Introduction

[Compound III](https://github.com/compound-finance/comet) is an EVM compatible protocol that enables supplying of crypto assets as collateral in order to borrow the *base asset*. Accounts can also earn interest by supplying the base asset to the protocol.

The initial deployment of Compound III is on Ethereum and the base asset is USDC.

The [app.compound.finance](https://app.compound.finance) interface is [open-source](https://github.com/compound-finance/palisade), deployed to IPFS, and is maintained by the community.

Please join the #development room in the Compound community [Discord](https://compound.finance/discord) server as well as the forums at [comp.xyz](https://comp.xyz); Compound Labs and members of the community look forward to helping you build an application on top of Compound III. Your questions help us improve, so please don't hesitate to ask if you can't find what you are looking for here.

For documentation of the Compound v2 Protocol, see [compound.finance/docs](https://compound.finance/docs).

## Interest Rates

Users with a positive balance of the base asset earn interest, denominated in the base asset, based on a supply rate model; users with a negative balance pay interest based on a borrow rate model. These are separate interest rate models, and set by governance.

The supply and borrow interest rates are a function of the utilization rate of the base asset. Each model includes a utilization rate "kink" - above this point the interest rate increases more rapidly. Interest accrues every second using the block timestamp.

Collateral assets do not earn or pay interest.

### Get Supply Rate

This function returns the per second supply rate as the decimal representation of a percentage scaled up by `10 ^ 18`. The formula for producing the supply rate is:

```
## If the Utilization is less than or equal to the Kink parameter

SupplyRate = (InterestRateBase + InterestRateSlopeLow * Utilization) * Utilization * (1 - ReserveRate)

## Else

SupplyRate = (InterestRateBase + InterestRateSlopeLow * Kink + InterestRateSlopeHigh * (Utilization - Kink)) * Utilization * (1 - ReserveRate)
```

To calculate the Compound III supply APR as a percentage, pass the current utilization to this function, and divide the result by `10 ^ 18` and multiply by the approximate number of seconds in one year and scale up by 100.

```
Seconds Per Year = 60 * 60 * 24 * 365
Utilization = getUtilization()
Supply Rate = getSupplyRate(Utilization)
Supply APR = Supply Rate / (10 ^ 18) * Seconds Per Year * 100
```

#### Comet

```solidity
function getSupplyRate(uint utilization) public view returns (uint64)
```

* `utilization`: The utilization at which to calculate the rate.
* `RETURNS`: The per second supply rate as the decimal representation of a percentage scaled up by `10 ^ 18`. E.g. `317100000` indicates, roughly, a 1% APR.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint supplyRate = comet.getSupplyRate(0.8e18);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const supplyRate = await comet.callStatic.getSupplyRate(0.8e18);
```

### Get Borrow Rate

This function returns the per second borrow rate as the decimal representation of a percentage scaled up by `10 ^ 18`. The formula for producing the borrow rate is:

```
## If the Utilization is less than or equal to the Kink parameter

BorrowRate = InterestRateBase + InterestRateSlopeLow * Utilization

## Else

BorrowRate = InterestRateBase + InterestRateSlopeLow * Kink + InterestRateSlopeHigh * (Utilization - Kink)
```

To calculate the Compound III borrow APR as a percentage, pass the current utilization to this function, and divide the result by `10 ^ 18` and multiply by the approximate number of seconds in one year and scale up by 100.

```
Seconds Per Year = 60 * 60 * 24 * 365
Utilization = getUtilization()
Borrow Rate = getBorrowRate(Utilization)
Borrow APR = Borrow Rate / (10 ^ 18) * Seconds Per Year * 100
```

#### Comet

```solidity
function getBorrowRate(uint utilization) public view returns (uint64)
```

* `utilization`: The utilization at which to calculate the rate.
* `RETURNS`: The per second borrow rate as the decimal representation of a percentage scaled up by `10 ^ 18`. E.g. `317100000` indicates, roughly, a 1% APR.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint borrowRate = comet.getBorrowRate(0.8e18);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const borrowRate = await comet.callStatic.getBorrowRate(0.8e18);
```

### Get Utilization

This function returns the current protocol utilization of the base asset. The formula for producing the utilization is:

`Utilization = TotalBorrows / TotalSupply`

#### Comet

```solidity
function getUtilization() public view returns (uint)
```

* `RETURNS`: The current protocol utilization percentage as a decimal, represented by an unsigned integer, scaled up by `10 ^ 18`. E.g. `1e17 or 100000000000000000` is 10% utilization.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint utilization = comet.getUtilization(); // example: 10000000000000000 (1%)
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const utilization = await comet.callStatic.getUtilization();
```

## Reserves

Reserves are a balance of the base asset, stored internally in the protocol, which automatically protect users from bad debt. Reserves can also be withdrawn or used through the governance process.

Reserves are generated in two ways: the difference in interest paid by borrowers, and earned by suppliers of the base asset, accrue as reserves into the protocol. Second, the [liquidation](./liquidation/) process uses, and can add to, protocol reserves based on the [target reserve](#target-reserves) level set by governance.

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

This immutable value represents the target amount of reserves of the base token. If the protocol holds greater than or equal to this amount of reserves, the *[buyCollateral](./liquidation/#buy-collateral)* function can no longer be successfully called.

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
