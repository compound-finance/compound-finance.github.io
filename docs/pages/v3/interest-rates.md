---
layout: docs-content
title: Compound III Docs | Interest Rates
permalink: /interest-rates/
docs_namespace: v3

## Element ID: In-page Heading
sidebar_nav_data:
  interest-rates: Interest Rates
  get-supply-rate: Get Supply Rate
  get-borrow-rate: Get Borrow Rate
  get-utilization: Get Utilization
---

# Interest Rates

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
