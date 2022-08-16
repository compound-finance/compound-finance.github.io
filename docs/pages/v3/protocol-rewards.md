---
layout: docs-content
title: Compound III Docs | Protocol Rewards
permalink: /v3/protocol-rewards/
docs_version: v3

## Element ID: In-page Heading
sidebar_nav_data:
  protocol-rewards: Protocol Rewards
  reward-accrual-tracking: Reward Accrual Tracking
  get-reward-accrued: Get Reward Accrued
  claim-rewards: Claim Rewards
---

# Protocol Rewards

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
