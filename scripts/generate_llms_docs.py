#!/usr/bin/env python3

from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import ParseResult, urljoin, urlparse, urlunparse

import yaml

SITE_ORIGIN = "https://docs.compound.finance"
ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "docs"
PAGES_ROOT = DOCS_ROOT / "pages"
SAME_SITE_HOST = urlparse(SITE_ORIGIN).netloc

DOCS = [
    {
        "source": "v3/compound-3.md",
        "section": "Compound III",
        "name": "Compound III overview",
        "description": "Overview of the current protocol, deployment addresses, core contracts, developer resources, and security references.",
        "core": True,
    },
    {
        "source": "v3/interest-rates.md",
        "section": "Compound III",
        "name": "Interest rates",
        "description": "Supply and borrow rate models, utilization, kink behavior, and APR conversion.",
        "core": True,
    },
    {
        "source": "v3/collateral-and-borrowing.md",
        "section": "Compound III",
        "name": "Collateral and borrowing",
        "description": "Supplying collateral, borrowing the base asset, withdraw rules, and collateral limits.",
        "core": True,
    },
    {
        "source": "v3/liquidation.md",
        "section": "Compound III",
        "name": "Liquidation",
        "description": "Liquidation factors, discounts, absorbing underwater accounts, and reserve usage.",
        "core": True,
    },
    {
        "source": "v3/account-management.md",
        "section": "Compound III",
        "name": "Account management",
        "description": "Delegated account managers, permissions, and EIP-712 allowance flows.",
        "core": True,
    },
    {
        "source": "v3/protocol-rewards.md",
        "section": "Compound III",
        "name": "Protocol rewards",
        "description": "Reward accrual, claiming flows, and reward configuration behavior.",
        "core": True,
    },
    {
        "source": "v3/governance.md",
        "section": "Compound III",
        "name": "Governance",
        "description": "Governance model, proposal flow, voting, and admin roles for Compound III.",
        "core": True,
    },
    {
        "source": "v3/helper-functions.md",
        "section": "Compound III",
        "name": "Helper functions",
        "description": "Read-only contract helpers for assets, prices, reserves, utilization, and market state.",
        "core": True,
    },
    {
        "source": "v2/getting-started.md",
        "section": "Compound v2",
        "name": "Getting started",
        "description": "Compound v2 overview, guides, network deployments, and protocol math.",
        "core": False,
    },
    {
        "source": "v2/ctokens.md",
        "section": "Compound v2",
        "name": "cTokens",
        "description": "cToken contract methods, events, errors, exchange rates, and FAQs.",
        "core": False,
    },
    {
        "source": "v2/comptroller.md",
        "section": "Compound v2",
        "name": "Comptroller",
        "description": "Risk management, market entry, liquidity, liquidation math, and admin views.",
        "core": False,
    },
    {
        "source": "v2/governance.md",
        "section": "Compound v2",
        "name": "Governance",
        "description": "COMP delegation, proposals, voting, timelock, and pause guardian mechanics.",
        "core": False,
    },
    {
        "source": "v2/prices.md",
        "section": "Compound v2",
        "name": "Price feed",
        "description": "Oracle architecture, deployed price feed addresses, and price normalization behavior.",
        "core": False,
    },
    {
        "source": "v2/security.md",
        "section": "Compound v2",
        "name": "Security",
        "description": "Audits, bug bounty details, formal verification, and economic security references.",
        "core": False,
    },
    {
        "source": "compound-js/compound-js.md",
        "section": "Compound.js",
        "name": "Compound.js overview",
        "description": "SDK overview, installation, provider setup, and common usage patterns.",
        "core": False,
    },
    {
        "source": "compound-js/comet.md",
        "section": "Compound.js",
        "name": "Comet SDK",
        "description": "Compound III SDK methods for Comet markets, supported deployments, and helpers.",
        "core": False,
    },
    {
        "source": "compound-js/governance.md",
        "section": "Compound.js",
        "name": "Governance SDK",
        "description": "SDK methods for governance reads, delegation, voting, and proposal actions.",
        "core": False,
    },
    {
        "source": "compound-js/ctokens.md",
        "section": "Compound.js",
        "name": "cTokens SDK",
        "description": "SDK methods for Compound v2 cToken interactions.",
        "core": False,
    },
    {
        "source": "compound-js/comptroller.md",
        "section": "Compound.js",
        "name": "Comptroller SDK",
        "description": "SDK methods for Compound v2 Comptroller interactions.",
        "core": False,
    },
    {
        "source": "compound-js/price-feed.md",
        "section": "Compound.js",
        "name": "Price feed SDK",
        "description": "SDK methods for Compound v2 price feed reads.",
        "core": False,
    },
    {
        "source": "compound-js/helpers.md",
        "section": "Compound.js",
        "name": "Helpers SDK",
        "description": "Utility helpers for the SDK and general EVM development tasks.",
        "core": False,
    },
]

ASSET_EXTENSIONS = {
    ".json",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".js",
    ".css",
    ".pdf",
}


def parse_page(path: Path) -> tuple[dict, str]:
    content = path.read_text()
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"Missing front matter in {path}")

    front_matter = yaml.safe_load(match.group(1)) or {}
    body = content[match.end() :]
    return front_matter, body


def markdown_target_for(permalink: str) -> Path:
    clean = permalink.strip("/")
    if not clean:
        return DOCS_ROOT / "index.html.md"
    if os.path.splitext(clean)[1]:
        return DOCS_ROOT / f"{clean}.md"
    return DOCS_ROOT / clean / "index.html.md"


def docs_markdown_url_for(permalink: str) -> str:
    clean = permalink.strip("/")
    if not clean:
        return f"{SITE_ORIGIN}/index.html.md"
    if os.path.splitext(clean)[1]:
        return f"{SITE_ORIGIN}/{clean}.md"
    return f"{SITE_ORIGIN}/{clean}/index.html.md"


def canonical_permalink(path: str) -> str | None:
    clean_path = path or "/"
    if clean_path == "/index.html":
        return "/"
    if clean_path.endswith("/index.html"):
        return clean_path[: -len("index.html")]
    if os.path.splitext(clean_path)[1]:
        return clean_path
    if clean_path == "/":
        return "/"
    return f"{clean_path.rstrip('/')}/"


def markdown_path_for_permalink(permalink: str) -> str:
    clean = permalink.strip("/")
    if not clean:
        return "/index.html.md"
    if os.path.splitext(clean)[1]:
        return f"/{clean}.md"
    return f"/{clean}/index.html.md"


def rewrite_markdown_links(text: str, current_permalink: str, known_permalinks: set[str]) -> str:
    def replace_link(match: re.Match[str]) -> str:
        label = match.group(1)
        target = match.group(2)
        parsed = urlparse(target)

        if parsed.scheme and not (parsed.scheme in {"http", "https"} and parsed.netloc == SAME_SITE_HOST):
            return f"[{label}]({target})"

        base_url = urljoin(SITE_ORIGIN, current_permalink)
        resolved = urlparse(urljoin(base_url, target if not parsed.scheme else parsed.path or "/"))
        permalink = canonical_permalink(resolved.path)
        if not permalink or permalink not in known_permalinks:
            return f"[{label}]({target})"

        markdown_path = markdown_path_for_permalink(permalink)
        query = parsed.query or resolved.query
        fragment = parsed.fragment or resolved.fragment

        if parsed.scheme in {"http", "https"} and parsed.netloc == SAME_SITE_HOST:
            rebuilt = ParseResult(
                scheme=parsed.scheme,
                netloc=parsed.netloc,
                path=markdown_path,
                params="",
                query=query,
                fragment=fragment,
            )
            rewritten_target = urlunparse(rebuilt)
        else:
            rewritten_target = markdown_path
            if query:
                rewritten_target += f"?{query}"
            if fragment:
                rewritten_target += f"#{fragment}"

        return f"[{label}]({rewritten_target})"

    return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", replace_link, text)


def ctoken_faq_markdown() -> str:
    return """### cToken FAQ

#### How do cTokens earn interest?

Each [market](https://app.compound.finance/markets/?market=v2) has its own supply APR. Interest is not distributed as separate tokens. Instead, cTokens accrue value through their exchange rate, so each cToken becomes redeemable for more of the underlying asset over time even if the wallet balance of cTokens stays the same.

#### Do I need to calculate the cToken exchange rate?

When a market launches, the cToken exchange rate starts at a fixed initial value and rises with the market interest rate. Every user sees the same exchange rate, so there is no wallet-specific exchange rate to track.

#### Can you walk me through an example?

If you supply 1,000 DAI when the exchange rate is 0.020070, you receive about 49,825.61 cDAI. If the exchange rate later rises to 0.021591, those cDAI become redeemable for about 1,075.78 DAI. You can redeem the full balance or redeem only part of the underlying and keep the remaining cDAI.

#### How do I view my cTokens?

cTokens are visible on [Etherscan](https://etherscan.io/tokens/label/compound). Wallet support varies, but Coinbase Wallet and MetaMask have supported displaying cToken balances.

#### Can I transfer cTokens?

Yes, but transferring cTokens transfers the claim on the underlying supplied asset inside Compound. A transfer fails if the sender has entered that market as collateral and the transfer would leave the account with insufficient liquidity.
"""


def flatten_html_block(text: str) -> str:
    return re.sub(r"</?[^>]+>", "", text).strip()


def render_deployments(deployments: dict | None) -> str:
    if not deployments:
        return ""

    lines: list[str] = []
    for network_name, network_data in deployments.items():
        blockscan_origin = network_data.get("blockscan_origin")
        contracts = network_data.get("contracts", {})
        protocol_contracts = {name: value for name, value in contracts.items() if isinstance(value, str)}
        asset_contracts = {name: value for name, value in contracts.items() if isinstance(value, dict)}

        lines.append(f"### {network_name}")
        lines.append("")
        if blockscan_origin:
            lines.append(f"Block explorer: {blockscan_origin}")
            lines.append("")

        if protocol_contracts:
            lines.append("#### Protocol contracts")
            lines.append("")
            for contract_name, address in protocol_contracts.items():
                lines.append(f"- {contract_name}: `{address}`")
            lines.append("")

        if asset_contracts:
            lines.append("#### Asset configuration")
            lines.append("")
            for asset_name, values in asset_contracts.items():
                lines.append(f"##### {asset_name}")
                lines.append("")
                for metric_name, metric_value in values.items():
                    lines.append(f"- {metric_name}: `{metric_value}`")
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def sanitize_non_code_line(line: str, current_permalink: str, known_permalinks: set[str]) -> str:
    line = re.sub(r"\s*\{:[^}]+\}", "", line)
    line = rewrite_markdown_links(line, current_permalink, known_permalinks)
    return line.rstrip()


def sanitize_body(body: str, front_matter: dict, known_permalinks: set[str]) -> str:
    cleaned = body
    cleaned = re.sub(r'<div class="new-docs-banner">.*?</div>\s*</div>', "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(
        r'<div class="ctoken-faq">\s*\{% include ctoken-faq\.html %\}\s*</div>',
        ctoken_faq_markdown().strip(),
        cleaned,
        flags=re.DOTALL,
    )
    cleaned = cleaned.replace('<div id="networks-widget-container"></div>', render_deployments(front_matter.get("deployments")).rstrip())
    cleaned = re.sub(
        r'<div class="notice">\s*(.*?)\s*</div>',
        lambda match: f"> Note: {flatten_html_block(match.group(1))}",
        cleaned,
        flags=re.DOTALL,
    )
    cleaned = re.sub(
        r'<div class="warning">\s*(.*?)\s*</div>',
        lambda match: f"> Warning: {flatten_html_block(match.group(1))}",
        cleaned,
        flags=re.DOTALL,
    )
    cleaned = re.sub(r"<br\s*/?>", "\n", cleaned)

    lines = []
    in_code_fence = False
    for raw_line in cleaned.splitlines():
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):
            lines.append(line.rstrip())
            in_code_fence = not in_code_fence
            continue

        if in_code_fence:
            lines.append(line.rstrip())
            continue

        line = sanitize_non_code_line(line, front_matter["permalink"], known_permalinks)
        if not line.strip() and stripped.startswith("{:"):
            continue
        lines.append(line)

    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return f"{cleaned}\n"


def llms_txt(entries: list[dict]) -> str:
    sections: dict[str, list[dict]] = {}
    for entry in entries:
        sections.setdefault(entry["section"], []).append(entry)

    lines = [
        "# Compound Protocol Documentation",
        "",
        "> LLM-friendly guide to the Compound docs site covering Compound III, Compound v2, and Compound.js.",
        "",
        "These docs are published at https://docs.compound.finance/. Every documentation page listed below also has a clean Markdown mirror at the same route with `.md` appended, such as `/interest-rates/index.html.md`.",
        "",
        "Prefer the Compound III section for current integrations. Use the Compound v2 and Compound.js sections for legacy protocol behavior and SDK helpers.",
        "",
        "## Quick Start",
        "",
        f"- [Compound III context pack]({SITE_ORIGIN}/llms-ctx.txt): Expanded Markdown context for the current Compound III docs.",
        f"- [Complete docs context pack]({SITE_ORIGIN}/llms-ctx-full.txt): Expanded Markdown context for all public docs pages.",
        "",
    ]

    for section_name in ["Compound III", "Compound v2", "Compound.js"]:
        lines.append(f"## {section_name}")
        lines.append("")
        for entry in sections.get(section_name, []):
            lines.append(f"- [{entry['name']}]({entry['url']}): {entry['description']}")
        lines.append("")

    lines.extend(
        [
            "## Optional",
            "",
            f"- [Comet interface ABI]({SITE_ORIGIN}/public/files/comet-interface-abi-98f438b.json): Machine-readable ABI for Compound III integrations.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def context_pack(title: str, summary: str, entries: list[dict]) -> str:
    lines = [
        f"# {title}",
        "",
        f"> {summary}",
        "",
        f"Source manifest: {SITE_ORIGIN}/llms.txt",
        "",
    ]

    for entry in entries:
        lines.extend(
            [
                f"## {entry['name']}",
                "",
                f"Source URL: {entry['url']}",
                "",
                entry["mirror_content"].rstrip(),
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    raw_entries: list[dict] = []
    for doc in DOCS:
        page_path = PAGES_ROOT / doc["source"]
        front_matter, body = parse_page(page_path)
        raw_entries.append(
            {
                **doc,
                "front_matter": front_matter,
                "body": body,
            }
        )

    known_permalinks = {entry["front_matter"]["permalink"] for entry in raw_entries}
    entries: list[dict] = []
    for entry in raw_entries:
        permalink = entry["front_matter"]["permalink"]
        mirror_content = sanitize_body(entry["body"], entry["front_matter"], known_permalinks)
        entries.append(
            {
                **entry,
                "permalink": permalink,
                "target_path": markdown_target_for(permalink),
                "url": docs_markdown_url_for(permalink),
                "mirror_content": mirror_content,
            }
        )

    generated_targets = {entry["target_path"] for entry in entries}
    generated_targets |= {
        DOCS_ROOT / "llms.txt",
        DOCS_ROOT / "llms-ctx.txt",
        DOCS_ROOT / "llms-ctx-full.txt",
    }

    for path in DOCS_ROOT.rglob("index.html.md"):
        if "/pages/" in path.as_posix():
            continue
        if path not in generated_targets:
            path.unlink()

    for entry in entries:
        entry["target_path"].parent.mkdir(parents=True, exist_ok=True)
        entry["target_path"].write_text(entry["mirror_content"])

    (DOCS_ROOT / "llms.txt").write_text(llms_txt(entries))
    (DOCS_ROOT / "llms-ctx.txt").write_text(
        context_pack(
            "Compound III Context Pack",
            "Expanded Markdown context for the current Compound III docs listed in /llms.txt.",
            [entry for entry in entries if entry["core"]],
        )
    )
    (DOCS_ROOT / "llms-ctx-full.txt").write_text(
        context_pack(
            "Compound Protocol Full Context Pack",
            "Expanded Markdown context for all public docs pages listed in /llms.txt.",
            entries,
        )
    )


if __name__ == "__main__":
    main()
