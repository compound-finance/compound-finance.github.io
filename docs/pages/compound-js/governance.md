---
layout: docs-content
title: Compound.js Docs | Governance
permalink: /compound-js/governance/
docs_namespace: compound-js

## Element ID: In-page Heading
sidebar_nav_data:
  governance--comp-methods: Governance & COMP Methods
  cast-vote: Cast Vote
  cast-vote-by-signature: Cast Vote By Signature
  create-vote-signature: Create Vote Signature
  cast-vote-with-reason: Cast Vote With Reason
  comp-methods: COMP Methods
  get-comp-balance: Get COMP Balance
  get-comp-accrued: Get COMP Accrued
  claim-comp: Claim COMP
  delegate: Delegate
  delegate-by-signature: Delegate By Signature
  create-delegate-signature: Create Delegate Signature

---

# Compound.js

## Governance & COMP Methods

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

## Cast Vote By Signature

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

## COMP Methods

These methods facilitate interactions with the COMP token smart contract.

## Get COMP Balance

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

## Get COMP Accrued

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

## Claim COMP

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

## Delegate By Signature

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