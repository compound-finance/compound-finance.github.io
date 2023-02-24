---
layout: docs-content
title: Compound III Docs | Governance
permalink: /governance/
docs_namespace: v3

## Element ID: In-page Heading
sidebar_nav_data:
  governance: Governance
  set-comet-factory: Set Comet Factory
  set-governor: Set Governor
  set-pause-guardian: Set Pause Guardian
  pause-protocol-functionality: Pause Protocol Functionality
  is-supply-paused: Is Supply Paused
  is-transfer-paused: Is Transfer Paused
  is-withdraw-paused: Is Withdraw Paused
  is-absorb-paused: Is Absorb Paused
  is-buy-paused: Is Buy Paused
  set-base-token-price-feed: Set Base Token Price Feed
  set-extension-delegate: Set Extension Delegate
  set-borrow-kink: Set Borrow Kink
  set-borrow-interest-rate-slope-low: Set Borrow Interest Rate Slope (Low)
  set-borrow-interest-rate-slope-high: Set Borrow Interest Rate Slope (High)
  set-borrow-interest-rate-slope-base: Set Borrow Interest Rate Slope (Base)
  set-supply-kink: Set Supply Kink
  set-supply-interest-rate-slope-low: Set Supply Interest Rate Slope (Low)
  set-supply-interest-rate-slope-high: Set Supply Interest Rate Slope (High)
  set-supply-interest-rate-slope-base: Set Supply Interest Rate Slope (Base)
  set-store-front-price-factor: Set Store Front Price Factor
  set-base-tracking-supply-speed: Set Base Tracking Supply Speed
  set-base-tracking-borrow-speed: Set Base Tracking Borrow Speed
  set-base-minimum-for-rewards: Set Base Minimum For Rewards
  set-borrow-minimum: Set Borrow Minimum
  set-target-reserves: Set Target Reserves
  add-a-new-asset: Add a New Asset
  update-an-existing-asset: Update an Existing Asset
  update-asset-price-feed: Update Asset Price Feed
  update-borrow-collateral-factor: Update Borrow Collateral Factor
  update-liquidation-collateral-factor: Update Liquidation Collateral Factor
  update-liquidation-factor: Update Liquidation Factor
  set-asset-supply-cap: Set Asset Supply Cap
  erc-20-approve-manager-address: ERC-20 Approve Manager Address
  transfer-governor: Transfer Governor
  withdraw-reserves: Withdraw Reserves


---

# Governance

Compound III is a decentralized protocol that is governed by holders and delegates of COMP. Governance allows the community to propose, vote, and implement changes through the administrative smart contract functions of the Compound III protocol. For more information on the Governor and Timelock see the original [governance](/v2/governance) section.

All instances of Compound III are controlled by the Timelock contract which is the same administrator of the Compound v2 protocol. The governance system has control over each *proxy*, the *Configurator implementation*, the *Comet factory*, and the *Comet implementation*.

Each time an immutable parameter is set via governance proposal, a new Comet implementation must be deployed by the Comet factory. If the proposal is approved by the community, the proxy will point to the new implementation upon execution.

To set specific protocol parameters in a proposal, the Timelock must call all of the relevant set methods on the *Configurator* contract, followed by `deployAndUpgradeTo` on the *CometProxyAdmin* contract.

## Governance on Other EVM Chains

The Compound III protocol can be deployed on any EVM chain. The deployment must have access to on-chain asset prices and messages passed from Ethereum Mainnet. The [Timelock](/v2/governance/#timelock) on Mainnet is the administrator of all community sanctioned instances of Compound III.

Each deployment outside of Mainnet needs to have a [Bridge Receiver](https://github.com/compound-finance/comet/blob/main/contracts/bridges/BaseBridgeReceiver.sol) and Local Timelock contract on its chain. Governance proposals executed on Ethereum must be read by the chain's bridge and published to the Bridge Receiver. Local Timelocks have an additional delay before Comet admin functions can be called via proposal execution.

Compound III instance initializations are logged on-chain using the [ENS text record system](https://docs.ens.domains/ens-improvement-proposals/ensip-5-text-records). The text record can only be modified by a Governance proposal. It can be viewed at [v3-additional-grants.compound-community-licenses.eth](https://app.ens.domains/name/v3-additional-grants.compound-community-licenses.eth/details) when the browser network is set to Ethereum Mainnet.

### Set Comet Factory

This function sets the official contract address of the Comet factory. The only acceptable caller is the Governor.

#### Configurator

```solidity
function setFactory(address cometProxy, address newFactory) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newFactory`: The address of the new Comet contract factory.
* `RETURN`: No return, reverts on error.

### Set Governor

This function sets the official contract address of the Compound III protocol Governor for subsequent proposals.

#### Configurator

```solidity
function setGovernor(address cometProxy, address newGovernor) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newGovernor`: The address of the new Compound III Governor.
* `RETURN`: No return, reverts on error.

### Set Pause Guardian

This function sets the official contract address of the Compound III protocol pause guardian. This address has the power to pause supply, transfer, withdraw, absorb, and buy collateral operations within Compound III.

COMP token-holders designate the Pause Guardian address, which is held by the [Community Multi-Sig](https://etherscan.io/address/0xbbf3f1421d886e9b2c5d716b5192ac998af2012c){:target="_blank"}.

#### Configurator

```solidity
function setPauseGuardian(address cometProxy, address newPauseGuardian) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newPauseGuardian`: The address of the new pause guardian.
* `RETURN`: No return, reverts on error.

### Pause Protocol Functionality

This function pauses the specified protocol functionality in the event of an unforeseen vulnerability. The only addresses that are allowed to call this function are the Governor and the Pause Guardian.

#### Comet

```solidity
function pause(
    bool supplyPaused,
    bool transferPaused,
    bool withdrawPaused,
    bool absorbPaused,
    bool buyPaused
) override external
```

* `supplyPaused`: Enables or disables all accounts' ability to supply assets to the protocol.
* `transferPaused`: Enables or disables all account's ability to transfer assets within the protocol.
* `withdrawPaused`: Enables or disables all account's ability to withdraw assets from the protocol.
* `absorbPaused`: Enables or disables protocol absorptions.
* `buyPaused`: Enables or disables the protocol's ability to sell absorbed collateral.
* `RETURN`: No return, reverts on error.

### Is Supply Paused

This function returns a boolean indicating whether or not the protocol supply functionality is presently paused.

#### Comet

```solidity
function isSupplyPaused() override public view returns (bool)
```

* `RETURN`: A boolean value of whether or not the protocol functionality is presently paused.

### Is Transfer Paused

This function returns a boolean indicating whether or not the protocol transfer functionality is presently paused.

#### Comet

```solidity
function isTransferPaused() override public view returns (bool)
```

* `RETURN`: A boolean value of whether or not the protocol functionality is presently paused.

### Is Withdraw Paused

This function returns a boolean indicating whether or not the protocol withdraw functionality is presently paused.

#### Comet

```solidity
function isWithdrawPaused() override public view returns (bool)
```

* `RETURN`: A boolean value of whether or not the protocol functionality is presently paused.

### Is Absorb Paused

This function returns a boolean indicating whether or not the protocol absorb functionality is presently paused.

#### Comet

```solidity
function isAbsorbPaused() override public view returns (bool)
```

* `RETURN`: A boolean value of whether or not the protocol functionality is presently paused.

### Is Buy Paused

This function returns a boolean indicating whether or not the protocol's selling of absorbed collateral functionality is presently paused.

#### Comet

```solidity
function isBuyPaused() override public view returns (bool)
```

* `RETURN`: A boolean value of whether or not the protocol functionality is presently paused.

### Set Base Token Price Feed

This function sets the official contract address of the price feed of the protocol base asset.

#### Configurator

```solidity
function setBaseTokenPriceFeed(address cometProxy, address newBaseTokenPriceFeed) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newBaseTokenPriceFeed`: The address of the new price feed contract.
* `RETURN`: No return, reverts on error.

### Set Extension Delegate

This function sets the official contract address of the protocol's Comet extension delegate. The methods in **CometExt.sol** are able to be called via the same proxy as **Comet.sol**.

#### Configurator

```solidity
function setExtensionDelegate(address cometProxy, address newExtensionDelegate) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newExtensionDelegate`: The address of the new extension delegate contract.
* `RETURN`: No return, reverts on error.

### Set Borrow Kink

This function sets the borrow interest rate utilization curve kink for the Compound III base asset.

#### Configurator

```solidity
function setBorrowKink(address cometProxy, uint64 newKink) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newKink`: The new kink parameter.
* `RETURN`: No return, reverts on error.

### Set Borrow Interest Rate Slope (Low)

This function sets the borrow interest rate slope low bound in the approximate amount of seconds in one year.

#### Configurator

```solidity
function setBorrowPerYearInterestRateSlopeLow(address cometProxy, uint64 newSlope) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newSlope`: The slope low bound as an unsigned integer.
* `RETURN`: No return, reverts on error.

### Set Borrow Interest Rate Slope (High)

This function sets the borrow interest rate slope high bound in the approximate amount of seconds in one year.

#### Configurator

```solidity
function setBorrowPerYearInterestRateSlopeHigh(address cometProxy, uint64 newSlope) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newSlope`: The slope high bound as an unsigned integer.
* `RETURN`: No return, reverts on error.

### Set Borrow Interest Rate Slope (Base)

This function sets the borrow interest rate slope base in the approximate amount of seconds in one year.

#### Configurator

```solidity
function setBorrowPerYearInterestRateBase(address cometProxy, uint64 newBase) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newSlope`: The slope base as an unsigned integer.
* `RETURN`: No return, reverts on error.

### Set Supply Kink

This function sets the supply interest rate utilization curve kink for the Compound III base asset.

#### Configurator

```solidity
function setSupplyKink(address cometProxy, uint64 newKink) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newKink`: The new kink parameter.
* `RETURN`: No return, reverts on error.

### Set Supply Interest Rate Slope (Low)

This function sets the supply interest rate slope low bound in the approximate amount of seconds in one year.

#### Configurator

```solidity
function setSupplyPerYearInterestRateSlopeLow(address cometProxy, uint64 newSlope) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newSlope`: The slope low bound as an unsigned integer.
* `RETURN`: No return, reverts on error.

### Set Supply Interest Rate Slope (High)

This function sets the supply interest rate slope high bound in the approximate amount of seconds in one year.

#### Configurator

```solidity
function setSupplyPerYearInterestRateSlopeHigh(address cometProxy, uint64 newSlope) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newSlope`: The slope high bound as an unsigned integer.
* `RETURN`: No return, reverts on error.

### Set Supply Interest Rate Slope (Base)

This function sets the supply interest rate slope base in the approximate amount of seconds in one year.

#### Configurator

```solidity
function setSupplyPerYearInterestRateBase(address cometProxy, uint64 newBase) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newSlope`: The slope base as an unsigned integer.
* `RETURN`: No return, reverts on error.

### Set Store Front Price Factor

This function sets the fraction of the liquidation penalty that goes to buyers of collateral instead of the protocol. This factor is used to calculate the discount rate of collateral for sale as part of the account absorption process. The rate is a decimal scaled up by `10 ^ 18`.

#### Configurator

```solidity
function setStoreFrontPriceFactor(address cometProxy, uint64 newStoreFrontPriceFactor) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newStoreFrontPriceFactor`: The new price factor as an unsigned integer expressed as a decimal scaled up by `10 ^ 18`.
* `RETURN`: No return, reverts on error.

### Set Base Tracking Supply Speed

This function sets the rate at which base asset supplier accounts accrue rewards.

#### Configurator

```solidity
function setBaseTrackingSupplySpeed(address cometProxy, uint64 newBaseTrackingSupplySpeed) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newBaseTrackingSupplySpeed`: The rate as an APR expressed as a decimal scaled up by `10 ^ 18`.
* `RETURN`: No return, reverts on error.

### Set Base Tracking Borrow Speed

This function sets the rate at which base asset borrower accounts accrue rewards.

#### Configurator

```solidity
function setBaseTrackingBorrowSpeed(address cometProxy, uint64 newBaseTrackingBorrowSpeed) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newBaseTrackingBorrowSpeed`: The rate as an APR expressed as a decimal scaled up by `10 ^ 18`.
* `RETURN`: No return, reverts on error.

### Set Base Minimum For Rewards

This function sets the minimum amount of base asset supplied to the protocol in order for accounts to accrue rewards.

#### Configurator

```solidity
function setBaseMinForRewards(address cometProxy, uint104 newBaseMinForRewards) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newBaseMinForRewards`: The amount of base asset scaled up by 10 to the "decimals" integer in the base asset's contract.
* `RETURN`: No return, reverts on error.

### Set Borrow Minimum

This function sets the minimum amount of base token that is allowed to be borrowed.

#### Configurator

```solidity
function setBaseBorrowMin(address cometProxy, uint104 newBaseBorrowMin) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `setBaseBorrowMin`: The minimum borrow as an unsigned integer scaled up by 10 to the "decimals" integer in the base asset's contract.
* `RETURN`: No return, reverts on error.

### Set Target Reserves

This function sets the target reserves amount. Once the protocol reaches this amount of reserves of base asset, liquidators cannot buy collateral from the protocol.

#### Configurator

```solidity
function setTargetReserves(address cometProxy, uint104 newTargetReserves) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newTargetReserves`: The amount of reserves of base asset as an unsigned integer scaled up by 10 to the "decimals" integer in the base asset's contract.
* `RETURN`: No return, reverts on error.

### Add a New Asset

This function adds an asset to the protocol through governance.

#### Configurator

```solidity
function addAsset(address cometProxy, AssetConfig calldata assetConfig) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `assetConfig`: The configuration that is added to the array of protocol asset configurations.
* `RETURN`: No return, reverts on error.

### Update an Existing Asset

This function modifies an existing asset's configuration parameters.

#### Configurator

```solidity
function updateAsset(address cometProxy, AssetConfig calldata newAssetConfig) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `newAssetConfig`: The configuration that is modified in the array of protocol asset configurations. All parameters are overwritten.
* `RETURN`: No return, reverts on error.

### Update Asset Price Feed

This function updates the price feed contract address for a specific asset.

#### Configurator

```solidity
function updateAssetPriceFeed(address cometProxy, address asset, address newPriceFeed) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `asset`: The address of the underlying asset smart contract.
* `newPriceFeed`: The address of the new price feed smart contract.
* `RETURN`: No return, reverts on error.

### Update Borrow Collateral Factor

This function updates the borrow collateral factor for an asset in the protocol.

#### Configurator

```solidity
function updateAssetBorrowCollateralFactor(address cometProxy, address asset, uint64 newBorrowCF) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `asset`: The address of the underlying asset smart contract.
* `newBorrowCF`: The collateral factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `RETURN`: No return, reverts on error.

### Update Liquidation Collateral Factor

This function updates the liquidation collateral factor for an asset in the protocol.

#### Configurator

```solidity
function updateAssetLiquidateCollateralFactor(address cometProxy, address asset, uint64 newLiquidateCF) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `asset`: The address of the underlying asset smart contract.
* `newLiquidateCF`: The collateral factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `RETURN`: No return, reverts on error.

### Update Liquidation Factor

This function updates the liquidation factor for an asset in the protocol.

The liquidation factor is a decimal value that is between 0 and 1 (inclusive) which determines the amount that is paid out to an underwater account upon liquidation.

The following is an example of the liquidation factor's role in a Compound III liquidation:

An underwater account has supplied $100 of WBTC as collateral. If the WBTC liquidation factor is `0.9`, the user will receive $90 of the base asset when a liquidator triggers an absorption of their account.

#### Configurator

```solidity
function updateAssetLiquidationFactor(address cometProxy, address asset, uint64 newLiquidationFactor) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `asset`: The address of the underlying asset smart contract.
* `newLiquidationFactor`: The factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `RETURN`: No return, reverts on error.

### Set Asset Supply Cap

This function sets the maximum amount of an asset that can be supplied to the protocol. Supply transactions will revert if the total supply would be greater than this number as a result.

#### Configurator

```solidity
function updateAssetSupplyCap(address cometProxy, address asset, uint128 newSupplyCap) external
```

* `cometProxy`: The address of the Comet proxy to set the configuration for.
* `asset`: The address of the underlying asset smart contract.
* `newSupplyCap`: The amount of the asset as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.
* `RETURN`: No return, reverts on error.

### ERC-20 Approve Manager Address

This function sets the Comet contract's ERC-20 allowance of an asset for a manager address. It can only be called by the Governor.

In the event of a governance attack, an attacker could create a proposal that leverages this function to give themselves permissions to freely transfer all ERC-20 tokens out of the Comet contract.

Hypothetically, the attacker would need to either acquire supreme voting weight or add a malicious step in an otherwise innocuous and popular proposal and the community would fail to detect before approving.

#### Comet

```solidity
function approveThis(address manager, address asset, uint amount) override external
```

* `manager`: The address of a manager account that has its allowance modified.
* `asset`: The address of the asset's smart contract.
* `amount`: The amount of the asset approved for the manager expressed as an integer.
* `RETURN`: No return, reverts on error.

### Transfer Governor

This function changes the address of the Configurator's Governor.

#### Configurator

```solidity
function transferGovernor(address newGovernor) external
```

* `newGovernor`: The address of the new Governor for Configurator.
* `RETURN`: No return, reverts on error.

### Withdraw Reserves

This function allows governance to withdraw base token reserves from the protocol and send them to a specified address. Only the Governor address may call this function.

#### Comet

```solidity
function withdrawReserves(address to, uint amount) external
```

* `to`: The address of the recipient of the base asset tokens.
* `amount`: The amount of the base asset to send scaled up by 10 to the "decimals" integer in the base asset's contract.
* `RETURN`: No return, reverts on error.
