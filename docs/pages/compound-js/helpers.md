---
layout: docs-content
title: Compound.js Docs | Helpers
permalink: /compound-js/helpers/
docs_namespace: compound-js

## Element ID: In-page Heading
sidebar_nav_data:
  helper--utility-methods: Helper & Utility Methods
  get-address: Get Address
  get-abi: Get ABI
  get-network-name-with-chain-id: Get Network Name With Chain ID
  get-balance: Get Balance
---

# Compound.js

## Helper & Utility Methods

These methods are helpers for the Compound class and basic utilities for EVM development.

## Get Address

Gets the contract address of the named contract. This method supports contracts used by the Compound Protocol.

- `contract` (string) The name of the contract.
- `[network]` (string) Optional name of the Ethereum network. Main net and all the popular public test nets are supported.
- `RETURN` (string) Returns the address of the contract.
```js
console.log('cETH Address: ', Compound.util.getAddress(Compound.cETH));
```

## Get ABI

Gets a contract ABI as a JavaScript array. This method supports contracts used by the Compound Protocol.

- `contract` (string) The name of the contract.
- `RETURN` (Array) Returns the ABI of the contract as a JavaScript array.
```js
console.log('cETH ABI: ', Compound.util.getAbi('cEther'));
```

## Get Network Name With Chain ID

Gets the name of an Ethereum network based on its chain ID. This method returns information only for chains that have a Compound deployment.

- `chainId` (string) The chain ID of the network.
- `RETURN` (string) Returns the name of the Ethereum network.
```js
console.log('Goerli : ', Compound.util.getNetNameWithChainId(5));
```

## Get Balance

Fetches the current Ether balance of a provided Ethereum address.

- `address` (string) The Ethereum address in which to get the ETH balance.
- `[provider]` (Provider \| string) Optional Ethereum network provider. Defaults to Ethers.js fallback mainnet provider.
- `RETURN` (BigNumber) Returns a BigNumber hexadecimal value of the ETH balance of the address.

```js
(async function () {

  balance = await Compound.eth.getBalance(myAddress, provider);
  console.log('My ETH Balance', +balance);

})().catch(console.error);
```
