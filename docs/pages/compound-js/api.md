---
layout: docs-content
title: Compound.js Docs | API
permalink: /compound-js/api/
docs_namespace: compound-js

## Element ID: In-page Heading
sidebar_nav_data:
  api-methods: API Methods
  account-api: Account API
  ctoken-api: cToken API
  market-history-api: Market History API
  governance-api: Governance API
---

# Compound.js

## API Methods

These methods facilitate HTTP requests to the Compound API.

## Account API

Makes a request to the AccountService API. The Account API retrieves information for various accounts which have interacted with the protocol. For more details, see the Compound API documentation.

- `options` (object) A JavaScript object of API request parameters.
- `RETURN` (object) Returns the HTTP response body or error.

```js
(async function() {
  const account = await Compound.api.account({
    "addresses": "0xa0df350d2637096571F7A701CBc1C5fdE30dF76A",
  });

  let daiBorrowBalance = 0;
  if (Object.isExtensible(account) &amp;&amp; account.accounts) {
    account.accounts.forEach((acc) => {
      acc.tokens.forEach((tok) => {
        if (tok.symbol === Compound.cDAI) {
          daiBorrowBalance = +tok.borrow_balance_underlying.value;
        }
      });
    });
  }

  console.log('daiBorrowBalance', daiBorrowBalance);
})().catch(console.error);
```

## cToken API

Makes a request to the CTokenService API. The cToken API retrieves information about cToken contract interaction. For more details, see the Compound API documentation.

- `options` (object) A JavaScript object of API request parameters.
- `RETURN` (object) Returns the HTTP response body or error.

```js
(async function() {
  const cDaiData = await Compound.api.cToken({
    "addresses": Compound.util.getAddress(Compound.cDAI)
  });

  console.log('cDaiData', cDaiData); // JavaScript Object
})().catch(console.error);
```

## Market History API

Makes a request to the MarketHistoryService API. The market history service retrieves information about a market. For more details, see the Compound API documentation.

- `options` (object) A JavaScript object of API request parameters.
- `RETURN` (object) Returns the HTTP response body or error.

```js
(async function() {
  const cUsdcMarketData = await Compound.api.marketHistory({
    "asset": Compound.util.getAddress(Compound.cUSDC),
    "min_block_timestamp": 1559339900,
    "max_block_timestamp": 1598320674,
    "num_buckets": 10,
  });

  console.log('cUsdcMarketData', cUsdcMarketData); // JavaScript Object
})().catch(console.error);
```

## Governance API

Makes a request to the GovernanceService API. The Governance Service includes three endpoints to retrieve information about COMP accounts. For more details, see the Compound API documentation.

- `options` (object) A JavaScript object of API request parameters.
- `endpoint` (string) A string of the name of the corresponding governance service endpoint. Valid values are `proposals`, `voteReceipts`, or `accounts`.
- `RETURN` (object) Returns the HTTP response body or error.

```js
(async function() {
  const proposal = await Compound.api.governance(
    { "proposal_ids": [ 20 ] }, 'proposals'
  );

  console.log('proposal', proposal); // JavaScript Object
})().catch(console.error);
```