---
layout: docs-content
title: Compound.js Docs | Comptroller (v2)
permalink: /compound-js/comptroller/
docs_namespace: compound-js

## Element ID: In-page Heading
sidebar_nav_data:
  comptroller-methods: Comptroller Methods
  enter-markets: Enter Markets
  exit-market: Exit Market
---

# Compound.js

## Comptroller Methods

These methods facilitate interactions with the Comptroller smart contract. Methods like `claimComp` are in the Governance/COMP section.

## Enter Markets

Enters the user's address into Compound Protocol markets.

- `markets` (any[]) An array of strings of markets to enter, meaning use those supplied assets as collateral.
- `[options]` (CallOptions) Call options and Ethers.js overrides for the transaction. A passed `gasLimit` will be used in both the `approve` (if not supressed) and `mint` transactions.
- `RETURN` (object) Returns an Ethers.js transaction object of the enterMarkets transaction.

```js
const compound = new Compound(window.ethereum);

(async function () {
  const trx = await compound.enterMarkets(Compound.ETH); // Use [] for multiple
  console.log('Ethers.js transaction object', trx);
})().catch(console.error);
```

## Exit Market

Exits the user's address from a Compound Protocol market.

- `market` (string) A string of the symbol of the market to exit.
- `[options]` (CallOptions) Call options and Ethers.js overrides for the transaction. A passed `gasLimit` will be used in both the `approve` (if not supressed) and `mint` transactions.
- `RETURN` (object) Returns an Ethers.js transaction object of the exitMarket transaction.

```js
const compound = new Compound(window.ethereum);

(async function () {
  const trx = await compound.exitMarket(Compound.ETH);
  console.log('Ethers.js transaction object', trx);
})().catch(console.error);
```
