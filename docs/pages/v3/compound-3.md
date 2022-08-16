---
layout: docs-content
title: Compound III
permalink: /v3/
docs_version: v3

## Element ID: In-page Heading
sidebar_nav_data:
  compound-iii: Introduction
  developer-resources: Developer Resources
  where-is-compound-iii-deployed: Networks
  how-do-i-get-the-latest-contract-addresses: Contract Addresses
  how-do-i-call-comet-methods: Calling Comet Methods
  how-do-i-deploy-compound-iii: Deploying
  code-examples: Code Examples
---

# Compound III

## Introduction

[Compound III](https://github.com/compound-finance/comet) is an EVM compatible protocol that enables supplying of crypto assets as collateral in order to borrow the *base asset*. Accounts can also earn interest by supplying the base asset to the protocol.

The initial deployment of Compound III is on Ethereum and the base asset is USDC.

The [app.compound.finance](https://app.compound.finance) interface is [open-source](https://github.com/compound-finance/palisade), deployed to IPFS, and is maintained by the community.

Please join the #development room in the Compound community [Discord](https://compound.finance/discord) server as well as the forums at [comp.xyz](https://comp.xyz); Compound Labs and members of the community look forward to helping you build an application on top of Compound III. Your questions help us improve, so please don't hesitate to ask if you can't find what you are looking for here.

For documentation of the Compound v2 Protocol, see [compound.finance/docs](https://compound.finance/docs).

## Developer Resources

### Where is Compound III Deployed?

The network deployment artifacts with contract addresses are available in the [Comet](https://github.com/compound-finance/comet) repository `deployments/` folder.

### How do I get the latest contract addresses?

Use the spider functionality in the Compound III repository. The addresses can then be found in the `deployments/` folder.

```
cd comet/
yarn
npx hardhat spider --network mainnet
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

### Code Examples

The [Compound III Developer FAQ](https://github.com/compound-developers/compound-3-developer-faq) repository contains code examples for frequent Compound III developer tasks.

See `contracts/MyContract.sol` for Solidity examples, and also the individual JavaScript files in `examples/` for the following cases:

- How do I supply collateral to Compound III? ([supply-withdraw-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/supply-withdraw-example.js))
- How do I borrow the base asset from Compound III? ([borrow-repay-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/borrow-repay-example.js))
- How do I get an asset price from the Compound III protocol's perspective? ([get-a-price.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/get-a-price.js))
- How do I get the Supply or Borrow APR from the protocol? ([get-apr-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/get-apr-example.js))
- How do I get the borrow capacity for a Compound III account? ([get-borrowable-amount.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/get-borrowable-amount.js))
- How do I get the borrow and liquidate collateral factors for a Compound III asset? ([get-cf-examples.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/get-cf-examples.js))
- How do I get the principal amount of asset for a Compound III account? ([get-principal-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/get-principal-example.js))
- How do I calculate the interest earned by a Compound III account? ([interest-earned-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/interest-earned-example.js))
- How do I repay my whole borrow precisely? ([repay-full-borrow-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/repay-full-borrow-example.js))
- How do I calculate the APR of COMP rewards? ([get-apr-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/get-apr-example.js))
- How do I find out the amount of COMP rewards currently accrued for my account? ([claim-reward-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/claim-reward-example.js))
- How do I find out the TVL? ([tvl-example.js](https://github.com/compound-developers/compound-3-developer-faq/blob/master/examples/tvl-example.js))

First install all of the repository's dependencies.

```
npm install
```

Be sure to set your JSON RPC provider URL at the top of `hardhat.config.js`. Also check the subdomain and make sure it points to the proper network.

```js
const providerUrl = 'https://eth-mainnet.alchemyapi.io/v2/__YOUR_API_KEY_HERE__';
```

Also make sure that the block number chosen to fork the chain for testing is near the latest block. This is also set in `hardhat.config.js` and can be found using the corresponding blockscan explorer website (i.e. Etherscan).

```js
const providerUrl = process.env.KOVAN_PROVIDER_URL;
const blockNumber = 32319250;
```

Use the mocha descriptions to run subsets of tests. **This repository currently supports the Kovan deployment only. See how the `net` variable at the top of each script is used.**

- To run all tests: `npm test`
- To run a single file's tests: `npm test -- -g "Find an account's Compound III base asset interest earned"`
  - Use the description in the top level describe block for the test file.
- To run a single test: `npm test -- -g 'Finds the interest earned of base asset'`
  - Use the description in the test level describe block.
