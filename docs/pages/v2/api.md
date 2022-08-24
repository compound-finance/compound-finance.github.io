---
layout: docs-content
title: Compound II | Docs - API
permalink: /v2/api/
docs_version: v2

## Element ID: In-page Heading
sidebar_nav_data:
  compound-api: Compound API
  account-service: AccountService
  ctoken-service: CTokenService
  market-history-service: MarketHistoryService
  governance-service: GovernanceService
  shared-data-types: Shared Data Types
---

# Compound API

## Introduction

The Compound API input and output formats are specified by [Protocol Buffers](https://developers.google.com/protocol-buffers/){:target="_blank"}, known colloquially as protobufs. Unlike typical protobufs endpoints, the Compound endpoints support JSON for input and output in addition to the protobufs binary format. To use JSON in both the input and the output, specify the headers `"Content-Type: application/json"` and `"Accept: application/json"` in the request.

The Compound API no longer supports the Ethereum testnets.

It is a possibility that in the future, API keys will be required to access the API.

## AccountService
{:id='account-service'}

The Account API retrieves information for various accounts which have interacted with Compound. You can use this API to pull data about a specific account by address, or alternatively, pull data for a list of unhealthy accounts (that is, accounts which are approaching under-collateralization).

```js
// Retreives list of accounts and related supply and borrow balances.
fetch("https://api.compound.finance/api/v2/account");

// Returns details for given account
fetch("https://api.compound.finance/api/v2/account?addresses[]=0x00..");
```

#### GET: `/account`

#### AccountRequest

The request to the account API can specify a number filters, such as which addresses to retrieve information about or general health requirements. The following shows an example set of request parameters in JSON:

```js
{
  "addresses": [] // returns all accounts if empty or not included
  "block_number": 0 // returns latest if given 0
  "max_health": { "value": "10.0" }
  "min_borrow_value_in_eth": { "value": "0.002" }
  "page_number": 1
  "page_size": 10
}
```

| Type    | Key         | Description |
|---------|-------------|-------------|
| bytes | `addresses` | List of account addresses to filter on, e.g.: ["0x...", ,"0x..."] (Optional) |
| Precise | `min_borrow_value_in_eth` | Filter for accounts which total outstanding borrows exceeding given amount. (Optional) |
| Precise | `max_health` | Filter for accounts where outstanding borrows divided by collateral value is less than the provided amount. If returned value is less than 1.0, for instance, the account is subject to liquidation. If provided, should be given as `{ "value": "...string formatted number..." }` (Optional) |
| uint32 | `block_number` | If provided, API returns data for given block number from our historical data. Otherwise, API defaults to returning the latest information. (Optional) |
| uint32 | `block_timestamp` | If provided, API returns data for given timestamp from our historical data. Otherwise, API defaults to returning the latest information. (Optional) |
| uint32 | `page_size` | Number of accounts to include in the response, default is 10 e.g. page_size=10 (Optional) |
| uint32 | `page_number` | Pagination number for accounts in the response, default is 1 e.g. page_number=1 (Optional) |

#### AccountResponse

The account API returns an overall picture of accounts matching the filters on Compound.

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1; INVALID_PAGE_NUMBER = 2; INVALID_PAGE_SIZE = 3;` |
| AccountRequest | `request` | The request parameters are echoed in the response. |
| PaginationSummary | `pagination_summary` | For example | `{ "page_number": 1, "page_size": 100, "total_entries": 83, "total_pages": 1 }` |
| Account | `accounts` |The list of accounts (see Account below) matching the requested filter, with the associated account and cToken data. |

#### Account

This includes a list of cTokens contextualized to each account.

```js
{
  "address": "0xbac065be2e8ca097e9ac924e94af000dd3a5663"
  "health": { "value": "1.07264275673050348990755599431194797431802239523113293682619605751591901" }
  "tokens": [
    {
      "address": "0xf5dce57282a584d2746faf1593d3121fcac444dc"
      "borrow_balance_underlying": {"value": "131.4682716123015"}
      "lifetime_borrow_interest_accrued": {"value": "0.44430505829286"}
      "lifetime_supply_interest_accrued": {"value": "0.0000021671829864899976"}
      "supply_balance_underlying": {"value": "0.0"}
    }
  ],
  "total_borrow_value_in_eth": {"value": "0.5100157047140227313856015174794473200000000000000000000000000000" }
  "total_collateral_value_in_eth": {"value": "0.54706465148029978664135447293587201124121731200000000000000000000000000" }
}
```

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The public Ethereum address of the account
| Precise | `total_collateral_value_in_eth` | The value of all collateral supplied by the account. Calculated as cTokens held • exchange rate • collateral factor. Note: assets can be supplied and gain interest without being counted as collateral.
| Precise | `total_borrow_value_in_eth` | The value of all outstanding borrows with accumulated interest.
| Precise | `health` |  `total_collateral_value_in_eth / total_borrow_value_in_eth`. If this value is less than 1.0, the account is subject to liquidation.
| int32 | `block_updated` | 
| AccountCToken | `tokens`| A list of tokens held by this account, see `AccountCToken` below for details.|

#### AccountCToken

An account's supply, borrow, and interest information for a particular cToken.

```js
{
  "address": "0xf5dce57282a584d2746faf1593d3121fcac444dc"
  "borrow_balance_underlying": {"value": "131.4682716123015"}
  "lifetime_borrow_interest_accrued": {"value": "0.44430505829286"}
  "lifetime_supply_interest_accrued": {"value": "0.0000021671829864899976"}
  "supply_balance_underlying": {"value": "0.0"}
}
```

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the cToken |
| string | `symbol` | The symbol of the cToken |
| Precise | `supply_balance_underlying` | The cToken balance converted to underlying `tokenscTokens held • exchange rate` |
| Precise | `borrow_balance_underlying` | The borrow balance (this is denominated in the underlying token, not in cTokens) |
| Precise | `lifetime_supply_interest_accrued` | The amount of supply interest accrued for the lifetime of this account-cToken pair. |
| Precise | `lifetime_borrow_interest_accrued` | The amount of borrow interest accrued for the lifetime of this account-cToken pair. |
| Precise | `safe_withdraw_amount_underlying` | The amount of supply that can be withdrawn such that the user's health remains at 1.25 or higher. |

## CTokenService
{:id='ctoken-service'}

#### GET: `/ctoken`

#### CTokenRequest

The request to the cToken API can specify a number filters, such as which tokens to retrieve information about or moment in time. The following shows an example set of request parameters in JSON:

```js
{
  "addresses": [] // returns all tokens if empty or not included
  "block_timestamp": 0 // returns latest information if given 0
}
```

| Type | Key | Description |
|------|-----|-------------|
| bytes | `addresses` | List of token addresses to filter on, e.g.: ["0x...", ,"0x..."] (Optional) |
| uint32 | `block_number` | Only one of block_number or block timestamp should be provided. If provided, API returns data for given block number from our historical data. Otherwise, API defaults to returning the latest information. (Optional) |
| uint32 | `block_timestamp` | Only one of block_number or block timestamp should be provided. If provided, API returns data for given block timestamp from our historical data. Otherwise, API defaults to returning the latest information. (Optional) |
| bool | `meta` | Pass true to get metadata for the token addresses specified. (Optional) |

#### CTokenResponse

The cToken API returns an overall picture of cTokens matching the filter.

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | |
| CTokenRequest | `request` | The request parameters are echoed in the response. |
| CToken | `cToken` | The list of cToken (see `CToken` below) matching the requested filter. |
| CTokenMeta | `meta` | Metadata for all CTokens specified |

#### CToken

This includes a list of cTokens contextualized to the full market.

```js
{
 "cToken": [{
   "borrow_rate": {"value": "0.051453109785093843"},
   "cash": {"value": "514.078443"},
   "collateral_factor": {"value": "0.80000000000000000"},
   "exchange_rate": {"value": "0.020024242770802729"},
   "interest_rate_model_address": "0x1a43bfd39b15dcf444e17ab408c4b5be32deb7f5",
   "name": "Compound USD Coin",
   "number_of_borrowers": 3,
   "number_of_suppliers": 34,
   "reserves": {"value": "0"},
   "reserve_factor": {"value": "0.10000000000000000"},
   "supply_rate": {"value": "0.013237112532748109"},
   "symbol": "cUSDC",
   "token_address": "0x5b281a6dda0b271e91ae35de655ad301c976edb1",
   "total_borrows": {"value": "178.064546"},
   "total_supply": {"value": "34565.25157651"},
   "underlying_address": "0x4dbcdf9b62e891a7cec5a2568c3f4faf9e8abe2b",
   "underlying_name": "USD Coin",
   "underlying_price": {"value": "0.0041368287055953530000000000"},
   "underlying_symbol":"USDC"
  }],
 "error": null,
 "request": {
   "addresses": ["0x5b281a6dda0b271e91ae35de655ad301c976edb1"],
   "block_number": 4515576,
   "block_timestamp": 0
  }
}
```

| Type | Key | Description |
|------|-----|-------------|
| bytes | `token_address` | The public Ethereum address of the cToken |
| Precise | `total_supply` |  The number of cTokens in existence |
| Precise | `total_borrows` | The amount of underlying tokens borrowed from the cToken |
| Precise | `reserves` |  The amount of underylying tokens held by reserves |
| Precise | `cash` |  The current liquidity of the cToken |
| Precise | `exchange_rate` | The cToken / underlying exchange rate. This rate increases over time as supply interest accrues. |
| Precise | `supply_rate` | The floating supply interest rate |
| Precise | `borrow_rate` | The floating borrow interest rate |
| Precise | `collateral_factor` | The amount of the value of the underlying token that will count as collateral. eg. cEth with collataral factor 0.75 means 1 eth of supply allows 0.75 eth of borrowing. |
| uint32 |  `number_of_suppliers` | The number of accounts holding this cToken |
| uint32 |  `number_of_borrowers` | The number of accounts with oustanding borrows |
| Precise | `underlying_price` |  The price of the underlying token in eth |
| bytes | `underlying_address` |  The address of the underlying token |
| string |  `symbol` |  The symbol of the ctoken |
| string |  `name` |  The name of the ctoken |
| string |  `underlying_symbol` | The symbol of the underlying token |
| string |  `underlying_name` | The name of the underlying token |
| bytes | `interest_rate_model_address` | The address of the interest rate model |
| Precise | `reserve_factor` |  The amount of borrow interest that is converted into reserves |
| Precise | `comp_supply_apy` | The floating comp apy for supplying this token |
| Precise | `comp_borrow_apy` | The floating comp apy for borrowing this token |
| Precise | `borrow_cap` |  The maximum size of total borrows for this market, beyond which no new borrows will be given |

#### CTokenMeta

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `unique_suppliers` | Number of non-duplicate suppliers between all specified markets |
| uint32 | `unique_borrowers` | Number of non-duplicate borrowers between all specified markets |

## MarketHistoryService
{:id='market-history-service'}

The market history service retrieves historical information about a market. You can use this API to find out the values of interest rates at a certain point in time. Its especially useful for making charts and graphs of the time-series values.

```js
// Returns 10 buckets of market data
fetch("https://api.compound.finance/api/v2/market_history/graph?asset=0xf5dce57282a584d2746faf1593d3121fcac444dc&amp;min_block_timestamp=1556747900&amp;max_block_timestamp=1559339900&amp;num_buckets=10");
```

#### GET: `/graph`

#### MarketHistoryGraphRequest

The market history graph API returns information about a market between two timestamps. The requestor can choose the asset and number of buckets to return within the range. For example:

```js
{
 "asset": "0xf5dce57282a584d2746faf1593d3121fcac444dc",
 "min_block_timestamp": 1556747900,
 "max_block_timestamp": 1559339900,
 "num_buckets": 10
}
```

| Type | Key | Description |
|------|-----|-------------|
| bytes | `asset` | The requested asset |
| uint32 | `min_block_timestamp` | Unix epoch time in seconds |
| uint32 | `max_block_timestamp` | Unix epoch time in seconds |
| uint32 | `num_buckets` | How many buckets to group data points in |

#### MarketHistoryGraphResponse

The market history graph API response contains the rates for both suppliers and borrowers, as well as the sequence of total supply and borrows for the given market.

| Type | Key | Description |
|------|-----|--------------|
| Error | `error` |If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1; INVALID_REQUEST = 2` |
| bytes | `asset` |The asset in question |
| Rate |  `supply_rates` | The historical interest rates for suppliers |
| Rate |  `borrow_rates` | The historical interest rates for borrowers |
| MarketTotal | `total_supply_history` | The historical total supply amounts for the market |
| MarketTotal | `total_borrows_history` |The historical total borrow amounts for the market |
| Rate |  `exchange_rates` | The historical exchange rate |
| Price | `prices_usd` | The historical usd price of asset |

#### MarketTotal

| Type | Key | Description |
|------|-----|--------------|
| uint32 | `block_number`  | The block number of the data point |
| uint32 | `block_timestamp` | The timestamp of the block of the data point |
| Precise | `total` | The total value of the asset in asset-WEI terms. |

#### Price

| Type | Key | Description |
|------|-----|--------------|
| uint32 | `block_number` | The block number of the data point|
| uint32 | `block_timestamp` | The timestamp of the block of the data point|
| Precise | `price` | The price of the underlying token in usd at that block number|

#### Rate

| Type | Key | Description |
|------|-----|--------------|
| uint32| `block_number` | The block number of the data point|
| uint32| `block_timestamp` | The timestamp of the block of the data point|
| double| `rate`  | The rate as a value between 0 and 1|

## GovernanceService
{:id='governance-service'}

The Governance Service includes three endpoints to retrieve information about COMP accounts, governance proposals, and proposal vote receipts. You can use the APIs below to pull data about the Compound governance system:

```js
// Retreives a list of governance proposals
fetch("https://api.compound.finance/api/v2/governance/proposals");

// Retreives a list of governance proposal vote receipts
fetch("https://api.compound.finance/api/v2/governance/proposal_vote_receipts");

// Retreives a list of COMP accounts
fetch("https://api.compound.finance/api/v2/governance/accounts");
```

#### GET: `/governance/proposals`

#### ProposalRequest

The request to the Proposal API can specify a number of filters, such as which ids to retrieve information about or state of proposals.

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `proposal_ids`  | List of ids to filter on, e.g.: `?proposal_ids[]=23,25` (Optional) |
| string | `state` | The state of the proposal to filter on, (e.g.: "pending", "active", "canceled", "defeated", "succeeded", "queued", "expired", "executed") (Optional) |
| bool | `with_detail` | Set as true to include proposer and action data, default is false (Optional) |
| uint32 | `page_size` | Number of proposals to include in the response, default is 10 e.g. `page_size=10` (Optional) |
| uint32 | `page_number` | Pagination number for proposals in the response, default is 1 e.g. `page_number=1` (Optional) |

#### ProposalResponse

The Proposal API returns a list of proposals that match the given filters on the request in descending order by `proposal_id`.

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1; INVALID_PAGE_NUMBER = 2; INVALID_PAGE_SIZE = 3; INVALID_PROPOSAL_ID = 4; INVALID_PROPOSAL_STATE = 5;` |
| ProposalRequest | `request` | The request parameters are echoed in the response. |
| PaginationSummary | `pagination_summary` | For example: `{ "page_number": 1, "page_size": 100, "total_entries": 83, "total_pages": 1 }` |
| Proposal | `proposals` | The list of proposals matching the requested filter |

#### DisplayCompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the given COMP account |
| string | `display_name`  | A human readable name that describes who owns the account |
| string | `image_url` | A url to retrieve an account image |
| string | `account_url` | A url for the organization/user of the COMP account |

#### Proposal

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `id` | Unique ID for looking up a proposal
| string | `title` | The title that describes the proposal |
| string | `description` | A description of the actions the proposal will take if successful |
| DisplayCompAccount | `proposer`  | Either`null` or an object with data about the creator of the proposal (See DisplayCompAccount). Only populated when request submitted `with_detail=true` |
| ProposalAction | `actions` | Either `null` or an array of actions (See ProposalAction) that will be queued and executed if proposal succeeds. Only populated when request submitted `with_detail=true` |
| ProposalState | `states`  | An array of states (See ProposalState) that represent the state transitions that the proposal has undergone |
| string | `for_votes` | The number of votes in support of the proposal |
| string | `against_votes` | The number of votes in opposition to this proposal |

#### ProposalAction

| Type | Key | Description |
|------|-----|-------------|
| string | `title` | The title that describes the action |
| bytes | `target` | The address to send the calldata to |
| string | `value` | The value of ETH to send with the transaction |
| string | `signature` | The function signature of the function to call at the target address |
| string | `data` | The encoded argument data for the action |

#### ProposalState

| Type | Key | Description |
|------|-----|-------------|
| string | `state` | The state objects type, (e.g.: pending, active, canceled, defeated, succeeded, queued, expired, executed) |
| uint32 | `start_time` | The start timestamp of state |
| uint32 | `end_time` | Either `null` or the definitive end timestamp or an estimated end timestamp of the state |
| string | `trx_hash` | Either `null` or the transaction hash that represents the state transition |

#### GET: `/governance/proposal_vote_receipts`

#### ProposalVoteReceiptRequest

The request to the Proposal Vote Receipt API can specify a number of filters, such as which id to retrieve information about or which account.

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `proposal_id` | A proposal id to filter on, e.g. `?proposal_id=23` (Optional) |
| bytes | `account` | Filter for proposals receipts for the given account (Optional) |
| bool | `support` | Filter for proposals receipts by for votes with `support=true` or against votes with `support=false`. If support not specified, response will return paginated votes for both for and against votes (Optional) |
| bool | `with_proposal_data` | Will populate a proposal object on the vote receipt when request submitted with `with_proposal_data=true`, default is false (Optional) |
| uint32 | `page_size` | Number of proposal vote receipts to include in the response, default is 10 e.g. `page_size=10` (Optional) |
| uint32 | `page_number` | Pagination number for proposal vote receipts in the response, default is 1 e.g. `page_number=1` (Optional) |

#### ProposalVoteReceiptResponse

The Proposal Vote Receipt API returns a list of proposal vote receipts that match the given filters on the request

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1; INVALID_PAGE_NUMBER = 2; INVALID_PAGE_SIZE = 3; INVALID_PROPOSAL_ID = 4; INVALID_ACCOUNT = 6;` |
| ProposalVoteReceiptRequest | `request` | The request parameters are echoed in the response. |
| PaginationSummary | `pagination_summary` | For example: `{ "page_number": 1, "page_size": 100, "total_entries": 83, "total_pages": 1 }` |
| ProposalVoteReceipt | `proposal_vote_receipts` | The list of proposal vote receipts matching the requested filter |

#### DisplayCompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the given COMP account |
| string | `display_name` | A human readable name that describes who owns the account |
| string | `image_url` | A url to retrieve an account image |
| string | `account_url` | A url for the organization/user of the COMP account |

#### Proposal

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `id` | Unique id for looking up a proposal |
| string | `title` | The title that describes the proposal |
| string | `description` | A description of the actions the proposal will take if successful |
| DisplayCompAccount | `proposer` | Either`null` or an object with data about the creator of the proposal (See DisplayCompAccount). Only populated when request submitted `with_detail=true` |
| ProposalAction | `actions` | Either `null` or an array of actions (See ProposalAction) that will be queued and executed if proposal succeeds. Only populated when request submitted `with_detail=true` |
| ProposalState | `states` | An array of states (See ProposalState) that represent the state transitions that the proposal has undergone |
| string | `for_votes` | The number of votes in support of the proposal |
| string | `against_votes` | The number of votes in opposition to this proposal |

#### ProposalVoteReceipt

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `proposal_id` | The proposal id the vote receipt corresponds to |
| Proposal | `proposal`  | Either `null` or the object with proposal data (See Proposal). Only populated when request submitted `with_proposal_data=true` |
| DisplayCompAccount | `voter` | The object with voter data (See DisplayCompAccount) |
| bool | `support` | Whether or not the voter supports the proposal |
| string | `votes` | The number of votes cast by the voter |

#### GET: `/governance/accounts`

#### GovernanceAccountRequest

The request to the Governance Account API can specify a number of filters, such as which accounts to retrieve information about.

| Type | Key | Description |
|------|-----|-------------|
| bytes | `addresses` | A list of accounts to filter on, e.g.: `?addresses=0x...` (Optional) |
| string | `order_by` | Filter for accounts by. E.g. "votes", "balance", or "proposals_created" (Optional) |
| bool | `with_history` | Will populate a list of transaction history for the accounts when request is submitted `with_history=true` |
| uint32 | `page_size` | Number of accounts to include in the response, default is 10 e.g. `page_size=10` (Optional) |
| uint32 | `page_number` | Pagination number for accounts in the response, default is 1 e.g. `page_number=1` (Optional) |

#### GovernanceAccountResponse

The Governance Account API returns a list of accounts that match the given filters on the request

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1; INVALID_PAGE_NUMBER = 2; INVALID_PAGE_SIZE = 3; INVALID_ACCOUNT = 6; INVALID_FILTER_BY = 7;` |
| GovernanceAccountRequest | `request` | The request parameters are echoed in the response. |
| PaginationSummary | `pagination_summary`  | For example: `{ "page_number": 1, "page_size": 100, "total_entries": 83, "total_pages": 1 }` |
| CompAccount | `accounts`  | The list of governance accounts matching the requested filter |

#### CompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes  | `address` | The address of the given COMP account |
| string | `display_name` | A human readable name that describes who owns the account |
| string | `image_url` | A url to retrieve an account image |
| string | `account_url` | A url for the organization/user of the COMP account |
| string | `balance` | The balance of COMP for the given account |
| string | `votes` | The total votes delegated to the account |
| string | `vote_weight` | The percentage of voting weight of the 10,000,000 total COMP |
| uint32 | `proposals_created` | The number of proposals created in the Compound Governance System |
| DisplayCompAccount | `delegate` | The account this COMP account is delegating to (See DisplayCompAccount) |
| uint32 | `rank` | Either `null` or the rank order of top 100 COMP accounts for votes |
| CompAccountTransaction | `transactions` | Either `null` or a list of historical transactions for the account (See CompAccountTransaction) |
| uint32 | `proposals_voted` | The number of proposals voted on in the Compound Governance System |
| uint32 | `total_delegates` | The number of addresses delegating to this account |
| CrowdProposal | `crowd_proposal` | Either `null` or a description of the crowd proposal the comp_moment represents (See CrowdProposal) |

#### CompAccountTransaction

| Type | Key | Description |
|------|-----|-------------|
| string | title | A human readable title representing the transaction |
| uint32 | timestamp | The timestamp the transaction occurred |
| string | trx_hash | The transaction hash of the transaction |
| string | delta | The change in value on the Comp Account |

#### CrowdProposal

| Type | Key | Description |
|------|-----|-------------|
| bytes | `proposal_address` | The address of the given COMP Crowd Proposal |
| string | `title` | The title that describes the proposal |
| string | `description` | A description of the actions the proposal will take if successful |
| DisplayCompAccount | `author` | An object with data about the author of the proposal (See DisplayCompAccount). |
| ProposalAction | `actions` | An array of actions (See ProposalAction) that will be queued and executed if proposal succeeds. |
| uint32 | `create_time` | The timestamp the crowd proposal was created |
| uint32 | `propose_time` | The timestamp the crowd proposal was proposed |
| uint32 | `terminate_time` | The timestamp the crowd proposal was terminated |
| string | `state` | The current state of the crowd proposal (e.g.: gathering_votes, proposed, terminated) |

#### DisplayCompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the given COMP account |
| string  | `display_name` | A human readable name that describes who owns the account |
| string  | `image_url` | A url to retrieve an account image |
| string  | `account_url` | A url for the organization/user of the COMP account |

#### GET: `/governance/accounts/search`

#### GovernanceAccountSearchRequest

The request to the Governance Account API can specify a number of filters, such as which accounts to retrieve information about.

| Type | Key | Description |
|------|-----|-------------|
| string | `term` | A string to search accounts by. The search term can be part of an address or display name, e.g. "0x1234" or "The Purple Diamonds" |
| uint32 | `page_size` | Number of accounts to include in the response, default is 10 e.g. `page_size=10` (Optional) |
| uint32 | `page_number` | Pagination number for accounts in the response, default is 1 e.g. `page_number=1` (Optional) |

#### GovernanceAccountSearchResponse

The Governance Account API returns a list of accounts that match the given filters on the request

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1;` |
| GovernanceAccountSearchRequest |  `request` | The request parameters are echoed in the response. |
| PaginationSummary | `pagination_summary` | For example: `{ "page_number": 1, "page_size": 100, "total_entries": 83, "total_pages": 1 }` |
| CompAccount | `accounts` | The list of governance accounts matching the requested search term |

#### CompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the given COMP account |
| string | `display_name` | A human readable name that describes who owns the account |
| string | `image_url` | A url to retrieve an account image |
| string | `account_url` | A url for the organization/user of the COMP account |
| string | `balance` | The balance of COMP for the given account |
| string | `votes` | The total votes delegated to the account |
| string | `vote_weight` | The percentage of voting weight of the 10,000,000 total COMP |
| uint32 | `proposals_created` | The number of proposals created in the Compound Governance System |
| DisplayCompAccount | `delegate` | The account this COMP account is delegating to (See DisplayCompAccount) |
| uint32 | `rank` | Either `null` or the rank order of top 100 COMP accounts for votes |
| CompAccountTransaction | `transactions` | Either `null` or a list of historical transactions for the account (See CompAccountTransaction) |
| uint32 | `proposals_voted` | The number of proposals voted on in the Compound Governance System |
| uint32 | `total_delegates` | The number of addresses delegating to this account |
| CrowdProposal | `crowd_proposal` | Either `null` or a description of the crowd proposal the comp_moment represents (See CrowdProposal) |

#### CompAccountTransaction

| Type | Key | Description |
|------|-----|-------------|
| string | `title` | A human readable title representing the transaction |
| uint32 | `timestamp` | The timestamp the transaction occurred |
| string | `trx_hash` | The transaction hash of the transaction |
| string | `delta` | The change in value on the Comp Account |

#### CrowdProposal

| Type | Key | Description |
|------|-----|-------------|
| bytes | `proposal_address` | The address of the given COMP Crowd Proposal |
| string | `title` | The title that describes the proposal |
| string | `description` | A description of the actions the proposal will take if successful |
| DisplayCompAccount | `author` | An object with data about the author of the proposal (See DisplayCompAccount). |
| ProposalAction | `actions` | An array of actions (See ProposalAction) that will be queued and executed if proposal succeeds. |
| uint32 | `create_time` | The timestamp the crowd proposal was created |
| uint32 | `propose_time` | The timestamp the crowd proposal was proposed |
| uint32 | `terminate_time` | The timestamp the crowd proposal was terminated |
| string | `state` | The current state of the crowd proposal (e.g.: gathering_votes, proposed, terminated) |

#### DisplayCompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the given COMP account |
| string | `display_name` | A human readable name that describes who owns the account |
| string | `image_url` | A url to retrieve an account image |
| string | `account_url` | A url for the organization/user of the COMP account |

#### GET: `/governance/history`

#### GovernanceHistoryRequest

The governance history API returns historical information about the Compound governance system.

#### GovernanceHistoryResponse

The governance history API response contains the values for votes delegate, total delegators, total delegatees, and proposals created.

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | If set and non-zero, indicates an error returning data. `NO_ERROR = 0; INTERNAL_ERROR = 1; INVALID_REQUEST = 2;` |
| string | `votes_delegated` | The number of votes delegated |
| uint32 | `token_holders` | The number of addresses with a COMP balance greater than 0 |
| uint32 | `voting_addresses` | The number of addresses that have votes greater than 0 |
| uint32 | `proposals_created` | The number of proposals created |
| string | `total_comp_allocated` | The number of COMP allocated to all markets, including COMP not yet transferred to users |

#### POST: `/governance/profile`

#### GovernanceProfileRequest

| Type | Key | Description |
|------|-----|-------------|
| string | `action` | Action to take on the profile, either "upsert" or "delete" |
| bytes | `address` | Address of the record to perform action on. |
| string | `display_name` | Name to display for the profile |
| string | `image_url` | Profile image for the profile |
| string | `account_url` | A link of the profile owner's choice |
| string | `key` | |

#### GovernanceProfileResponse

| Type | Key | Description |
|------|-----|-------------|
| Error | `error` | |
| GovernanceProfileRequest | `request` | |
| DisplayCompAccount | `profile` | |

#### DisplayCompAccount

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the given COMP account |
| string | `display_name` | A human readable name that describes who owns the account |
| string | `image_url` | A url to retrieve an account image |
| string | `account_url` | A url for the organization/user of the COMP account |

#### GET: `/governance/comp`

#### GovernanceCompDistributionRequest

The governance COMP distribution API returns COMP distribution information for markets in the Compound protocol.

| Type | Key | Description |
|------|-----|-------------|
| bytes | `addresses` | List of token addresses to filter on, e.g.: ["0x...", ,"0x..."] |

#### GovernanceCompDistributionResponse

The governance COMP distribution API response contains the values for COMP allocated, COMP borrow index, COMP distributed, COMP speed, and COMP supply index for each market.

| Type | Key | Description |
|------|-----|-------------|
| GovernanceCompDistributionRequest | `request` | The request parameters are echoed in the response. |
| string | `comp_rate` | The number of COMP allocated to all markets per block |
| string | `daily_comp` | The number of COMP allocated to all markets per day assuming a given block time |
| string | `total_comp_allocated` | The number of COMP allocated to all markets, including COMP not yet transferred to users |
| string | `total_comp_distributed` | The number of total COMP actually transferred to users |
| MarketCompDistribution | `markets` | A list of all cToken markets receiving COMP |

#### MarketCompDistribution

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the cToken market |
| string | `name` | The name of the cToken market |
| string | `symbol` | The symbol of the cToken market |
| bytes | `underlying_address` | The address of undelrying token of the cToken market |
| string | `underlying_name` | The name of the underlying token of the cToken market |
| string | `underlying_symbol` | The symbol of the underlying token of the cToken market |
| string | `supplier_daily_comp` | The projected daily comp distribution to suppliers of the market given the current distribution rate for the market |
| string | `borrower_daily_comp` | The projected daily comp distribution to borrowers of the market given the current distribution rate for the market |
| string | `comp_allocated` | The number of COMP allocated to the market, including COMP not yet transferred to borrowers/suppliers of the market |
| string | `comp_borrow_index` | The index used to calculate how much COMP an individual borrower should receive |
| string | `comp_distributed` | The number of COMP already transferred to the borrowers/suppliers of the market |
| string | `comp_speed` | The number of COMP allocated to the market each block |
| string | `comp_supply_index` | The index used to calculate how much COMP an individual supplier should receive |

#### GET: `/governance/comp/account`

#### GovernanceAccountCompDistributionRequest

The governance COMP account distribution API returns COMP distribution information across all markets for a given account

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The account address to use for the request |

#### GovernanceAccountCompDistributionResponse

The governance COMP account distribution API response contains the values for COMP allocated, COMP borrow index, COMP distributed, daily COMP, and COMP supply index for each market.

| Type | Key | Description |
|------|-----|-------------|
| GovernanceCompDistributionRequest | `request` | The request parameters are echoed in the response. |
| AccountCompDistribution | `markets` | A list of all cToken markets the account has been allocated COMP |

#### AccountCompDistribution

| Type | Key | Description |
|------|-----|-------------|
| bytes | `address` | The address of the cToken market |
| string | `name` | The name of the cToken market |
| string | `symbol` | The symbol of the cToken market |
| bytes | `underlying_address` | The address of undelrying token of the cToken market |
| string | `underlying_name` | The name of the underlying token of the cToken market |
| string | `underlying_symbol` | The symbol of the underlying token of the cToken market |
| string | `daily_comp` | The projected daily comp distribution to the account |
| string | `comp_allocated` | The number of COMP allocated to the account, including COMP not yet transferred to the account |
| string | `comp_borrow_index` | The index used to calculate how much COMP the account should receive based on it's borrows from the market |
| string | `comp_distributed` | The number of COMP already transferred to the the account |
| string | `comp_supply_index` | The index used to calculate how much COMP the account should receive based on it's supply to market |

#### GovernanceCompDistributionRequest

The governance COMP distribution API returns COMP distribution information for markets in the Compound protocol.

| Type | Key | Description |
|------|-----|-------------|
| bytes | `addresses` | List of token addresses to filter on, e.g.: ["0x...", ,"0x..."] (Optional) |

## Shared Data Types

Custom data types that are shared between services.

#### Pagination Summary

Used for paginating results.

| Type | Key | Description |
|------|-----|-------------|
| uint32 | `page_number` | The current page number |
| uint32 | `page_size` | The number of entries to show per page. |
| uint32 | `total_entries` | The number of items matching the request across all pages. |
| uint32 | `total_pages` | The number of pages need to show total_entries at the given page_size. |

#### Precise

For non-negative numbers only.

| Type | Key | Description |
|------|-----|-------------|
| string | `value` | The full UNSIGNED number in string form. max value is 2^257 - 1,aka 231584178474632390847141970017375815706539969331281128078915168015826259279871 |

