---
layout: docs-content
title: Compound II | Docs - Security
permalink: /v2/security/
docs_version: v2

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

01 Certora Verification Summary

## Economic Security

[Gauntlet](https://gauntlet.network/){:target="_blank"} has constructed a simulation-based market stress-testing platform to evaluate the economic security of the Compound protocol, as it scales supported assets and volume.

01 Gauntlet Market Risk Assessment

## Bug Bounty Program

Security is core to our values, and we value the input of hackers acting in good faith to help us maintain the highest standard for the security and safety of the Ethereum ecosystem. The Compound protocol, while it has gone through professional audits and formal verification, depends on new technology that may contain undiscovered vulnerabilities.

Compound encourages the community to audit our contracts and security; we also encourage the responsible disclosure of any issues. This program is intended to recognize the value of working with the community of independent security researchers, and sets out our definition of good faith in the context of finding and reporting vulnerabilities, as well as what you can expect from us in return.

#### Rewards

Compound offers substantial rewards for discoveries that can prevent the loss of assets, the freezing of assets, or harm to a user, commensurate with the severity and exploitability of the vulnerability. Compound will pay a reward of $500 to $150,000 for eligible discoveries according to the terms and conditions provided below.

#### Scope

The primary scope of the bug bounty program is for vulnerabilities affecting the on-chain Compound Protocol, deployed to the Ethereum Mainnet, for contract addresses listed in this developer documentation.

This list may change as new contracts are deployed, or as existing contracts are removed from usage. Vulnerabilities in contracts built on top of the Protocol by third-party developers (such as smart contract wallets) are not in-scope, nor are vulnerabilities that require ownership of an admin key.

The secondary scope of the bug bounty program is for vulnerabilities affecting the Compound Interface hosted at app.compound.finance that could conceivably result in exploitation of user accounts.

Finally, test contracts (Rinkeby and other testnets) and staging servers are out of scope, unless the discovered vulnerability also affects the Compound Protocol or Interface, or could otherwise be exploited in a way that risks user funds.

#### Disclosure

Submit all bug bounty disclosures to security@compound.finance. The disclosure must include clear and concise steps to reproduce the discovered vulnerability in either written or video format. Compound will follow up promptly with acknowledgement of the disclosure.

#### Terms and Conditions

To be eligible for bug bounty reward consideration, you must:

- Identify an original, previously unreported, non-public vulnerability within the scope of the Compound bug bounty program as described above.
- Include sufficient detail in your disclosure to enable our engineers to quickly reproduce, understand, and fix the vulnerability.
- Be at least 18 years of age.
- Be reporting in an individual capacity, or if employed by a company, reporting with the company’s written approval to submit a disclosure to Compound.
- Not be subject to US sanctions or reside in a US-embargoed country.
- Not be a current or former Compound employee, vendor, contractor, or employee of a Compound vendor or contractor.

To encourage vulnerability research and to avoid any confusion between good-faith hacking and malicious attack, we require that you:

- Play by the rules, including following the terms and conditions of this program and any other relevant agreements. If there is any inconsistency between this program and any other relevant agreements, the terms of this program will prevail.
- Report any vulnerability you’ve discovered promptly.
- Avoid violating the privacy of others, disrupting our systems, destroying data, or harming user experience.
- Use only security@compound.finance to discuss vulnerabilities with us.
- Keep the details of any discovered vulnerabilities confidential until they are fixed.
- Perform testing only on in-scope systems, and respect systems and activities which are out-of-scope.
- Only interact with accounts you own or with explicit permission from the account holder.
- Not engage in blackmail, extortion, or any other unlawful conduct.

When working with us according to this program, you can expect us to:

- Pay generous rewards for eligible discoveries based on the severity and exploitability of the discovery, at Compound’s sole discretion
- Extend Safe Harbor for your vulnerability research that is related to this program, meaning we will not threaten or bring any legal action against anyone who makes a good faith effort to comply with our bug bounty program.
- Work with you to understand and validate your report, including a timely initial response to the submission.
- Work to remediate discovered vulnerabilities in a timely manner.
- Recognize your contribution to improving our security if you are the first to report a unique vulnerability, and your report triggers a code or configuration change.

**All reward determinations, including eligibility and payment amount, are made at Compound’s sole discretion. Compound reserves the right to reject submissions and alter the terms and conditions of this program.**
