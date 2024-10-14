---
layout: docs-content
title: Compound.js Docs | Price Feed (v2)
permalink: /compound-js/price-feed/
docs_namespace: compound-js

## Element ID: In-page Heading
sidebar_nav_data:
  compound-v2-get-price: Compound v2 Get Price
---

# Compound.js

## Price Feed Methods

These methods facilitate interactions with the v2 Price Feed smart contracts. For Compound III price feed methods, see the Comet section.

## Compound v2 Get Price

Gets an asset's price from the Compound v2 Protocol price feed. The price
   of the asset can be returned in any other supported asset value, including
   all cTokens and underlyings.

- `asset` (string) A string of a supported asset in which to find the current price.
- `[inAsset]` (string) A string of a supported asset in which to express the `asset` parameter's price. This defaults to USD.
- `RETURN` (string) Returns a string of the numeric value of the asset.

```js
const compound = new Compound(window.ethereum);
let price;

(async function () {

  price = await compound.getPrice(Compound.WBTC);
  console.log('WBTC in USD', price); // 6 decimals, see Price Feed docs

  price = await compound.getPrice(Compound.BAT, Compound.USDC); // supports cTokens too
  console.log('BAT in USDC', price);

})().catch(console.error);
```