---
layout: docs-content
title: Compound II | Docs - Compound.js
permalink: /v2/compound-js/
docs_version: v2

## Element ID: In-page Heading
sidebar_nav_data:
  compoundjs: Compound.js
  compound-constructor: Compound Constructor
  api-methods: API Methods
  account: Account
  ctoken: cToken
  market-history: Market History
  governance: Governance
  ctoken-methods: cToken Methods
  supply: Supply
  redeem: Redeem
  borrow: Borrow
  repay-borrow: Repay Borrow
  comp-methods: COMP Methods
  to-checksum-address: To Checksum Address
  get-comp-balance: Get Comp Balance
  get-comp-accrued: Get Comp Accrued
  claim-comp: Claim Comp
  delegate: Delegate
  delegate-by-sig: Delegate By Sig
  create-delegate-signature: Create Delegate Signature
  comptroller-methods: Comptroller Methods
  enter-markets: Enter Markets
  exit-market: Exit Market
  ethereum-methods: Ethereum Methods
  read: Read
  trx: Trx
  get-balance: Get Balance
  governance-methods: Governance Methods
  cast-vote: Cast Vote
  cast-vote-by-sig: Cast Vote By Sig
  create-vote-signature: Create Vote Signature
  cast-vote-with-reason: Cast Vote With Reason
  price-feed-methods: Price Feed Methods
  get-price: Get Price
  utility-methods: Utility Methods
  get-address: Get Address
  get-abi: Get ABI
  get-network-name-with-chain-id: Get Network Name With Chain ID
---

# Compound.js

## Introduction

[Compound.js](https://github.com/compound-finance/compound-js){:target="_blank"} is a JavaScript SDK for Ethereum and the Compound Protocol. It wraps around Ethers.js, which is its only dependency. It is designed for both the web browser and Node.js.

The SDK is currently in open beta. For bugs reports and feature requests, either create an issue in the GitHub repository or send a message in the Development channel of the Compound Discord.

## Compound Constructor

Creates an instance of the Compound.js SDK.

- `[provider]` (Provider \| string) Optional Ethereum network provider. Defaults to Ethers.js fallback mainnet provider.
- `[options]` (object) Optional provider options.
- `RETURN` (object) Returns an instance of the Compound.js SDK.

```js
var compound = new Compound(window.ethereum); // web browser

var compound = new Compound('http://127.0.0.1:8545'); // HTTP provider

var compound = new Compound(); // Uses Ethers.js fallback mainnet (for testing only)

var compound = new Compound('ropsten'); // Uses Ethers.js fallback (for testing only)

// Init with private key (server side)
var compound = new Compound('https://mainnet.infura.io/v3/_your_project_id_', {
  privateKey: '0x_your_private_key_', // preferably with environment variable
});

// Init with HD mnemonic (server side)
var compound = new Compound('mainnet' {
  mnemonic: 'clutch captain shoe...', // preferably with environment variable
});
```

## API Methods

These methods facilitate HTTP requests to the Compound API.

## Account

Makes a request to the AccountService API. The Account API retrieves information for various accounts which have interacted with the protocol. For more details, see the Compound API documentation.

- `options` (object) A JavaScript object of API request parameters.
- `RETURN` (object) Returns the HTTP response body or error.


```js
(async function() {
  const account = await Compound.api.account({
    "addresses": "0xB61C5971d9c0472befceFfbE662555B78284c307",
    "network": "ropsten"
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

## cToken

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

## Market History

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

## Governance

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

## cToken Methods

These methods facilitate interactions with the cToken smart contracts.

## Supply

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

## COMP Methods

These methods facilitate interactions with the COMP token smart contract.

## To Checksum Address

Applies the EIP-55 checksum to an Ethereum address.

- `_address` (string) The Ethereum address to apply the checksum.
- `RETURN` (string) Returns a string of the Ethereum address.

## Get Comp Balance

Get the balance of COMP tokens held by an address.

- `_address` (string) The address in which to find the COMP balance.
- `[_provider]` (Provider \| string) An Ethers.js provider or valid network name string.
- `RETURN` (string) Returns a string of the numeric balance of COMP. The value is scaled up by 18 decimal places.


```js
(async function () {
  const bal = await Compound.comp.getCompBalance('0x2775b1c75658Be0F640272CCb8c72ac986009e38');
  console.log('Balance', bal);
})().catch(console.error);
```

## Get Comp Accrued

Get the amount of COMP tokens accrued but not yet claimed by an address.

- `_address` (string) The address in which to find the COMP accrued.
- `[_provider]` (Provider \| string) An Ethers.js provider or valid network name string.
- `RETURN` (string) Returns a string of the numeric accruement of COMP. The value is scaled up by 18 decimal places.


```js
(async function () {
  const acc = await Compound.comp.getCompAccrued('0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5');
  console.log('Accrued', acc);
})().catch(console.error);
```

## Claim Comp

Create a transaction to claim accrued COMP tokens for the user.

- `[options]` (CallOptions) Options to set for a transaction and Ethers.js method overrides.
- `RETURN` (object) Returns an Ethers.js transaction object of the vote transaction.


```js
const compound = new Compound(window.ethereum);

(async function() {

  console.log('Claiming COMP...');
  const trx = await compound.claimComp();
  console.log('Ethers.js transaction object', trx);

})().catch(console.error);
```

## Delegate

Create a transaction to delegate Compound Governance voting rights to an address.

- `_address` (string) The address in which to delegate voting rights to.
- `[options]` (CallOptions) Options to set for `eth_call`, optional ABI (as JSON object), and Ethers.js method overrides. The ABI can be a string of the single intended method, an array of many methods, or a JSON object of the ABI generated by a Solidity compiler.
- `RETURN` (object) Returns an Ethers.js transaction object of the vote transaction.


```js
const compound = new Compound(window.ethereum);

(async function() {
  const delegateTx = await compound.delegate('0xa0df350d2637096571F7A701CBc1C5fdE30dF76A');
  console.log('Ethers.js transaction object', delegateTx);
})().catch(console.error);
```

## Delegate By Sig

Delegate voting rights in Compound Governance using an EIP-712 signature.

- `_address` (string) The address to delegate the user's voting rights to.
- `nonce` (number) The contract state required to match the signature. This can be retrieved from the COMP contract's public nonces mapping.
- `expiry` (number) The time at which to expire the signature. A block timestamp as seconds since the unix epoch.
- `signature` (object) An object that contains the v, r, and, s values of an EIP-712 signature.
- `[options]` (CallOptions) Options to set for `eth_call`, optional ABI (as JSON object), and Ethers.js method overrides. The ABI can be a string of the single intended method, an array of many methods, or a JSON object of the ABI generated by a Solidity compiler.
- `RETURN` (object) Returns an Ethers.js transaction object of the vote transaction.


```js
const compound = new Compound(window.ethereum);

(async function() {
  const delegateTx = await compound.delegateBySig(
    '0xa0df350d2637096571F7A701CBc1C5fdE30dF76A',
    42,
    9999999999,
    {
      v: '0x1b',
      r: '0x130dbca2fafa07424c033b4479687cc1deeb65f08809e3ab397988cc4c6f2e78',
      s: '0x1debeb8250262f23906b1177161f0c7c9aa3641e8bff5b6f5c88a6bb78d5d8cd'
    }
  );
  console.log('Ethers.js transaction object', delegateTx);
})().catch(console.error);
```

## Create Delegate Signature

Create a delegate signature for Compound Governance using EIP-712. The signature can be created without burning gas. Anyone can post it to the blockchain using the `delegateBySig` method, which does have gas costs.

- `delegatee` (string) The address to delegate the user's voting rights to.
- `[expiry]` (number) The time at which to expire the signature. A block timestamp as seconds since the unix epoch. Defaults to `10e9`.
- `RETURN` (object) Returns an object that contains the `v`, `r`, and `s` components of an Ethereum signature as hexadecimal strings.


```js
const compound = new Compound(window.ethereum);

(async () => {

  const delegateSignature = await compound.createDelegateSignature('0xa0df350d2637096571F7A701CBc1C5fdE30dF76A');
  console.log('delegateSignature', delegateSignature);

})().catch(console.error);
```

## Comptroller Methods

These methods facilitate interactions with the Comptroller smart contract.

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

## Ethereum Methods

These methods facilitate interactions with the Ethereum blockchain.

## Read

This is a generic method for invoking JSON RPC's `eth_call` with Ethers.js. Use this method to execute a smart contract's constant or non-constant member without using gas. This is a read-only method intended to read a value or test a transaction for valid parameters. It does not create a transaction on the block chain.

- `address` (string) The Ethereum address the transaction is directed to.
- `method` (string) The smart contract member in which to invoke.
- `[parameters]` (any[]) Parameters of the method to invoke.
- `[options]` (CallOptions) Options to set for `eth_call`, optional ABI (as JSON object), and Ethers.js method overrides. The ABI can be a string of the single intended method, an array of many methods, or a JSON object of the ABI generated by a Solidity compiler.
- `RETURN` (Promise&lt;any&gt;) Return value of the invoked smart contract member or an error object if the call failed.

```js
const cEthAddress = Compound.util.getAddress(Compound.cETH);

(async function() {

  const srpb = await Compound.eth.read(
    cEthAddress,
    'function supplyRatePerBlock() returns (uint256)',
    // [], // [optional] parameters
    // {}  // [optional] call options, provider, network, plus Ethers.js "overrides"
  );

  console.log('cETH market supply rate per block:', srpb.toString());

})().catch(console.error);
```

## Trx

This is a generic method for invoking JSON RPC's `eth_sendTransaction` with Ethers.js. Use this method to create a transaction that invokes a smart contract method. Returns an Ethers.js `TransactionResponse` object.

- `address` (string) The Ethereum address the transaction is directed to.
- `method` (string) The smart contract member in which to invoke.
- `[parameters]` (any[]) Parameters of the method to invoke.
- `[options]` (CallOptions) Options to set for `eth_sendTransaction`, (as JSON object), and Ethers.js method overrides. The ABI can be a string optional ABI of the single intended method, an array of many methods, or a JSON object of the ABI generated by a Solidity compiler.
- `RETURN` (Promise&lt;any&gt;) Returns an Ethers.js `TransactionResponse` object or an error object if the transaction failed.

```js
const oneEthInWei = '1000000000000000000';
const cEthAddress = '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5';
const provider = window.ethereum;

(async function() {
  console.log('Supplying ETH to the Compound Protocol...');

  // Mint some cETH by supplying ETH to the Compound Protocol
  const trx = await Compound.eth.trx(
    cEthAddress,
    'function mint() payable',
    [],
    {
      provider,
      value: oneEthInWei
    }
  );

  // const result = await trx.wait(1); // JSON object of trx info, once mined

  console.log('Ethers.js transaction object', trx);
})().catch(console.error);
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

## Governance Methods

These methods facilitate interactions with the Governor smart contract.

## Cast Vote

Submit a vote on a Compound Governance proposal.

- `proposalId` (string) The ID of the proposal to vote on. This is an auto-incrementing integer in the Governor contract.
- `support` (number) A number value of 0, 1, or 2 for the proposal vote. The numbers correspond to 'in-favor', 'against', and 'abstain' respectively.
- `[options]` (CallOptions) Options to set for a transaction and Ethers.js method overrides.
- `RETURN` (object) Returns an Ethers.js transaction object of the vote transaction.


```js
const compound = new Compound(window.ethereum);

(async function() {
  const castVoteTx = await compound.castVote(12, 1);
  console.log('Ethers.js transaction object', castVoteTx);
})().catch(console.error);
```

## Cast Vote By Sig

Submit a vote on a Compound Governance proposal using an EIP-712 signature.

- `proposalId` (string) The ID of the proposal to vote on. This is an auto-incrementing integer in the Governor contract.
- `support` (number) A number value of 0, 1, or 2 for the proposal vote. The numbers correspond to 'in-favor', 'against', and 'abstain' respectively.
- `signature` (object) An object that contains the v, r, and, s values of an EIP-712 signature.
- `[options]` (CallOptions) Options to set for a transaction and Ethers.js method overrides.
- `RETURN` (object) Returns an Ethers.js transaction object of the vote transaction.

```js
const compound = new Compound(window.ethereum);

(async function() {
  const castVoteTx = await compound.castVoteBySig(
    12,
    1,
    {
      v: '0x1b',
      r: '0x130dbcd2faca07424c033b4479687cc1deeb65f08509e3ab397988cc4c6f2e78',
      s: '0x1debcb8250262f23906b1177161f0c7c9aa3641e6bff5b6f5c88a6bb78d5d8cd'
    }
  );
  console.log('Ethers.js transaction object', castVoteTx);
})().catch(console.error);
```

## Create Vote Signature

Create a vote signature for a Compound Governance proposal using EIP-712. This can be used to create an 'empty ballot' without burning gas. The signature can then be sent to someone else to post to the blockchain. The recipient can post one signature using the `castVoteBySig` method.

- `proposalId` (string) The ID of the proposal to vote on. This is an auto-incrementing integer in the Governor contract.
- `support` (number) A number value of 0, 1, or 2 for the proposal vote. The numbers correspond to 'in-favor', 'against', and 'abstain' respectively. To create an 'empty ballot' call this method thrice using `0`, `1`, and then `2` for this parameter.
- `RETURN` (object) Returns an object that contains the `v`, `r`, and `s` components of an Ethereum signature as hexadecimal strings.

```js
const compound = new Compound(window.ethereum);

(async () => {

  const voteForSignature = await compound.createVoteSignature(20, 1);
  console.log('voteForSignature', voteForSignature);

  const voteAgainstSignature = await compound.createVoteSignature(20, 0);
  console.log('voteAgainstSignature', voteAgainstSignature);

})().catch(console.error);
```

## Cast Vote With Reason

Submit a Compound Governance proposal vote with a reason.

- `proposalId` (string) The ID of the proposal to vote on. This is an auto-incrementing integer in the Governor contract.
- `support` (number) A number value of 0, 1, or 2 for the proposal vote. The numbers correspond to 'in-favor', 'against', and 'abstain' respectively.
- `reason` (string) A string of the reason for a vote selection.
- `[options]` (CallOptions) Options to set for a transaction and Ethers.js method overrides.
- `RETURN` (object) Returns an Ethers.js transaction object of the vote transaction.


```js
const compound = new Compound(window.ethereum);

(async function() {
  const castVoteTx = await compound.castVoteWithReason(12, 1, 'I vote YES because...');
  console.log('Ethers.js transaction object', castVoteTx);
})().catch(console.error);
```

## Price Feed Methods

These methods facilitate interactions with the Open Price Feed smart contracts.

## Get Price

Gets an asset's price from the Compound Protocol open price feed. The price
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
  console.log('WBTC in USD', price); // 6 decimals, see Open Price Feed docs

  price = await compound.getPrice(Compound.BAT, Compound.USDC); // supports cTokens too
  console.log('BAT in USDC', price);

})().catch(console.error);
```

## Utility Methods

These methods are helpers for the Compound class.

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

Gets the name of an Ethereum network based on its chain ID.

- `chainId` (string) The chain ID of the network.
- `RETURN` (string) Returns the name of the Ethereum network.

```js
console.log('Ropsten : ', Compound.util.getNetNameWithChainId(3));
```
