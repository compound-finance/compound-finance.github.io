---
layout: docs-content
title: Compound III Docs | Helper Functions
permalink: /v3/helper-functions/
docs_version: v3

## Element ID: In-page Heading
sidebar_nav_data:
  helper-functions: Helper Functions
  total-supply: Total Supply
  total-borrow: Total Borrow
  total-collateral: Total Collateral
  supplied-base-balance: Supplied Base Balance
  borrow-balance: Borrow Balance
  base-balance-as-integer: Base Balance as Integer
  account-data: Account Data
  get-asset-info: Get Asset Info
  get-asset-info-by-address: Get Asset Info By Address
  get-price: Get Price
  accrue-account: Accrue Account
  get-protocol-configuration: Get Protocol Configuration
  get-base-asset-market-information: Get Base Asset Market Information
  get-base-accrual-scale: Get Base Accrual Scale
  get-base-index-scale: Get Base Index Scale
  get-factor-scale: Get Factor Scale
  get-price-scale: Get Price Scale
  get-max-assets: Get Max Assets
  bulk-actions: Bulk Actions
  invoke: Invoke
---

# Helper Functions

### Total Supply

The total supply of base tokens supplied to the protocol plus interest accrued to suppliers.

#### Comet

```solidity
function totalSupply() override external view returns (uint256)
```

* `RETURN`: The amount of base asset scaled up by 10 to the "decimals" integer in the base asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint256 totalSupply = comet.totalSupply();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const totalSupply = await comet.callStatic.totalSupply();
```

### Total Borrow

The total amount of base tokens that are currently borrowed from the protocol plus interest accrued to all borrows.

#### Comet

```solidity
function totalBorrow() virtual external view returns (uint256)
```

* `RETURN`: The amount of base asset scaled up by 10 to the "decimals" integer in the base asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint256 totalBorrow = comet.totalBorrow();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const totalBorrow = await comet.callStatic.totalBorrow();
```

### Total Collateral

The protocol tracks the current amount of collateral that all accounts have supplied. Each valid collateral asset sum is tracked in a mapping with the asset address that points to a struct.

#### Comet

```solidity
struct TotalsCollateral {
    uint128 totalSupplyAsset;
    uint128 _reserved;
}

mapping(address => TotalsCollateral) public totalsCollateral;
```

* `address`:  The address of the collateral asset's contract.
* `RETURN`: A struct containing the stored data pertaining to the sum of the collateral in the protocol.
* `totalSupplyAsset`: A Solidity `uint128` of the sum of the collateral asset stored in the protocol, scaled up by 10 to the "decimals" integer in the asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
TotalsCollateral totalsCollateral = comet.totalsCollateral(0xERC20Address);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const [ totalSupplyAsset ] = await comet.callStatic.totalsCollateral('0xERC20Address');
```

### Supplied Base Balance

This function returns the current balance of base asset for a specified account in the protocol, including interest. If the account is presently borrowing or not supplying, it will return `0`.

#### Comet

```solidity
function balanceOf(address account) external view returns (uint256)
```

* `account`: The address of the account in which to retrieve the base asset balance.
* `RETURNS`: The balance of the base asset, including interest, in the protocol for the specified account as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint balance = comet.balanceOf(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const balance = await comet.callStatic.balanceOf('0xAccount');
```

### Borrow Balance

This function returns the current balance of borrowed base asset for a specified account in the protocol, including interest. If the account has a non-negative base asset balance, it will return `0`.

#### Comet

```solidity
function borrowBalanceOf(address account) external view returns (uint256)
```

* `account`: The address of the account in which to retrieve the borrowed base asset balance.
* `RETURNS`: The balance of the base asset, including interest, borrowed by the specified account as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint owed = comet.borrowBalanceOf(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const owed = await comet.callStatic.borrowBalanceOf('0xAccount');
```

### Base Balance as Integer

This function returns the current balance of base asset for a specified account in the protocol, including interest. If the account is currently borrowing, the return value will be negative. If the account is currently supplying the base asset, the return value will be positive.

#### Comet

```solidity
function baseBalanceOf(address account) external view returns (int104)
```

* `account`: The address of the account in which to retrieve the base asset balance.
* `RETURNS`: The balance of the base asset, including interest, that the specified account is due as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint baseBalance = comet.baseBalanceOf(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const baseBalance = await comet.callStatic.baseBalanceOf('0xAccount');
```

### Account Data

The protocol tracks data like the principal and indexes for each account that supplies and borrows. The data is stored in a mapping with the account address that points to a struct.

#### Comet

```solidity
struct UserBasic {
    int104 principal;
    uint64 baseTrackingIndex;
    uint64 baseTrackingAccrued;
    uint16 assetsIn;
}

mapping(address => UserBasic) public userBasic;
```

* `address`:  The address of the account that has used the protocol.
* `RETURN`: A struct containing the stored data pertaining to the account.
* `principal`: A Solidity `int104` of the amount of base asset that the account has supplied (greater than zero) or owes (less than zero) to the protocol.
* `baseTrackingIndex`: A Solidity `uint64` of the index of the account.
* `baseTrackingAccrued`: A Solidity `uint64` of the interest that the account has accrued.
* `assetsIn`: A Solidity `uint16` that tracks which assets the account has supplied as collateral. This storage implementation is for internal purposes and enables gas savings.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
UserBasic userBasic = comet.userBasic(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const [ principal, baseTrackingIndex, baseTrackingAccrued, assetsIn ] = await comet.callStatic.userBasic('0xAccount');
```

### Get Asset Info

This function returns asset information such as the collateral factors, asset price feed address, and more. In order to create a loop to fetch information for every asset, use the `numAssets` constant, which indicates the total number of supported assets.

#### Comet

```solidity
struct AssetInfo {
    uint8 offset;
    address asset;
    address priceFeed;
    uint64 scale;
    uint64 borrowCollateralFactor;
    uint64 liquidateCollateralFactor;
    uint64 liquidationFactor;
    uint128 supplyCap;
}

function getAssetInfo(uint8 i) public view returns (AssetInfo memory)
```

* `i`: The index of the asset based on the order it was added to the protocol. The index begins at `0`.
* `RETURNS`: The asset information as a struct called `AssetInfo`.
* `offset`: The index of the asset based on the order it was added to the protocol.
* `asset`: The address of the asset's smart contract.
* `priceFeed`: The address of the price feed contract for this asset.
* `scale`: An integer that equals `10 ^ x` where `x` is the amount of decimal places in the asset's smart contract.
* `borrowCollateralFactor`: The collateral factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `liquidateCollateralFactor`: The liquidate collateral factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `liquidationFactor`: The liquidation factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `supplyCap`: The supply cap of the asset as an integer scaled up by `10 ^ x` where `x` is the amount of decimal places in the asset's smart contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
AssetInfo info = comet.getAssetInfo(0);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const infoObject = await comet.callStatic.getAssetInfo(0);
```

### Get Asset Info By Address

This function returns asset information of a specific asset.

#### Comet

```solidity
struct AssetInfo {
    uint8 offset;
    address asset;
    address priceFeed;
    uint64 scale;
    uint64 borrowCollateralFactor;
    uint64 liquidateCollateralFactor;
    uint64 liquidationFactor;
    uint128 supplyCap;
}

function getAssetInfoByAddress(address asset) public view returns (AssetInfo memory)
```

* `address`: The address of the asset.
* `RETURNS`: The asset information as a struct called `AssetInfo`.
* `offset`: The index of the asset based on the order it was added to the protocol.
* `asset`: The address of the asset's smart contract.
* `priceFeed`: The address of the price feed contract for this asset.
* `scale`: An integer that equals `10 ^ x` where `x` is the amount of decimal places in the asset's smart contract.
* `borrowCollateralFactor`: The collateral factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `liquidateCollateralFactor`: The liquidate collateral factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `liquidationFactor`: The liquidation factor as an integer that represents the decimal value scaled up by `10 ^ 18`.
* `supplyCap`: The supply cap of the asset as an integer scaled up by `10 ^ x` where `x` is the amount of decimal places in the asset's smart contract.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
AssetInfo info = comet.getAssetInfoByAddress(0xAsset);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const infoObject = await comet.callStatic.getAssetInfoByAddress('0xAsset');
```

### Get Price

The protocol's prices are updated by [Chainlink Price Feeds](https://data.chain.link/). In order to fetch the present price of an asset, the price feed contract address for that asset must be passed to the `getPrice` function.

This function returns the price of an asset in USD with 8 decimal places.

#### Comet

```solidity
function getPrice(address priceFeed) public view returns (uint128)
```

* `priceFeed`: The ERC-20 address of the Chainlink price feed contract for the asset.
* `RETURNS`: Returns the USD price with 8 decimal places as an unsigned integer scaled up by `10 ^ 8`. E.g. `500000000000` means that the asset's price is $5000 USD.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint price = comet.getPrice(0xAssetAddress);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const price = await comet.callStatic.getPrice(usdcAddress);
```

### Accrue Account

This function triggers a manual accrual of interest and rewards to an account.

#### Comet

```solidity
function accrueAccount(address account) override external
```

* `account`: The account in which to accrue interest and rewards.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint price = comet.accrueAccount(0xAccount);
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
await comet.accrueAccount('0xAccount');
```

### Get Protocol Configuration

This function returns the configuration struct stored for a specific instance of Comet in the configurator contract.

#### Configurator

```solidity
struct Configuration {
    address governor;
    address pauseGuardian;
    address baseToken;
    address baseTokenPriceFeed;
    address extensionDelegate;

    uint64 kink;
    uint64 perYearInterestRateSlopeLow;
    uint64 perYearInterestRateSlopeHigh;
    uint64 perYearInterestRateBase;
    uint64 reserveRate;
    uint64 storeFrontPriceFactor;
    uint64 trackingIndexScale;
    uint64 baseTrackingSupplySpeed;
    uint64 baseTrackingBorrowSpeed;
    uint104 baseMinForRewards;
    uint104 baseBorrowMin;
    uint104 targetReserves;

    AssetConfig[] assetConfigs;
}

function getConfiguration(address cometProxy) external view returns (Configuration memory)
```

* `cometProxy`: The address of the Comet proxy to get the configuration for.
* `RETURNS`: Returns the protocol configuration.
  * `governor`: The address of the protocol Governor.
  * `pauseGuardian`: The address of the protocol pause guardian.
  * `baseToken`: The address of the protocol base token smart contract.
  * `baseTokenPriceFeed`: The address of the protocol base token price feed smart contract.
  * `extensionDelegate`: The address of the delegate of extra methods that did not fit in Comet.sol (CometExt.sol).
  * `kink`: The interest rate utilization curve kink.
  * `perYearInterestRateSlopeLow`: The interest rate slope low bound.
  * `perYearInterestRateSlopeHigh`: The interest rate slope high bound.
  * `perYearInterestRateBase`: The interest rate slope base.
  * `reserveRate`: The reserve rate that borrowers pay to the protocol reserves.
  * `storeFrontPriceFactor`: The fraction of the liquidation penalty that goes to buyers of collateral instead of the protocol.
  * `trackingIndexScale`: The scale for the index tracking protocol rewards.
  * `baseTrackingSupplySpeed`: The rate for protocol awards accrued to suppliers.
  * `baseTrackingBorrowSpeed`: The rate for protocol awards accrued to borrowers.
  * `baseMinForRewards`: The minimum amount of base asset supplied to the protocol in order for accounts to accrue rewards.
  * `baseBorrowMin`: The minimum allowed borrow size.
  * `targetReserves`: The amount of reserves allowed before absorbed collateral is no longer sold by the protocol.
  * `assetConfigs`: An array of all supported asset configurations.

#### Solidity

```solidity
Configurator configurator = Configurator(0xConfiguratorAddress);
Configuration config = configurator.getConfiguration(0xCometProxy);
```

#### Ethers.js v5.x

```js
const configurator = new ethers.Contract(contractAddress, abiJson, provider);
const config = await configurator.callStatic.getConfiguration('0xCometProxy');
```

### Get Base Asset Market Information

This function gets several of the current parameter values for the protocol market.

#### Comet

```solidity
struct TotalsBasic {
    uint64 baseSupplyIndex;
    uint64 baseBorrowIndex;
    uint64 trackingSupplyIndex;
    uint64 trackingBorrowIndex;
    uint104 totalSupplyBase;
    uint104 totalBorrowBase;
    uint40 lastAccrualTime;
    uint8 pauseFlags;
}

function totalsBasic() public override view returns (TotalsBasic memory)
```

* `RETURNS`: The base asset market information as a struct called `TotalsBasic` (defined in CometStorage.sol).
* `baseSupplyIndex`: The global base asset supply index for calculating interest accrued to suppliers.
* `baseBorrowIndex`: The global base asset borrow index for calculating interest owed by borrowers.
* `trackingSupplyIndex`: A global index for tracking participation of accounts that supply the base asset.
* `trackingBorrowIndex`:  A global index for tracking participation of accounts that borrow the base asset.
* `totalSupplyBase`: The total amount of base asset presently supplied to the protocol as an unsigned integer scaled up by 10 to the "decimals" integer in the base asset's contract.
* `totalBorrowBase`: The total amount of base asset presently borrowed from the protocol as an unsigned integer scaled up by 10 to the "decimals" integer in the base asset's contract.
* `lastAccrualTime`: The most recent time that protocol interest accrual was globally calculated. A block timestamp as seconds since the Unix epoch.
* `pauseFlags`: An integer that represents paused protocol functionality flags that are packed for data storage efficiency. See [Pause Protocol Functionality](../governance/#pause-protocol-functionality).

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
TotalsBasic tb = comet.totalsBasic();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const [ baseSupplyIndex, baseBorrowIndex, trackingSupplyIndex, trackingBorrowIndex, totalSupplyBase, totalBorrowBase, lastAccrualTime, pauseFlags ] = await comet.callStatic.totalsBasic();
```

### Get Base Accrual Scale

This function gets the scale for the base asset tracking accrual.

#### Comet

```solidity
function baseAccrualScale() override external pure returns (uint64)
```

* `RETURNS`: The integer used to scale down the base accrual when calculating a decimal value.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint baseAccrualScale = comet.baseAccrualScale();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const baseAccrualScale = await comet.callStatic.baseAccrualScale();
```

### Get Base Index Scale

This function gets the scale for the base asset index.

#### Comet

```solidity
function baseIndexScale() override external pure returns (uint64)
```

* `RETURNS`: The integer used to scale down the index when calculating a decimal value.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint baseIndexScale = comet.baseIndexScale();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const baseIndexScale = await comet.callStatic.baseIndexScale();
```

### Get Factor Scale

This function gets the scale for all protocol factors, i.e. borrow collateral factor.

#### Comet

```solidity
function factorScale() override external pure returns (uint64)
```

* `RETURNS`: The integer used to scale down the factor when calculating a decimal value.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint factorScale = comet.factorScale();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const factorScale = await comet.callStatic.factorScale();
```

### Get Price Scale

This function gets the scale integer for USD prices in the protocol, i.e. `8 decimals = 1e8`.

#### Comet

```solidity
function priceScale() override external pure returns (uint64)
```

* `RETURNS`: The integer used to scale down a price when calculating a decimal value.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint priceScale = comet.priceScale();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const priceScale = await comet.callStatic.priceScale();
```

### Get Max Assets

This function gets the maximum number of assets that can be simultaneously supported by Compound III.

#### Comet

```solidity
function maxAssets() override external pure returns (uint8)
```

* `RETURNS`: The maximum number of assets that can be simultaneously supported by Compound III.

#### Solidity

```solidity
Comet comet = Comet(0xCometAddress);
uint maxAssets = comet.maxAssets();
```

#### Ethers.js v5.x

```js
const comet = new ethers.Contract(contractAddress, abiJson, provider);
const maxAssets = await comet.callStatic.maxAssets();
```

## Bulk Actions

The Compound III codebase contains the source code of an external contract called *Bulker* that is designed to allow multiple Comet functions to be called in a single transaction.

Use cases of the Bulker contract include but are not limited to:
  * Supplying of a collateral asset and borrowing of the base asset.
  * Supplying or withdrawing of the native EVM token (like Ether) directly.
  * Transferring or withdrawing of the base asset without leaving dust in the account.

### Invoke

This function allows callers to pass an array of action codes and calldatas that are executed, one by one, in a single transaction.

#### Bulker

```solidity
uint public constant ACTION_SUPPLY_ASSET = 1;
uint public constant ACTION_SUPPLY_ETH = 2;
uint public constant ACTION_TRANSFER_ASSET = 3;
uint public constant ACTION_WITHDRAW_ASSET = 4;
uint public constant ACTION_WITHDRAW_ETH = 5;

function invoke(uint[] calldata actions, bytes[] calldata data) external payable
```

* `actions`: An array of integers that correspond to the actions defined in the contract constructor.
* `data`: An array of calldatas for each action to be called in the invoke transaction.
  * Supply Asset, Withdraw Asset, Transfer Asset
    * `to`: The destination address, within or external to the protocol.
    * `asset`: The address of the ERC-20 asset contract.
    * `amount`: The amount of the asset as an unsigned integer scaled up by 10 to the "decimals" integer in the asset's contract.
  * Supply ETH, Withdraw ETH (or equivalent native chain token)
    * `to`: The destination address, within or external to the protocol.
    * `amount`: The amount of the native token as an unsigned integer scaled up by 10 to the number of decimals of precision of the native EVM token.
* `RETURN`: No return, reverts on error.

#### Solidity

```solidity
Bulker bulker = Bulker(0xBulkerAddress);
// ERC-20 `approve` the bulker. Then Comet `allow` the bulker to be a manager before calling `invoke`.
bytes memory supplyAssetCalldata = (abi.encode('0xAccount', '0xAsset', amount);
bulker.invoke([ 1 ], [ supplyAssetCalldata ]);
```

#### Ethers.js v5.x

```js
const bulker = new ethers.Contract(contractAddress, abiJson, provider);
// ERC-20 `approve` the bulker. Then Comet `allow` the bulker to be a manager before calling `invoke`.
const supplyAssetCalldata = ethers.utils.defaultAbiCoder.encode(['address', 'address', 'uint'], ['0xAccount', '0xAsset', amount]);
await bulker.invoke([ 1 ], [ supplyAssetCalldata ]);
```
