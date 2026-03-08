---
layout: docs-content
title: Compound v2 Docs | Security
permalink: /v2/security/
docs_namespace: v2

## Element ID: In-page Heading
sidebar_nav_data:
  security: Security
  audits: Audits
  formal-verification: Formal Verification
  economic-security: Economic Security
  bug-bounty-program: Bug Bounty
---

# Security

## Introduction

The security of the Compound protocol is our highest priority; our development team, alongside third-party auditors and consultants, has invested considerable effort to create a protocol that we believe is safe and dependable. All contract code and balances are publicly verifiable, and security researchers are eligible for a bug bounty for reporting undiscovered vulnerabilities.

We believe that size, visibility, and time are the true test for the security of a smart contract; please exercise caution, and make your own determination of security and suitability.

## Audits

The Compound protocol has been reviewed & audited by [Trail of Bits](https://www.trailofbits.com/){:target="_blank"} and [OpenZeppelin](https://openzeppelin.com/){:target="_blank"}.

1. [Trail of Bits - April 2019](https://github.com/trailofbits/publications/blob/master/reviews/compound-2.pdf){:target="_blank"}
2. [OpenZeppelin - August 2019](https://blog.openzeppelin.com/compound-audit/){:target="_blank"}
3. [Trail of Bits - August 2019](https://github.com/trailofbits/publications/blob/master/reviews/compound-3.pdf){:target="_blank"}
4. [OpenZeppelin - Timelock & Pause Guardian](https://blog.openzeppelin.com/compound-finance-patch-audit){:target="_blank"}
5. [OpenZeppelin - cDAI](https://blog.openzeppelin.com/compound-finance-mcd-dsr-integration/){:target="_blank"}
6. [OpenZeppelin - COMP & Governance](https://blog.openzeppelin.com/compound-alpha-governance-system-audit/){:target="_blank"}
7. [Trail of Bits - February 2020](https://github.com/trailofbits/publications/blob/master/reviews/compound-governance.pdf){:target="_blank"}
8. [OpenZeppelin - Tether](https://blog.openzeppelin.com/compound-tether-integration-audit/){:target="_blank"}
9. [OpenZeppelin - COMP Distribution](https://blog.openzeppelin.com/compound-comp-distribution-system-audit/){:target="_blank"}
{: .mega-ordered-list }

## Formal Verification

The Compound protocol was developed with a specifications of security principles, and formally verified by [Certora](https://www.certora.com/){:target="_blank"} using Certora ASA (Accurate Static Analysis), which is integrated into Compound's continuous integration system.

1. [Certora Verification Summary](ttps://www.certora.com/wp-content/uploads/2022/02/CompoundMoneyMarketV2Aug2019.pdf){:target="_blank"}

## Economic Security

[Gauntlet](https://gauntlet.network/){:target="_blank"} has constructed a simulation-based market stress-testing platform to evaluate the economic security of the Compound protocol, as it scales supported assets and volume.

1. [Gauntlet Market Risk Assessment](https://gauntlet.network/reports/compound){:target="_blank"}

## Bug Bounty Program

Security is core to our values, and we value the input of hackers acting in good faith to help us maintain the highest standard for the security and safety of the Ethereum ecosystem. The Compound protocol, while it has gone through professional audits and formal verification, depends on new technology that may contain undiscovered vulnerabilities.

The Compound protocol bug bounty program is run entirely by the community with collaboration from Immunefi.

[Bug Bounty Dashboard](https://immunefi.com/bug-bounty/compoundfinance/information/)

