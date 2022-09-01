---
layout: docs-content
title: Compound III Documentation
permalink: /
docs_namespace: v3

## Element ID: In-page Heading
sidebar_nav_data:
  compound-iii: Introduction
  networks: Networks
  what-does-each-protocol-contract-do: Protocol Contracts
  how-do-i-call-comet-methods: Calling Comet Methods
  how-do-i-deploy-compound-iii: Deploying
  security: Security
  code-examples: Code Examples

deployments:
  Ethereum Mainnet - USDC Base: ## this becomes the header text
    tab_text: Mainnet USDC
    blockscan_origin: 'https://etherscan.io/'
    contracts:
      cUSDCv3: '0xc3d688B66703497DAA19211EEdff47f25384cdc3'
      cUSDCv3 Implementation: '0x42F9505a376761b180e27a01bA0554244ED1DE7D'
      cUSDCv3 Ext: '0x285617313887d43256F852cAE0Ee4de4b68D45B0'
      Configurator: '0x316f9708bB98af7dA9c68C1C3b5e79039cD336E3'
      Configurator Implementation: '0xcFC1fA6b7ca982176529899D99af6473aD80DF4F'
      Proxy Admin: '0x1EC63B5883C3481134FD50D5DAebc83Ecd2E8779'
      Comet Factory: '0x1C1853Bc7C6bFf0D276Da53972C0b1a066DB1AE7'
      Rewards: '0x1B0e765F6224C21223AeA2af16c1C46E38885a40'
      Bulker: '0x74a81F84268744a40FEBc48f8b812a1f188D80C3'
      USDC: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
      COMP: '0xc00e94Cb662C3520282E6f5717214004A7f26888'
      WBTC: '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'
      WETH: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
      UNI: '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'
      LINK: '0x514910771AF9Ca656af840dff83E8264EcF986CA'
  Ethereum Kovan Testnet - USDC Base:
    tab_text: Kovan USDC
    blockscan_origin: 'https://kovan.etherscan.io/'
    contracts:
      cUSDCv3: '0xa7D85950E6E1bB7115c626cBB388Fa0a8C927c1c'
      cUSDCv3 Implementation: '0x875383444366331b7266baa1c330330ab351c5b2'
      cUSDCv3 Ext: '0x166eEC6266ff57A7Da43a1AfDb68FfCC3b87caac'
      Configurator: '0xDb3c6Ae44FE4689f142Ed8dE1a87304249d3d5a6'
      Configurator Implementation: '0xe60F5De591D22DB80804ac44DcCA9c16615bA00c'
      Proxy Admin: '0x1e5Ca6D2cc41935a3c39A3f3B29FBc779A2ceFEa'
      Comet Factory: '0xFCa21Dd5c442A2dB245DD44e7C9c3a28335a8558'
      Rewards: '0xC694877D91A8aEfb9D95cf34393cdC0DDdAded18'
      Bulker: '0x24cB9673158d19DE22cf4Fa747A1D30DAD60AEB5'
      USDC: '0xb6D5769d2877a462355F9A6eCa262D8826285c7D'
      COMP: '0xEe673239cBAc27aF34Bc39908405529E252d3c7B'
      WBTC: '0xDcB5Daf44164efFfC20E4418216b7F7f9064692b'
      WETH: '0xC3425E55c2C75bcdc99bD6DD0e515B0C421B60E4'
      UNI: '0x98d07Bcb5aA9D332361beA69f4749786dD812406'
      LINK: '0x20c5E16FEeD68F89166D20Da0dfe3CB7387BcCb3'
  Avalanche Fuji Testnet - USDC Base:
    tab_text: Fuji USDC
    blockscan_origin: 'https://testnet.snowtrace.io/'
    contracts:
      cUSDCv3: '0x59BF4753899C20EA152dEefc6f6A14B2a5CC3021'
      cUSDCv3 Implementation: '0x8ebf4Be4DB56a0273aE4e6f3Ae49A8aC2990304C'
      cUSDCv3 Ext: '0xcbfF67C09C90d7710BbD3046fD3556b1383170C7'
      Configurator: '0x8c083632099CBA949EA61A3044DB1B5A27818b20'
      Configurator Implementation: '0x215bbC327e77D4060dc7049eE299bdA3Ce48773B'
      Proxy Admin: '0x13046bAa7fB74dcd6f3f7A460092E11F5f91e419'
      Comet Factory: '0x0BFDf42b35b4D7e6E450c50b21f658b4E1216943'
      Rewards: '0x7CA364f9C4257FE2E22d503dD0E3f1c1Db41591d'
      USDC: '0x4fed3d02D095f7D92AF161311fA6Ef23dc8dA040'
      WAVAX: '0xA2c25E48269e3f89A60b2CC8e02AAfEeB3BAb761'
      WBTC.e: '0xfa78400e01Fc9da830Cb2F13B3e7E18F813414Ff'
---

# Compound III

## Introduction

[Compound III](https://github.com/compound-finance/comet) is an EVM compatible protocol that enables supplying of crypto assets as collateral in order to borrow the *base asset*. Accounts can also earn interest by supplying the base asset to the protocol.

The initial deployment of Compound III is on Ethereum and the base asset is USDC.

<!-- This can come back when the v3 app is live -->
<!-- The [app.compound.finance](https://app.compound.finance) interface is [open-source](https://github.com/compound-finance/palisade), deployed to IPFS, and is maintained by the community. -->

Please join the #development room in the Compound community [Discord](https://compound.finance/discord) server as well as the forums at [comp.xyz](https://comp.xyz); Compound Labs and members of the community look forward to helping you build an application on top of Compound III. Your questions help us improve, so please don't hesitate to ask if you can't find what you are looking for here.

For documentation of the Compound v2 Protocol, see [docs.compound.finance/v2](/v2/).

### Networks

The network deployment artifacts with contract addresses are available in the [Comet](https://github.com/compound-finance/comet) repository `deployments/` folder.

<div id="networks-widget-container"></div>

### What does each protocol contract do?

#### cUSDCv3

This is the main proxy contract for interacting with the new market. The address should remain fixed and independent from future upgrades to the market. It is an [OpenZeppelin TransparentUpgradeableProxy contract](https://docs.openzeppelin.com/contracts/4.x/api/proxy){:target="_blank"}.

#### cUSDCv3 Implementation

This is the implementation of the market logic contract, as deployed by the Comet Factory via the Configurator.

#### cUSDCv3 Ext

This is an extension of the market logic contract which supports some auxiliary/independent interfaces for the protocol. This is used to add additional functionality without requiring contract space in the main protocol contract.

#### Configurator

This is a [proxy](https://docs.openzeppelin.com/contracts/4.x/api/proxy#TransparentUpgradeableProxy){:target="_blank"} contract for the `configurator`, which is used to set and update parameters of a Comet proxy contract. The configurator deploys implementations of the Comet logic contract according to its configuration. This pattern allows significant gas savings for users of the protocol by 'constantizing' the parameters of the protocol.

#### Configurator Implementation

This is the implementation of the Configurator contract, which can also be upgraded to support unforeseen changes to the protocol.

#### Proxy Admin

This is the admin of the Comet and Configurator proxy contracts. It is a [ProxyAdmin](https://docs.openzeppelin.com/contracts/4.x/api/proxy#ProxyAdmin){:target="_blank"} as recommended/implemented by OpenZeppelin according to their upgradeability pattern.

#### Comet Factory

This is the factory contract capable of producing instances of the Comet implementation/logic contract, and invoked by the Configurator.

#### Rewards

This is a rewards contract which can hold rewards tokens (e.g. COMP, WETH) and allows claiming rewards by users, according to the core protocol tracking indices.

#### Bulker

This is an external contract that is not integral to Comet's function. It allows accounts to bulk multiple operations into a single transaction. This is a useful contract for Compound III user interfaces. The following is an example of steps in a bulked transaction.

- Wrap Ether to WETH
- Supply WETH collateral
- Supply WBTC collateral
- Borrow USDC

In addition to supplying, borrowing, and wrapping, the bulker contract can also transfer collateral within the protocol and claim rewards.

### How do I get the latest contract addresses?

Use the spider functionality in the Compound III repository. The addresses can then be found in the `deployments/` folder.

```
git clone https://github.com/compound-finance/comet.git
cd comet/
yarn
npx hardhat spider --deployment mainnet
```

### How do I call Comet methods?

Compound III has several contract files that make up the public Comet interface. The address of the Compound III upgradable proxy contract is used to call methods in Comet.sol, CometExt.sol, and CometCore.sol.

To get the ABI for Comet, run the build process in the [Compound III repository](https://github.com/compound-finance/comet). Look for the artifact of `CometInterface.sol` in the generated Hardhat artifacts folder.

```bash
## First, run the build command in the Compound III project repository
yarn run build
```

```js
// Reference the Hardhat artifact in  the Compound III project build files
const abi = require('./artifacts/contracts/CometInterface.sol/CometInterface.json').abi;

const comet = new ethers.Contract(cometAddress, abi, provider);
```

```solidity
pragma solidity 0.8.13;

import "./CometInterface.sol";

contract MyContract { //...
```

### How do I deploy Compound III?

To deploy to a public blockchain, see the `yarn deploy` instructions in the [README file of the Comet repository](https://github.com/compound-finance/comet#multi-chain-support). Be sure to first use the `spider` command to pull in the network's existing configuration and latest contract addresses.

Compound III can be deployed to EVM compatible blockchains. Here is an example for deploying to a locally run Ethereum node.

```
## In one command line window:
git clone https://github.com/compound-finance/comet.git
cd comet/
yarn install

## This runs the ethereum node locally
## The development mnemonic or private keys can be configured in hardhat.config.ts
npx hardhat node

## In another command line window:
cd comet/

## This deploys to the running local ethereum node
## It also writes deployment information to ./deployments/localhost/
yarn deploy --network localhost
```

## Security

The security of the Compound protocol is our highest priority; our development team, alongside third-party auditors and consultants, has invested considerable effort to create a protocol that we believe is safe and dependable. All contract code and balances are publicly verifiable, and security researchers are eligible for a bug bounty for reporting undiscovered vulnerabilities.

We believe that size, visibility, and time are the true test for the security of a smart contract; please exercise caution, and make your own determination of security and suitability.

### Audits

The Compound protocol has been reviewed & audited by [OpenZeppelin](https://openzeppelin.com/) and [ChainSecurity](https://chainsecurity.com/){:target="_blank"}.

1. [Compound III Audit by OpenZeppelin](https://blog.openzeppelin.com/compound-iii-audit/){:target="_blank"}
2. [Compound III Security Audit by ChainSecurity](https://chainsecurity.com/security-audit/compound-iii/){:target="_blank"}
{: .mega-ordered-list }

### Code Examples

The [Compound III Developer FAQ](https://github.com/compound-developers/compound-3-developer-faq){:target="_blank"} repository contains code examples for frequent Compound III developer tasks.

See `contracts/MyContract.sol` for Solidity examples, and also the individual JavaScript files in `examples/` for helpful use cases.
