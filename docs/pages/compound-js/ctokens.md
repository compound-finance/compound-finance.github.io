---
layout: docs-content
title: Compound.js Docs | cTokens (v2)
permalink: /compound-js/ctokens/
docs_namespace: compound-js

## Element ID: In-page Heading
sidebar_nav_data:
  ctoken-methods: cToken Methods
  compound-v2-supply: Compound v2 Supply
  redeem: Redeem
  borrow: Borrow
  repay-borrow: Repay Borrow
---

# Compound.js

## cToken Methods

These methods facilitate interactions with the cToken smart contracts.

## Compound v2 Supply

Supplies the user's Ethereum asset to the Compound Protocol.

- `asset` (string) A string of the asset to supply.
- `amount` (number \| string \| BigNumber) A string, number, or BigNumber object of the amount of an asset to supply. Use the `mantissa` boolean in the `options` parameter to indicate if this value is scaled up (so there are no decimals) or in its natural scale.
- `noApprove` (boolean) Explicitly prevent this method from attempting an ERC-20 `approve` transaction prior to sending the `mint` transaction.
- `[options]` (CallOptions) Call options and Ethers.js overrides for the transaction. A passed `gasLimit` will be used in both the `approve` (if not supressed) and `mint` transactions.
- `RETURN` (object) Returns an Ethers.js transaction object of the supply transaction.

```js
const compound = new Compound(window.ethereum);

// Ethers.js overrides are an optional 3rd parameter for `supply`
// const trxOptions = { gasLimit: 250000, mantissa: false };

(async function() {

  console.log('Supplying ETH to the Compound Protocol...');
  const trx = await compound.supply(Compound.ETH, 1);
  console.log('Ethers.js transaction object', trx);

})().catch(console.error);
```

## Redeem

Redeems the user's Ethereum asset from the Compound Protocol.

- `asset` (string) A string of the asset to redeem, or its cToken name.
- `amount` (number \| string \| BigNumber) A string, number, or BigNumber object of the amount of an asset to redeem. Use the `mantissa` boolean in the `options` parameter to indicate if this value is scaled up (so there are no decimals) or in its natural scale. This can be an amount of cTokens or underlying asset (use the `asset` parameter to specify).
- `[options]` (CallOptions) Call options and Ethers.js overrides for the transaction.
- `RETURN` (object) Returns an Ethers.js transaction object of the redeem transaction.

```js
const compound = new Compound(window.ethereum);

(async function() {

  console.log('Redeeming ETH...');
  const trx = await compound.redeem(Compound.ETH, 1); // also accepts cToken args
  console.log('Ethers.js transaction object', trx);

})().catch(console.error);
```

## Borrow

Borrows an Ethereum asset from the Compound Protocol for the user. The user's address must first have supplied collateral and entered a corresponding market.

- `asset` (string) A string of the asset to borrow (must be a supported underlying asset).
- `amount` (number \| string \| BigNumber) A string, number, or BigNumber object of the amount of an asset to borrow. Use the `mantissa` boolean in the `options` parameter to indicate if this value is scaled up (so there are no decimals) or in its natural scale.
- `[options]` (CallOptions) Call options and Ethers.js overrides for the transaction.
- `RETURN` (object) Returns an Ethers.js transaction object of the borrow transaction.

```js
const compound = new Compound(window.ethereum);

(async function() {

  const daiScaledUp = '32000000000000000000';
  const trxOptions = { mantissa: true };

  console.log('Borrowing 32 Dai...');
  const trx = await compound.borrow(Compound.DAI, daiScaledUp, trxOptions);

  console.log('Ethers.js transaction object', trx);

})().catch(console.error);
```

## Repay Borrow

Repays a borrowed Ethereum asset for the user or on behalf of another Ethereum address.

- `asset` (string) A string of the asset that was borrowed (must be a supported underlying asset).
- `amount` (number \| string \| BigNumber) A string, number, or BigNumber object of the amount of an asset to borrow. Use the `mantissa` boolean in the `options` parameter to indicate if this value is scaled up (so there are no decimals) or in its natural scale.
- `[borrower]` (string \| null) The Ethereum address of the borrower to repay an open borrow for. Set this to `null` if the user is repaying their own borrow.
- `noApprove` (boolean) Explicitly prevent this method from attempting an ERC-20 `approve` transaction prior to sending the subsequent repayment transaction.
- `[options]` (CallOptions) Call options and Ethers.js overrides for the transaction. A passed `gasLimit` will be used in both the `approve` (if not supressed) and `repayBorrow` or `repayBorrowBehalf` transactions.
- `RETURN` (object) Returns an Ethers.js transaction object of the repayBorrow or repayBorrowBehalf transaction.

```js
const compound = new Compound(window.ethereum);

(async function() {

  console.log('Repaying Dai borrow...');
  const address = null; // set this to any address to repayBorrowBehalf
  const trx = await compound.repayBorrow(Compound.DAI, 32, address);

  console.log('Ethers.js transaction object', trx);

})().catch(console.error);
```