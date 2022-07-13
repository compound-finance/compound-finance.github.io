---
layout: docs-content
title: Compound III Docs | Collateral & Borrowing
permalink: /collateral-and-borrowing/

## Element ID: In-page Heading
sidebar_nav_data:
  collateral--borrowing: Collateral & Borrowing
  supply: Supply
  withdraw-or-borrow: Withdraw or Borrow
  collateral-balance: Collateral Balance
  borrow-collateralization: Borrow Collateralization
---

# Collateral & Borrowing

Users can add collateral assets to their account using the *[supply](#supply)* function. Collateral can only be added if the market is below its *[supplyCap](../helper-functions/#get-asset-info-by-address)*, which limits the protocol's risk exposure to collateral assets.

Each collateral asset increases the user's borrowing capacity, based on the asset's *[borrowCollateralFactor](../helper-functions/#get-asset-info-by-address)*. The borrowing collateral factors are percentages that represent the portion of collateral value that can be borrowed.

For instance, if the borrow collateral factor for WBTC is 85%, an account can borrow up to 85% of the USD value of its supplied WBTC in the base asset. Collateral factors can be fetched using the *[Get Asset Info By Address](../helper-functions/#get-asset-info-by-address)* function.

The base asset can be borrowed using the *[withdraw](#withdraw-or-borrow)* function; the resulting borrow balance must meet the borrowing collateral factor requirements. If a borrowing account subsequently fails to meet the borrow collateral factor requirements, it cannot borrow additional assets until it supplies more collateral, or reduces its borrow balance using the supply function.

Account *balances* for the base token are signed integers. An account balance greater than zero indicates the base asset is supplied and a balance less than zero indicates the base asset is borrowed. *Note: Base token balances for assets with 18 decimals will start to overflow at a value of 2<sup>103</sup>/1e18=~10 trillion.*

Account balances are stored internally in Comet as *principal* values (also signed integers). The principal value, also referred to as the day-zero balance, is what an account balance at *T<sub>0</sub>* would have to be for it to be equal to the account balance today after accruing interest.

Global *indices* for supply and borrow are unsigned integers that increase over time to account for the interest accrued on each side. When an account interacts with the protocol, the indices are updated and saved. An account's present balance can be calculated using the current index with the following formulas.

```
Balance=Principal * BaseSupplyIndex [Principal>0]
Balance=Principal * BaseBorrowIndex [Principal<0]
```

### Supply

The supply function transfers an asset to the protocol and adds it to the account's balance. This function can be used to **supply collateral, supply the base asset, or repay an open borrow** of the base asset.

If the base asset is supplied resulting in the account having a balance greater than zero, the base asset earns interest based on the current supply rate. Collateral assets that are supplied do not earn interest.

There are three separate methods to supply an asset to Compound III. The first is on behalf of the caller, the second is to a separate account, and the third is for a manager on behalf of an account.

Before supplying an asset to Compound III, the caller must first execute the asset's ERC-20 approve of the Comet contract.

#### Comet

```solidity
function supply(address asset, uint amount)

function supplyTo(address dst, address asset, uint amount)

function supplyFrom(address from, address dst, address asset, uint amount)
```

* `asset`: The address of the asset's smart contract.
* `amount`: The amount of the asset to supply to Compound III expressed as an integer. A value of `MaxUint256` will repay all of the `dst`'s base borrow balance.
* `dst`: The address that is credited with the supplied asset within the protocol.
* `from`: The address to supply from. This account must first use the Allow method in order to allow the sender to transfer its tokens prior to calling Supply.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.supply(0xERC20Address, 1000000);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.supply(usdcAddress, 1000000);
```

### Withdraw or Borrow

The withdraw method is used to **withdraw collateral** that is not currently supporting an open borrow. Withdraw is **also used to borrow the base asset** from the protocol if the account has supplied sufficient collateral. It can also be called from an allowed manager address.

Compound III implements a minimum borrow position size which can be found as `baseBorrowMin` in the [protocol configuration](../helper-functions/#get-protocol-configuration). A withdraw transaction to borrow that results in the account's borrow size being less than the `baseBorrowMin` will revert.

#### Comet

```solidity
function withdraw(address asset, uint amount)

function withdrawTo(address to, address asset, uint amount)

function withdrawFrom(address src, address to, address asset, uint amount)
```

* `asset`: The address of the asset that is being withdrawn or borrowed in the transaction.
* `amount`: The amount of the asset to withdraw or borrow. A value of `MaxUint256` will withdraw all of the `src`'s base balance.
* `to`: The address to send the withdrawn or borrowed asset.
* `src`: The address of the account to withdraw or borrow on behalf of. The `withdrawFrom` method can only be called by an allowed manager.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
comet.withdraw(0xwbtcAddress, 100000000);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.withdraw(usdcAddress, 100000000);
```

### Collateral Balance

This function returns the current balance of a collateral asset for a specified account in the protocol.

#### Comet

```solidity
function collateralBalanceOf(address account, address asset) external view returns (uint128)
```

* `account`: The address of the account in which to retrieve a collateral balance.
* `asset`: The address of the collateral asset smart contract.
* `RETURNS`: The balance of the collateral asset in the protocol for the specified account as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint balance = comet.collateralBalanceOf(0xAccount, 0xUsdcAddress);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const balance = await comet.callStatic.collateralBalanceOf('0xAccount', '0xUsdcAddress');
```

### Borrow Collateralization

This function returns true if the account passed to it has non-negative liquidity based on the borrow collateral factors. This function returns false if an account does not have sufficient liquidity to increase its borrow position. A return value of false does not necessarily imply that the account is presently liquidatable (see *[isLiquidatable](../liquidation/#liquidatable-accounts)* function).

#### Comet

```solidity
function isBorrowCollateralized(address account) public view returns (bool)
```

* `account`: The account to examine collateralization.
* `RETURNS`: Returns true if the account has enough liquidity for borrowing.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
bool isCollateralized = comet.isBorrowCollateralized(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const isCollateralized = await comet.callStatic.isBorrowCollateralized('0xAccount');
```

## Protocol Rewards

Compound III has a built-in system for tracking rewards for accounts that use the protocol. The full history of accrual of rewards are tracked for suppliers and borrowers of the base asset. The rewards can be any ERC-20 token. In order for rewards to accrue to Compound III accounts, the configuration's `baseMinForRewards` threshold for total supply of the base asset must be met.

### Reward Accrual Tracking

The reward accrual is tracked in the Comet contract and rewards can be claimed by users from an external Comet Rewards contract. Rewards are accounted for with up to 6 decimals of precision.

#### Comet

```solidity
function baseTrackingAccrued(address account) external view returns (uint64);
```

* `RETURNS`: Returns the amount of reward token accrued based on usage of the base asset within the protocol for the specified account, scaled up by `10 ^ 6`.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint64 accrued = comet.baseTrackingAccrued(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const accrued = await comet.callStatic.baseTrackingAccrued('0xAccount');
```

### Get Reward Accrued

The amount of reward token accrued but not yet claimed for an account can be fetched from the external Comet Rewards contract.

#### Comet Rewards

```solidity
struct RewardOwed {
    address token;
    uint owed;
}

function getRewardOwed(address comet, address account) external returns (RewardOwed memory)
```

* `RETURNS`: Returns the amount of reward token accrued but not yet claimed, scaled up by 10 to the "decimals" integer in the reward token's contract.

#### Solidity

```solidity
CometRewards rewards = CometRewards(0xRewardsAddress);
RewardOwed reward = rewards.getRewardOwed(0xCometAddress, 0xAccount);
```

#### Ethers.js v5.x

```js
const rewards = new ethers.Contract(contractAddress, abiJson, provider);
const [ tokenAddress, amtOwed ] = await rewards.callStatic.getRewardOwed(cometAddress, accountAddress);
```

### Claim Rewards

Any account can claim rewards for a specific account. Account owners and managers can also claim rewards to a specific address. The claim functions are available on the external Comet Rewards contract.

#### Comet Rewards

```solidity
function claim(address comet, address src, bool shouldAccrue) external
```

```solidity
function claimTo(address comet, address src, address to, bool shouldAccrue) external
```

* `comet`: The address of the Comet contract.
* `src`: The account in which to claim rewards.
* `to`: The account in which to transfer the claimed rewards.
* `shouldAccrue`: If true, the protocol will account for the rewards owed to the account as of the current block before transferring.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
CometRewards rewards = CometRewards(0xRewardsAddress);
rewards.claim(0xCometAddress, 0xAccount, true);
```

#### Ethers.js v5.x

```js
const rewards = new ethers.Contract(contractAddress, abiJson, provider);
await rewards.claim(cometAddress, accountAddress, true);
```