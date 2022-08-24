---
layout: docs-content
title: Compound III Docs | Account Management
permalink: /account-management/
docs_version: v3

## Element ID: In-page Heading
sidebar_nav_data:
  account-management: Account Management
  allow: Allow
  allow-by-signature: Allow By Signature
  user-nonce: User Nonce
  version: Version
  account-permissions: Account Permissions
  transfer: Transfer
  interfaces--erc-20-compatibility: Interfaces & ERC-20 Compatibility
---

# Account Management

In addition to self-management, Compound III accounts can enable other addresses to have write permissions for their account. Account managers can withdraw or transfer collateral within the protocol on behalf of another account. This is possible only after an account has enabled permissions by using the *[allow](#allow)* function.

### Allow

Allow or disallow another address to withdraw or transfer on behalf of the sender's address.

#### Comet

```solidity
function allow(address manager, bool isAllowed)
```

* `msg.sender`: The address of an account to allow or disallow a manager for.
* `manager`: The address of an account that becomes or will no longer be the manager of the owner.
* `isAllowed`: True to add the manager and false to remove the manager.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.allow(0xmanager, true);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.allow(managerAddress, true);
```

### Allow By Signature

This is a separate version of the allow function that enables submission using an EIP-712 offline signature. For more details on how to create an offline signature, review [EIP-712](https://eips.ethereum.org/EIPS/eip-712){:target="_blank"}.

#### Comet

```solidity
function allowBySig(
  address owner,
  address manager,
  bool isAllowed_,
  uint256 nonce,
  uint256 expiry,
  uint8 v,
  bytes32 r,
  bytes32 s
) external
```

* `owner`: The address of an account to allow or disallow a manager for. The signatory must be the owner address.
* `manager`: The address of an account that becomes or will no longer be the manager of the owner.
* `isAllowed`: True to add the manager and false to remove the manager.
* `nonce`: The contract state required to match the signature. This can be retrieved from the contract's public `userNonce` mapping.
* `expiry`: The time at which the signature expires. A block timestamp as seconds since the Unix epoch (uint).
* `v`: The recovery byte of the signature.
* `r`: Half of the ECDSA signature pair.
* `s`: Half of the ECDSA signature pair.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.allowBySig(0xowner, 0xmanager, true, nonce, expiry, v, r, s);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.allowBySig('0xowner', '0xmanager', true, nonce, expiry, v, r, s);
```

### User Nonce

This gets the user nonce, like an EVM account nonce, which is used by `allowBySig`.

#### Comet

```solidity
function userNonce(address) returns (uint)
```
* `address`: The address of the account in which to get a nonce.
* `RETURN`: An integer of the specified account's nonce.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint nonce = comet.userNonce(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const nonce = await comet.callStatic.userNonce('0xAccount');
```

### Version

This gets the protocol version which is used by `allowBySig`.

#### Comet

```solidity
function version() view returns (string memory)
```
* `RETURN`: A string of the protocol version number.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint version = comet.version();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const version = await comet.callStatic.version();
```

### Account Permissions

This function returns a boolean that indicates the status of an account's management address.

#### Comet

```solidity
function hasPermission(address owner, address manager) public view returns (bool)
```

* `owner`: The address of an account that can be managed by another.
* `manager`: The address of the account that can have manager permissions over another.
* `RETURNS`: Returns true if the `manager` address is presently a manager of the `owner` address.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
bool isManager = comet.hasPermission(0xOwner, 0xManager);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const isManager = await comet.callStatic.hasPermission('0xOwner', '0xManager');
```

### Transfer

This function is used to transfer an asset within the protocol to another address. A manager of an account is also able to perform a transfer on behalf of the account. Account balances change but the asset does not leave the protocol contract. The transfer will fail if it would make the account liquidatable.

There are two variants of the transfer function: `transfer` and `transferAsset`. The former conforms to the ERC-20 standard and transfers the base asset, while the latter requires specifying a specific asset to transfer.

#### Comet

```solidity
function transfer(address dst, uint amount)
```

```solidity
function transferFrom(address src, address dst, uint amount)
```

```solidity
function transferAsset(address dst, address asset, uint amount)
```

```solidity
function transferAssetFrom(address src, address dst, address asset, uint amount)
```

* `dst`: The address of an account that is the receiver in the transaction.
* `src`: The address of an account that is the sender of the asset in the transaction. This transfer method can only be called by an allowed manager.
* `asset`: The ERC-20 address of the asset that is being sent in the transaction.
* `amount`: The amount of the asset to transfer. A value of `MaxUint256` will transfer all of the `src`'s base balance.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.transfer(0xreceiver, 0xwbtcAddress, 100000000);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.transfer(receiverAddress, usdcAddress, 100000000);
```

### Interfaces & ERC-20 Compatibility

The Comet contract is a fully compatible ERC-20 wrapper for the base token. All of the interface methods of ERC-20 are externally exposed for accounts that supply or borrow. The **CometInterface.sol** contract file contains an example of a Solidity interface for the Comet contract.
