---
layout: docs-content
title: Compound v2 Docs | Comptroller
permalink: /v2/comptroller/
docs_namespace: v2

## Element ID: In-page Heading
sidebar_nav_data:
  comptroller: Comptroller
  architecture: Architecture
  enter-markets: Enter Markets
  exit-market: Exit Market
  get-assets-in: Get Assets In
  collateral-factor: Collateral Factor
  account-liquidity: Get Account Liquidity
  close-factor: Close Factor
  liquidation-incentive: Liquidation Incentive
  key-events: Key Events
  error-codes: Error Codes
  comp-distribution-speeds: COMP Distribution Speeds
  claim-comp: Claim COMP
  market-metadata: Market Metadata
---

# Comptroller

## Introduction

The Comptroller is the risk management layer of the Compound protocol; it determines how much collateral a user is required to maintain, and whether (and by how much) a user can be liquidated. Each time a user interacts with a cToken, the Comptroller is asked to approve or deny the transaction.

The Comptroller maps user balances to prices (via the Price Oracle) to
risk weights (called [Collateral Factors](/v2/comptroller#collateral-factor)) to make its determinations. Users explicitly list which assets they would like included in their risk scoring, by calling [Enter Markets](/v2/comptroller#enter-markets) and [Exit Market](/v2/comptroller#exit-market).

## Architecture

The Comptroller is implemented as an upgradeable proxy. The Unitroller proxies all logic to the Comptroller implementation, but storage values are set on the Unitroller. To call Comptroller functions, use the Comptroller ABI on the Unitroller address.

## Enter Markets

Enter into a list of markets - it is not an error to enter the same market more than once. In order to supply collateral or borrow in a market, it must be entered first.

#### Comptroller

```solidity
function enterMarkets(address[] calldata cTokens) returns (uint[] memory)
```

* `msg.sender`: The account which shall enter the given markets.
* `cTokens`: The addresses of the cToken markets to enter.
* `RETURN`: For each market, returns an error code indicating whether or not it was entered. Each is 0 on success, otherwise an [Error code](/v2/comptroller#error-codes).

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
CToken[] memory cTokens = new CToken[](2);
cTokens[0] = CErc20(0x3FDA...);
cTokens[1] = CEther(0x3FDB...);
uint[] memory errors = troll.enterMarkets(cTokens);
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const cTokens = [CErc20.at(0x3FDA...), CEther.at(0x3FDB...)];
const errors = await troll.methods.enterMarkets(cTokens).send({from: ...});
```

## Exit Market

Exit a market - it is not an error to exit a market which is not currently entered. Exited markets will not count towards account liquidity calculations.

#### Comptroller

```solidity
function exitMarket(address cToken) returns (uint)
```

* `msg.sender`: The account which shall exit the given market.
* `cTokens`: The addresses of the cToken market to exit.
* `RETURN`: 0 on success, otherwise an [Error code](/v2/comptroller#error-codes).

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
uint error = troll.exitMarket(CToken(0x3FDA...));
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const errors = await troll.methods.exitMarket(CEther.at(0x3FDB...)).send({from: ...});
```

## Get Assets In

Get the list of markets an account is currently entered into. In order to supply collateral or borrow in a market, it must be entered first. Entered markets count towards [account liquidity](/v2/comptroller#account-liquidity) calculations.

#### Comptroller

```solidity
function getAssetsIn(address account) view returns (address[] memory)

```

* `account`: The account whose list of entered markets shall be queried.
* `RETURN`: The address of each market which is currently entered into.

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
address[] memory markets = troll.getAssetsIn(0xMyAccount);
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const markets = await troll.methods.getAssetsIn(cTokens).call();
```

## Collateral Factor

A cToken's collateral factor can range from 0-90%, and represents the proportionate increase in liquidity (borrow limit) that an account receives by minting the cToken.
Generally, large or liquid assets have high collateral factors, while small or illiquid assets have low collateral factors. If an asset has a 0% collateral factor, it can't be used as collateral (or seized in liquidation), though it can still be borrowed.

<div class="notice">
Collateral factors can be increased (or decreased) through Compound Governance, as market conditions change.
</div>

#### Comptroller

```solidity
function markets(address cTokenAddress) view returns (bool, uint, bool)
```

* `cTokenAddress`: The address of the cToken to check if listed and get the collateral factor for.
* `RETURN`: Tuple of values (isListed, collateralFactorMantissa, isComped); isListed represents whether the comptroller recognizes this cToken; collateralFactorMantissa, scaled by 1e18, is multiplied by a supply balance to determine how much value can be borrowed. The isComped boolean indicates whether or not suppliers and borrowers are distributed COMP tokens.

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
(bool isListed, uint collateralFactorMantissa, bool isComped) = troll.markets(0x3FDA...);
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const result = await troll.methods.markets(0x3FDA...).call();
const {0: isListed, 1: collateralFactorMantissa, 2: isComped} = result;
```

## Get Account Liquidity
{:id="account-liquidity"}

Account Liquidity represents the USD value borrowable by a user, before it reaches liquidation. Users with a shortfall (negative liquidity) are subject to liquidation, and can’t withdraw or borrow assets until Account Liquidity is positive again.

For each market the user has [entered](/v2/comptroller#enter-markets) into, their supplied balance is multiplied by the market’s [collateral factor](/v2/comptroller#collateral-factor), and summed; borrow balances are then subtracted, to equal Account Liquidity. Borrowing an asset reduces Account Liquidity for each USD borrowed; withdrawing an asset reduces Account Liquidity by the asset’s collateral factor times each USD withdrawn.

Because the Compound Protocol exclusively uses unsigned integers, Account Liquidity returns either a surplus or shortfall.

#### Comptroller

```solidity
function getAccountLiquidity(address account) view returns (uint, uint, uint)
```

* `account`: The account whose liquidity shall be calculated.
* `RETURN`: Tuple of values (error, liquidity, shortfall). The error shall be 0 on success, otherwise an [error code](/v2/comptroller#error-codes). A non-zero liquidity value indicates the account has available [account liquidity](/v2/comptroller#account-liquidity). A non-zero shortfall value indicates the account is currently below his/her collateral requirement and is subject to liquidation. At most one of liquidity or shortfall shall be non-zero.

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
(uint error, uint liquidity, uint shortfall) = troll.getAccountLiquidity(msg.caller);
require(error == 0, "join the Discord");
require(shortfall == 0, "account underwater");
require(liquidity > 0, "account has excess collateral");
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const result = await troll.methods.getAccountLiquidity(0xBorrower).call();
const {0: error, 1: liquidity, 2: shortfall} = result;
```

## Close Factor

The percent, ranging from 0% to 100%, of a liquidatable account's borrow that can be repaid in a single liquidate transaction. If a user has multiple borrowed assets, the closeFactor applies to any single borrowed asset, not the aggregated value of a user’s outstanding borrowing.

#### Comptroller

```solidity
function closeFactorMantissa() view returns (uint)
```

* `RETURN`: The closeFactor, scaled by 1e18, is multiplied by an outstanding borrow balance to determine how much could be closed.

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
uint closeFactor = troll.closeFactorMantissa();
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const closeFactor = await troll.methods.closeFactorMantissa().call();
```

## Liquidation Incentive

The additional collateral given to liquidators as an incentive to perform liquidation of underwater accounts. A portion of this is given to the collateral cToken reserves as determined by the seize share. The seize share is assumed to be 0 if the cToken does not have a `protocolSeizeShareMantissa` constant. For example, if the liquidation incentive is 1.08, and the collateral's seize share is 1.028, liquidators receive an extra 5.2% of the borrower's collateral for every unit they close, and the remaining 2.8% is added to the cToken's reserves.

#### Comptroller

```solidity
function liquidationIncentiveMantissa() view returns (uint)
```

* `RETURN`: The liquidationIncentive, scaled by 1e18, is multiplied by the closed borrow amount from the liquidator to determine how much collateral can be seized.

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
uint closeFactor = troll.liquidationIncentiveMantissa();
```

#### Web3 1.0

```js
const troll = Comptroller.at(0xABCD...);
const closeFactor = await troll.methods.liquidationIncentiveMantissa().call();
```

## Key Events

| Event | Description |
|-------|-------------|
| `MarketEntered(CToken cToken, address account)` | Emitted upon a successful [Enter Market](/v2/comptroller#enter-markets). |
| `MarketExited(CToken cToken, address account)` | Emitted upon a successful [Exit Market](/v2/comptroller#exit-market). |
{: .key-events-table }

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| 0    | `NO_ERROR` | Not a failure. |
| 1    | `UNAUTHORIZED` | The sender is not authorized to perform this action. |
| 2    | `COMPTROLLER_MISMATCH` | Liquidation cannot be performed in markets with different comptrollers. |
| 3    | `INSUFFICIENT_SHORTFALL` | The account does not have sufficient shortfall to perform this action. |
| 4    | `INSUFFICIENT_LIQUIDITY` | The account does not have sufficient liquidity to perform this action. |
| 5    | `INVALID_CLOSE_FACTOR` | The close factor is not valid. |
| 6    | `INVALID_COLLATERAL_FACTOR` | The collateral factor is not valid. |
| 7    | `INVALID_LIQUIDATION_INCENTIVE` | The liquidation incentive is invalid. |
| 8    | `MARKET_NOT_ENTERED` | The market has not been entered by the account. |
| 9    | `MARKET_NOT_LISTED` | The market is not currently listed by the comptroller. |
| 10   | `MARKET_ALREADY_LISTED` | An admin tried to list the same market more than once. |
| 11   | `MATH_ERROR` | A math calculation error occurred. |
| 12   | `NONZERO_BORROW_BALANCE` | The action cannot be performed since the account carries a borrow balance. |
| 13   | `PRICE_ERROR` | The comptroller could not obtain a required price of an asset. |
| 14   | `REJECTION` | The comptroller rejects the action requested by the market. |
| 15   | `SNAPSHOT_ERROR` | The comptroller could not get the account borrows and exchange rate from the market. |
| 16   | `TOO_MANY_ASSETS` | Attempted to enter more markets than are currently supported. |
| 17   | `TOO_MUCH_REPAY` | Attempted to repay more than is allowed by the protocol. |
{: .error-codes-table }

## Failure Info

| Code | Name |
|------|------|
| 0    | `ACCEPT_ADMIN_PENDING_ADMIN_CHECK` |
| 1    | `ACCEPT_PENDING_IMPLEMENTATION_ADDRESS_CHECK` |
| 2    | `EXIT_MARKET_BALANCE_OWED` |
| 3    | `EXIT_MARKET_REJECTION` |
| 4    | `SET_CLOSE_FACTOR_OWNER_CHECK` |
| 5    | `SET_CLOSE_FACTOR_VALIDATION` |
| 6    | `SET_COLLATERAL_FACTOR_OWNER_CHECK` |
| 7    | `SET_COLLATERAL_FACTOR_NO_EXISTS` |
| 8    | `SET_COLLATERAL_FACTOR_VALIDATION` |
| 9    | `SET_COLLATERAL_FACTOR_WITHOUT_PRICE` |
| 10   | `SET_IMPLEMENTATION_OWNER_CHECK` |
| 11   | `SET_LIQUIDATION_INCENTIVE_OWNER_CHECK` |
| 12   | `SET_LIQUIDATION_INCENTIVE_VALIDATION` |
| 13   | `SET_MAX_ASSETS_OWNER_CHECK` |
| 14   | `SET_PENDING_ADMIN_OWNER_CHECK` |
| 15   | `SET_PENDING_IMPLEMENTATION_OWNER_CHECK` |
| 16   | `SET_PRICE_ORACLE_OWNER_CHECK` |
| 17   | `SUPPORT_MARKET_EXISTS` |
| 18   | `SUPPORT_MARKET_OWNER_CHECK` |

## COMP Distribution Speeds

### COMP Speed

The "COMP speed" unique to each market is an unsigned integer that specifies the amount of COMP that is distributed, per block, to suppliers and borrowers in each market. This number can be changed for individual markets by calling the `_setCompSpeed` method through a successful Compound Governance proposal.
The following is the formula for calculating the rate that COMP is distributed to each supported market.

```solidity
utility = cTokenTotalBorrows * assetPrice
utilityFraction = utility / sumOfAllCOMPedMarketUtilities
marketCompSpeed = compRate * utilityFraction
```

### COMP Distributed Per Block (All Markets)

The Comptroller contract’s `compRate` is an unsigned integer that indicates the rate at which the protocol distributes COMP to markets’ suppliers or borrowers, every Ethereum block. The value is the amount of COMP (in wei), per block, allocated for the markets. Note that not every market has COMP distributed to its participants (see Market Metadata).
The compRate indicates how much COMP goes to the suppliers or borrowers, so doubling this number shows how much COMP goes to all suppliers and borrowers combined. The code examples implement reading the amount of COMP distributed, per Ethereum block, to all markets.

#### Comptroller

```solidity
uint public compRate;
```

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
// COMP issued per block to suppliers OR borrowers * (1 * 10 ^ 18)
uint compRate = troll.compRate();
// Approximate COMP issued per day to suppliers OR borrowers * (1 * 10 ^ 18)
uint compRatePerDay = compRate * 4 * 60 * 24;
// Approximate COMP issued per day to suppliers AND borrowers * (1 * 10 ^ 18)
uint compRatePerDayTotal = compRatePerDay * 2;
```

#### Web3 1.2.6

```js
const comptroller = new web3.eth.Contract(comptrollerAbi, comptrollerAddress);
let compRate = await comptroller.methods.compRate().call();
compRate = compRate / 1e18;
// COMP issued to suppliers OR borrowers
const compRatePerDay = compRate * 4 * 60 * 24;
// COMP issued to suppliers AND borrowers
const compRatePerDayTotal = compRatePerDay * 2;
```

### COMP Distributed Per Block (Single Market)

The Comptroller contract has a mapping called `compSpeeds`. It maps cToken addresses to an integer of each market’s COMP distribution per Ethereum block. The integer indicates the rate at which the protocol distributes COMP to markets’ suppliers or borrowers. The value is the amount of COMP (in wei), per block, allocated for the market. Note that not every market has COMP distributed to its participants (see Market Metadata).
The speed indicates how much COMP goes to the suppliers or the borrowers, so doubling this number shows how much COMP goes to market suppliers and borrowers combined. The code examples implement reading the amount of COMP distributed, per Ethereum block, to a single market.

#### Comptroller

```solidity
mapping(address => uint) public compSpeeds;
```

#### Solidity

```solidity
Comptroller troll = Comptroller(0x123...);
address cToken = 0xabc...;
// COMP issued per block to suppliers OR borrowers * (1 * 10 ^ 18)
uint compSpeed = troll.compSpeeds(cToken);
// Approximate COMP issued per day to suppliers OR borrowers * (1 * 10 ^ 18)
uint compSpeedPerDay = compSpeed * 4 * 60 * 24;
// Approximate COMP issued per day to suppliers AND borrowers * (1 * 10 ^ 18)
uint compSpeedPerDayTotal = compSpeedPerDay * 2;
```

#### Web3 1.2.6

```js
const cTokenAddress = '0xabc...';
const comptroller = new web3.eth.Contract(comptrollerAbi, comptrollerAddress);
let compSpeed = await comptroller.methods.compSpeeds(cTokenAddress).call();
compSpeed = compSpeed / 1e18;
// COMP issued to suppliers OR borrowers
const compSpeedPerDay = compSpeed * 4 * 60 * 24;
// COMP issued to suppliers AND borrowers
const compSpeedPerDayTotal = compSpeedPerDay * 2;
```

## Claim COMP

Every Compound user accrues COMP for each block they are supplying to or borrowing from the protocol. Users may call the Comptroller's `claimComp` method at any time to transfer COMP accrued to their address.

#### Comptroller

```solidity
// Claim all the COMP accrued by holder in all markets
function claimComp(address holder) public
// Claim all the COMP accrued by holder in specific markets
function claimComp(address holder, CToken[] memory cTokens) public
// Claim all the COMP accrued by specific holders in specific markets for their supplies and/or borrows
function claimComp(address[] memory holders, CToken[] memory cTokens, bool borrowers, bool suppliers) public
```
#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
troll.claimComp(0x1234...);
```

#### Web3 1.2.6

```js
const comptroller = new web3.eth.Contract(comptrollerAbi, comptrollerAddress);
await comptroller.methods.claimComp("0x1234...").send({ from: sender });
```

## Market Metadata

The Comptroller contract has an array called `getAllMarkets` that contains the addresses of each cToken contract. Each address in the `getAllMarkets` array can be used to fetch a metadata struct in the Comptroller’s markets constant. See the [Comptroller Storage contract](https://github.com/compound-finance/compound-protocol/blob/master/contracts/ComptrollerStorage.sol){:target="_blank"} for the Market struct definition.

#### Comptroller

```solidity
CToken[] public getAllMarkets;
```

#### Solidity

```solidity
Comptroller troll = Comptroller(0xABCD...);
CToken cTokens[] = troll.getAllMarkets();
```

#### Web3 1.2.6

```js
const comptroller = new web3.eth.Contract(comptrollerAbi, comptrollerAddress);
const cTokens = await comptroller.methods.getAllMarkets().call();
const cToken = cTokens[0]; // address of a cToken
```
