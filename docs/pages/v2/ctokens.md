---
layout: docs-content
title: Compound II | Docs - cTokens
permalink: /v2/ctokens/
docs_version: v2

## Element ID: In-page Heading
sidebar_nav_data:
  ctokens: cTokens
  mint: Mint
  redeem: Redeem
  redeem-underlying: Redeem Underlying
  borrow: Borrow
  repay-borrow: Repay Borrow
  repay-borrow-behalf: Repay Borrow Behalf
  transfer: Transfer
  liquidate-borrow: Liquidate Borrow
  key-events: Key Events
  error-codes: Error Codes
  exchange-rate: Exchange Rate
  get-cash: Get Cash
  total-borrows: Total Borrows
  borrow-balance: Borrow Balance
  borrow-rate: Borrow Rate
  total-supply: Total Supply
  underlying-balance: Underlying Balance
  supply-rate: Supply Rate
  total-reserves: Total Reserves
  reserve-factor: Reserve Factor
---

# cTokens

## Introduction

Each asset supported by the Compound Protocol is integrated through a cToken contract, which is an [EIP-20](https://eips.ethereum.org/EIPS/eip-20){:target="_blank"} compliant representation of balances supplied to the protocol. By minting cTokens, users (1) earn interest through the cToken's exchange rate, which increases in value relative to the underlying asset, and (2) gain the ability to use cTokens as collateral.

cTokens are the primary means of interacting with the Compound Protocol; when a user mints, redeems, borrows, repays a borrow, liquidates a borrow, or transfers cTokens, she will do so using the cToken contract.

There are currently two types of cTokens: CErc20 and CEther. Though both types expose the EIP-20 interface, CErc20 wraps an underlying ERC-20 asset, while CEther simply wraps Ether itself. As such, the core functions which involve transferring an asset into the protocol have slightly different interfaces depending on the type, each of which is shown below.

<div class="ctoken-faq">
  {% include ctoken-faq.html %}
</div>

## Mint

The mint function transfers an asset into the protocol, which begins accumulating interest based on the current [Supply Rate](#supply-rate) for the asset. The user receives a quantity of cTokens equal to the underlying tokens supplied, divided by the current [Exchange Rate](#exchange-rate).

#### CErc20

```solidity
function mint(uint mintAmount) returns (uint)
```
* `msg.sender`: The account which shall supply the asset, and own the minted cTokens.
* `mintAmount`: The amount of the asset to be supplied, in units of the underlying asset.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)
Before supplying an asset, users must first [approve](https://eips.ethereum.org/EIPS/eip-20#approve){:target="_blank"} the cToken to access their token balance.

#### CEther

```solidity
function mint() payable
```
* `msg.value`: The amount of ether to be supplied, in wei.
* `msg.sender`: The account which shall supply the ether, and own the minted cTokens.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Erc20 underlying = Erc20(0xToken...);     // get a handle for the underlying asset contract
CErc20 cToken = CErc20(0x3FDA...);        // get a handle for the corresponding cToken contract
underlying.approve(address(cToken), 100); // approve the transfer
assert(cToken.mint(100) == 0);            // mint the cTokens and assert there is no error
```
#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
await cToken.methods.mint().send({from: myAccount, value: 50});
```

## Redeem

The redeem function converts a specified quantity of cTokens into the underlying asset, and returns them to the user. The amount of underlying tokens received is equal to the quantity of cTokens redeemed, multiplied by the current [Exchange Rate](#exchange-rate). The amount redeemed must be less than the user's [Account Liquidity](/v2/comptroller#account-liquidity) and the market's available liquidity.

#### CErc20 / CEther

```solidity
function redeem(uint redeemTokens) returns (uint)
```
* `msg.sender`: The account to which redeemed funds shall be transferred.
* `redeemTokens`: The number of cTokens to be redeemed.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)

#### Solidity

```solidity
CEther cToken = CEther(0x3FDB...);
require(cToken.redeem(7) == 0, "something went wrong");
```

#### Web3 1.0

```js
const cToken = CErc20.at(0x3FDA...);
cToken.methods.redeem(1).send({from: ...});
```

## Redeem Underlying

The redeem underlying function converts cTokens into a specified quantity of the underlying asset, and returns them to the user. The amount of cTokens redeemed is equal to the quantity of underlying tokens received, divided by the current [Exchange Rate](#exchange-rate). The amount redeemed must be less than the user's [Account Liquidity](/v2/comptroller#account-liquidity) and the market's available liquidity.

#### CErc20 / CEther

```solidity
function redeemUnderlying(uint redeemAmount) returns (uint)
```
* `msg.sender`: The account to which redeemed funds shall be transferred.
* `redeemAmount`: The amount of underlying to be redeemed.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)

#### Solidity

```solidity
CEther cToken = CEther(0x3FDB...);
require(cToken.redeemUnderlying(50) == 0, "something went wrong");
```

#### Web3 1.0

```js
const cToken = CErc20.at(0x3FDA...);
cToken.methods.redeemUnderlying(10).send({from: ...});
```

## Borrow

The borrow function transfers an asset from the protocol to the user, and creates a borrow balance which begins accumulating interest based on the [Borrow Rate](#borrow-rate) for the asset. The amount borrowed must be less than the user's [Account Liquidity](/v2/comptroller#account-liquidity) and the market's available liquidity. To borrow Ether, the borrower must be 'payable' (solidity).

#### CErc20 / CEther

```solidity
function borrow(uint borrowAmount) returns (uint)
```

* `msg.sender`: The account to which borrowed funds shall be transferred.
* `borrowAmount` : The amount of the underlying asset to be borrowed.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)

#### Solidity

```solidity
CErc20 cToken = CErc20(0x3FDA...);
require(cToken.borrow(100) == 0, "got collateral?");
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
await cToken.methods.borrow(50).send({from: 0xMyAccount});
```

## Repay Borrow

The repay function transfers an asset into the protocol, reducing the user's borrow balance.

#### CErc20

```solidity
function repayBorrow(uint repayAmount) returns (uint)
```

* `msg.sender`: The account which borrowed the asset, and shall repay the borrow.
* `repayAmount`: The amount of the underlying borrowed asset to be repaid. A value of -1 (i.e. `2^256` - 1) can be used to repay the full amount.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)
Before repaying an asset, users must first [approve](https://eips.ethereum.org/EIPS/eip-20#approve){:target="_blank"} the cToken to access their token balance.

#### CEther

```solidity
function repayBorrow() payable
```

* `msg.value`: The amount of ether to be repaid, in wei.
* `msg.sender`: The account which borrowed the asset, and shall repay the borrow.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
CEther cToken = CEther(0x3FDB...);
require(cToken.repayBorrow.value(100)() == 0, "transfer approved?");
```

#### Web3 1.0

```js
const cToken = CErc20.at(0x3FDA...);
cToken.methods.repayBorrow(10000).send({from: ...});
```

## Repay Borrow Behalf

The repay function transfers an asset into the protocol, reducing the target user's borrow balance.

#### CErc20

```solidity
function repayBorrowBehalf(address borrower, uint repayAmount) returns (uint)
```

* `msg.sender`: The account which shall repay the borrow.
* `borrower`: The account which borrowed the asset to be repaid.
* `repayAmount`: The amount of the underlying borrowed asset to be repaid. A value of -1 (i.e. `2^256` - 1) can be used to repay the full amount.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)
Before repaying an asset, users must first [approve](https://eips.ethereum.org/EIPS/eip-20#approve){:target="_blank"} the cToken to access their token balance.

#### CEther

```solidity
function repayBorrowBehalf(address borrower) payable
```
* `msg.value`: The amount of ether to be repaid, in wei.
* `msg.sender`: The account which shall repay the borrow.
* `borrower`: The account which borrowed the asset to be repaid.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
CEther cToken = CEther(0x3FDB...);
require(cToken.repayBorrowBehalf.value(100)(0xBorrower) == 0, "transfer approved?");
```

#### Web3 1.0

```js
const cToken = CErc20.at(0x3FDA...);
await cToken.methods.repayBorrowBehalf(0xBorrower, 10000).send({from: 0xPayer});
```

## Transfer

Transfer is an ERC-20 method that allows accounts to send tokens to other Ethereum addresses. A cToken transfer will fail if the account has [entered](/v2/comptroller#enter-markets) that cToken market and the transfer would have put the account into a state of negative [liquidity](/v2/comptroller#account-liquidity).

#### CErc20 / CEther

```solidity
function transfer(address recipient, uint256 amount) returns (bool)
```

* `recipient`: The transfer recipient address.
* `amount`: The amount of cTokens to transfer.
* `RETURN`: Returns a boolean value indicating whether or not the operation succeeded.

#### Solidity

```solidity
CEther cToken = CEther(0x3FDB...);
cToken.transfer(0xABCD..., 100000000000);
```

#### Web3 1.0

```js
const cToken = CErc20.at(0x3FDA...);
await cToken.methods.transfer(0xABCD..., 100000000000).send({from: 0xSender});
```

## Liquidate Borrow

A user who has negative [account liquidity](/v2/comptroller#account-liquidity) is subject to [liquidation](#liquidate-borrow) by other users of the protocol to return his/her account liquidity back to positive (i.e. above the collateral requirement). When a liquidation occurs, a liquidator may repay some or all of an outstanding borrow on behalf of a borrower and in return receive a discounted amount of collateral held by the borrower; this discount is defined as the liquidation incentive.
A liquidator may close up to a certain fixed percentage (i.e. close factor) of any individual outstanding borrow of the underwater account. Unlike in v1, liquidators must interact with each cToken contract in which they wish to repay a borrow and seize another asset as collateral. When collateral is seized, the liquidator is transferred cTokens, which they may redeem the same as if they had supplied the asset themselves. Users must approve each cToken contract before calling liquidate (i.e. on the borrowed asset which they are repaying), as they are transferring funds into the contract.

#### CErc20

```solidity
function liquidateBorrow(address borrower, uint amount, address collateral) returns (uint)
```

* `msg.sender`: The account which shall liquidate the borrower by repaying their debt and seizing their collateral.
* `borrower`: The account with negative [account liquidity](/v2/comptroller#account-liquidity) that shall be liquidated.
* `repayAmount`: The amount of the borrowed asset to be repaid and converted into collateral, specified in units of the underlying borrowed asset.
* `cTokenCollateral`: The address of the cToken currently held as collateral by a borrower, that the liquidator shall seize.
* `RETURN`: 0 on success, otherwise an [Error code](#error-codes)
Before supplying an asset, users must first [approve](https://eips.ethereum.org/EIPS/eip-20#approve){:target="_blank"} the cToken to access their token balance.

#### CEther

```solidity
function liquidateBorrow(address borrower, address cTokenCollateral) payable
```

* `msg.value`: The amount of ether to be repaid and converted into collateral, in wei.
* `msg.sender`: The account which shall liquidate the borrower by repaying their debt and seizing their collateral.
* `borrower`: The account with negative [account liquidity](/v2/comptroller#account-liquidity) that shall be liquidated.
* `cTokenCollateral`: The address of the cToken currently held as collateral by a borrower, that the liquidator shall seize.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
CEther cToken = CEther(0x3FDB...);
CErc20 cTokenCollateral = CErc20(0x3FDA...);
require(cToken.liquidateBorrow.value(100)(0xBorrower, cTokenCollateral) == 0, "borrower underwater??");
```

#### Web3 1.0

```js
const cToken = CErc20.at(0x3FDA...);
const cTokenCollateral = CEther.at(0x3FDB...);
await cToken.methods.liquidateBorrow(0xBorrower, 33, cTokenCollateral).send({from: 0xLiquidator});
```

## Key Events

| Event | Description |
|-------|-------------|
| `Mint(address minter, uint mintAmount, uint mintTokens)` | Emitted upon a successful [Mint](#mint). |
| `Redeem(address redeemer, uint redeemAmount, uint redeemTokens)` | Emitted upon a successful [Redeem](#redeem). |
| `Borrow(address borrower, uint borrowAmount, uint accountBorrows, uint totalBorrows)` | Emitted upon a successful [Borrow](#borrow). |
| `RepayBorrow(address payer, address borrower, uint repayAmount, uint accountBorrows, uint totalBorrows)` | Emitted upon a successful [Repay Borrow](#repay-borrow). |
| `LiquidateBorrow(address liquidator, address borrower, uint repayAmount, address cTokenCollateral, uint seizeTokens)` | Emitted upon a successful [Liquidate Borrow](#liquidate-borrow). |
{: .key-events-table }

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| 0    | `NO_ERROR` | Not a failure. |
| 1    | `UNAUTHORIZED` | The sender is not authorized to perform this action. |
| 2    | `BAD_INPUT` | An invalid argument was supplied by the caller. |
| 3    | `COMPTROLLER_REJECTION` | The action would violate the comptroller policy. |
| 4    | `COMPTROLLER_CALCULATION_ERROR` | An internal calculation has failed in the comptroller. |
| 5    | `INTEREST_RATE_MODEL_ERROR` | The interest rate model returned an invalid value. |
| 6    | `INVALID_ACCOUNT_PAIR` | The specified combination of accounts is invalid. |
| 7    | `INVALID_CLOSE_AMOUNT_REQUESTED` | The amount to liquidate is invalid. |
| 8    | `INVALID_COLLATERAL_FACTOR` | The collateral factor is invalid. |
| 9    | `MATH_ERROR` | A math calculation error occurred. |
| 10   | `MARKET_NOT_FRESH` | Interest has not been properly accrued. |
| 11   | `MARKET_NOT_LISTED` | The market is not currently listed by its comptroller. |
| 12   | `TOKEN_INSUFFICIENT_ALLOWANCE` | ERC-20 contract must *allow* Money Market contract to call `transferFrom`. The current allowance is either 0 or less than the requested supply, repayBorrow or liquidate amount. |
| 13   | `TOKEN_INSUFFICIENT_BALANCE` | Caller does not have sufficient balance in the ERC-20 contract to complete the desired action. |
| 14   | `TOKEN_INSUFFICIENT_CASH` | The market does not have a sufficient cash balance to complete the transaction. You may attempt this transaction again later. |
| 15   | `TOKEN_TRANSFER_IN_FAILED` | Failure in ERC-20 when transfering token into the market. |
| 16   | `TOKEN_TRANSFER_OUT_FAILED` | Failure in ERC-20 when transfering token out of the market. |
{: .error-codes-table }

## Failure Info

| Code | Name |
|------|------|
| 0    | `ACCEPT_ADMIN_PENDING_ADMIN_CHECK` |
| 1    | `ACCRUE_INTEREST_ACCUMULATED_INTEREST_CALCULATION_FAILED` |
| 2    | `ACCRUE_INTEREST_BORROW_RATE_CALCULATION_FAILED` |
| 3    | `ACCRUE_INTEREST_NEW_BORROW_INDEX_CALCULATION_FAILED` |
| 4    | `ACCRUE_INTEREST_NEW_TOTAL_BORROWS_CALCULATION_FAILED` |
| 5    | `ACCRUE_INTEREST_NEW_TOTAL_RESERVES_CALCULATION_FAILED` |
| 6    | `ACCRUE_INTEREST_SIMPLE_INTEREST_FACTOR_CALCULATION_FAILED` |
| 7    | `BORROW_ACCUMULATED_BALANCE_CALCULATION_FAILED` |
| 8    | `BORROW_ACCRUE_INTEREST_FAILED` |
| 9    | `BORROW_CASH_NOT_AVAILABLE` |
| 10   | `BORROW_FRESHNESS_CHECK` |
| 11   | `BORROW_NEW_TOTAL_BALANCE_CALCULATION_FAILED` |
| 12   | `BORROW_NEW_ACCOUNT_BORROW_BALANCE_CALCULATION_FAILED` |
| 13   | `BORROW_MARKET_NOT_LISTED` |
| 14   | `BORROW_COMPTROLLER_REJECTION` |
| 15   | `LIQUIDATE_ACCRUE_BORROW_INTEREST_FAILED` |
| 16   | `LIQUIDATE_ACCRUE_COLLATERAL_INTEREST_FAILED` |
| 17   | `LIQUIDATE_COLLATERAL_FRESHNESS_CHECK` |
| 18   | `LIQUIDATE_COMPTROLLER_REJECTION` |
| 19   | `LIQUIDATE_COMPTROLLER_CALCULATE_AMOUNT_SEIZE_FAILED` |
| 20   | `LIQUIDATE_CLOSE_AMOUNT_IS_UINT_MAX` |
| 21   | `LIQUIDATE_CLOSE_AMOUNT_IS_ZERO` |
| 22   | `LIQUIDATE_FRESHNESS_CHECK` |
| 23   | `LIQUIDATE_LIQUIDATOR_IS_BORROWER` |
| 24   | `LIQUIDATE_REPAY_BORROW_FRESH_FAILED` |
| 25   | `LIQUIDATE_SEIZE_BALANCE_INCREMENT_FAILED` |
| 26   | `LIQUIDATE_SEIZE_BALANCE_DECREMENT_FAILED` |
| 27   | `LIQUIDATE_SEIZE_COMPTROLLER_REJECTION` |
| 28   | `LIQUIDATE_SEIZE_LIQUIDATOR_IS_BORROWER` |
| 29   | `LIQUIDATE_SEIZE_TOO_MUCH` |
| 30   | `MINT_ACCRUE_INTEREST_FAILED` |
| 31   | `MINT_COMPTROLLER_REJECTION` |
| 32   | `MINT_EXCHANGE_CALCULATION_FAILED` |
| 33   | `MINT_EXCHANGE_RATE_READ_FAILED` |
| 34   | `MINT_FRESHNESS_CHECK` |
| 35   | `MINT_NEW_ACCOUNT_BALANCE_CALCULATION_FAILED` |
| 36   | `MINT_NEW_TOTAL_SUPPLY_CALCULATION_FAILED` |
| 37   | `MINT_TRANSFER_IN_FAILED` |
| 38   | `MINT_TRANSFER_IN_NOT_POSSIBLE` |
| 39   | `REDEEM_ACCRUE_INTEREST_FAILED` |
| 40   | `REDEEM_COMPTROLLER_REJECTION` |
| 41   | `REDEEM_EXCHANGE_TOKENS_CALCULATION_FAILED` |
| 42   | `REDEEM_EXCHANGE_AMOUNT_CALCULATION_FAILED` |
| 43   | `REDEEM_EXCHANGE_RATE_READ_FAILED` |
| 44   | `REDEEM_FRESHNESS_CHECK` |
| 45   | `REDEEM_NEW_ACCOUNT_BALANCE_CALCULATION_FAILED` |
| 46   | `REDEEM_NEW_TOTAL_SUPPLY_CALCULATION_FAILED` |
| 47   | `REDEEM_TRANSFER_OUT_NOT_POSSIBLE` |
| 48   | `REDUCE_RESERVES_ACCRUE_INTEREST_FAILED` |
| 49   | `REDUCE_RESERVES_ADMIN_CHECK` |
| 50   | `REDUCE_RESERVES_CASH_NOT_AVAILABLE` |
| 51   | `REDUCE_RESERVES_FRESH_CHECK` |
| 52   | `REDUCE_RESERVES_VALIDATION` |
| 53   | `REPAY_BEHALF_ACCRUE_INTEREST_FAILED` |
| 54   | `REPAY_BORROW_ACCRUE_INTEREST_FAILED` |
| 55   | `REPAY_BORROW_ACCUMULATED_BALANCE_CALCULATION_FAILED` |
| 56   | `REPAY_BORROW_COMPTROLLER_REJECTION` |
| 57   | `REPAY_BORROW_FRESHNESS_CHECK` |
| 58   | `REPAY_BORROW_NEW_ACCOUNT_BORROW_BALANCE_CALCULATION_FAILED` |
| 59   | `REPAY_BORROW_NEW_TOTAL_BALANCE_CALCULATION_FAILED` |
| 60   | `REPAY_BORROW_TRANSFER_IN_NOT_POSSIBLE` |
| 61   | `SET_COLLATERAL_FACTOR_OWNER_CHECK` |
| 62   | `SET_COLLATERAL_FACTOR_VALIDATION` |
| 63   | `SET_COMPTROLLER_OWNER_CHECK` |
| 64   | `SET_INTEREST_RATE_MODEL_ACCRUE_INTEREST_FAILED` |
| 65   | `SET_INTEREST_RATE_MODEL_FRESH_CHECK` |
| 66   | `SET_INTEREST_RATE_MODEL_OWNER_CHECK` |
| 67   | `SET_MAX_ASSETS_OWNER_CHECK` |
| 68   | `SET_ORACLE_MARKET_NOT_LISTED` |
| 69   | `SET_PENDING_ADMIN_OWNER_CHECK` |
| 70   | `SET_RESERVE_FACTOR_ACCRUE_INTEREST_FAILED` |
| 71   | `SET_RESERVE_FACTOR_ADMIN_CHECK` |
| 72   | `SET_RESERVE_FACTOR_FRESH_CHECK` |
| 73   | `SET_RESERVE_FACTOR_BOUNDS_CHECK` |
| 74   | `TRANSFER_COMPTROLLER_REJECTION` |
| 75   | `TRANSFER_NOT_ALLOWED` |
| 76   | `TRANSFER_NOT_ENOUGH` |
| 77   | `TRANSFER_TOO_MUCH` |

## Exchange Rate

Each cToken is convertible into an ever increasing quantity of the underlying asset, as interest accrues in the market. The exchange rate between a cToken and the underlying asset is equal to:

```solidity
exchangeRate = (getCash() + totalBorrows() - totalReserves()) / totalSupply()
```

#### CErc20 / CEther

```solidity
function exchangeRateCurrent() returns (uint)
```
* `RETURN`: The current exchange rate as an unsigned integer, scaled by 1 * 10^(18 - 8 + Underlying Token Decimals).

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint exchangeRateMantissa = cToken.exchangeRateCurrent();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const exchangeRate = (await cToken.methods.exchangeRateCurrent().call()) / 1e18;
```

Tip: note the use of `call` vs. `send` to invoke the function from off-chain without incurring gas costs.

## Get Cash

Cash is the amount of underlying balance owned by this cToken contract. One may query the total amount of cash currently available to this market.

#### CErc20 / CEther

```solidity
function getCash() returns (uint)
```

* `RETURN`: The quantity of underlying asset owned by the contract.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint cash = cToken.getCash();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const cash = (await cToken.methods.getCash().call());
```

## Total Borrows

Total Borrows is the amount of underlying currently loaned out by the market, and the amount upon which interest is accumulated to suppliers of the market.

#### CErc20 / CEther

```solidity
function totalBorrowsCurrent() returns (uint)
```

* `RETURN`: The total amount of borrowed underlying, with interest.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint borrows = cToken.totalBorrowsCurrent();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const borrows = (await cToken.methods.totalBorrowsCurrent().call());
```

## Borrow Balance

A user who borrows assets from the protocol is subject to accumulated interest based on the current [borrow rate](#borrow-rate). Interest is accumulated every block and integrations may use this function to obtain the current value of a user's borrow balance with interest.

#### CErc20 / CEther

```solidity
function borrowBalanceCurrent(address account) returns (uint)
```

* `account`: The account which borrowed the assets.
* `RETURN`: The user's current borrow balance (with interest) in units of the underlying asset.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint borrows = cToken.borrowBalanceCurrent(msg.caller);
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const borrows = await cToken.methods.borrowBalanceCurrent(account).call();
```

## Borrow Rate

At any point in time one may query the contract to get the current borrow rate per block.

#### CErc20 / CEther

```solidity
function borrowRatePerBlock() returns (uint)
```

* `RETURN`: The current borrow rate as an unsigned integer, scaled by 1e18.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint borrowRateMantissa = cToken.borrowRatePerBlock();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const borrowRate = (await cToken.methods.borrowRatePerBlock().call()) / 1e18;
```

## Total Supply

Total Supply is the number of tokens currently in circulation in this cToken market. It is part of the EIP-20 interface of the cToken contract.

#### CErc20 / CEther

```solidity
function totalSupply() returns (uint)
```

* `RETURN`: The total number of tokens in circulation for the market.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint tokens = cToken.totalSupply();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const tokens = (await cToken.methods.totalSupply().call());
```

## Underlying Balance

The user's underlying balance, representing their assets in the protocol, is equal to the user's cToken balance multiplied by the [Exchange Rate](#exchange-rate).

#### CErc20 / CEther

```solidity
function balanceOfUnderlying(address account) returns (uint)
```
* `account`: The account to get the underlying balance of.
* `RETURN`: The amount of underlying currently owned by the account.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint tokens = cToken.balanceOfUnderlying(msg.caller);
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const tokens = await cToken.methods.balanceOfUnderlying(account).call();
```

## Supply Rate
At any point in time one may query the contract to get the current supply rate per block. The supply rate is derived from the [borrow rate](#borrow-rate), [reserve factor](#reserve-factor) and the amount of [total borrows](#total-borrows).

#### CErc20 / CEther

```solidity
function supplyRatePerBlock() returns (uint)
```

* `RETURN`: The current supply rate as an unsigned integer, scaled by 1e18.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint supplyRateMantissa = cToken.supplyRatePerBlock();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const supplyRate = (await cToken.methods.supplyRatePerBlock().call()) / 1e18;
```

## Total Reserves

Reserves are an accounting entry in each cToken contract that represents a portion of historical interest set aside as [cash](#cash) which can be withdrawn or transferred through the protocol's governance. A small portion of borrower interest accrues into the protocol, determined by the [reserve factor](#reserve-factor).

#### CErc20 / CEther

```solidity
function totalReserves() returns (uint)
```

* `RETURN`: The total amount of reserves held in the market.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint reserves = cToken.totalReserves();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const reserves = (await cToken.methods.totalReserves().call());
```

## Reserve Factor

The reserve factor defines the portion of borrower interest that is converted into [reserves](#total-reserves).

#### CErc20 / CEther

```solidity
function reserveFactorMantissa() returns (uint)
```

* `RETURN`: The current reserve factor as an unsigned integer, scaled by 1e18.

#### Solidity

```solidity
CErc20 cToken = CToken(0x3FDA...);
uint reserveFactorMantissa = cToken.reserveFactorMantissa();
```

#### Web3 1.0

```js
const cToken = CEther.at(0x3FDB...);
const reserveFactor = (await cToken.methods.reserveFactorMantissa().call()) / 1e18;
```
