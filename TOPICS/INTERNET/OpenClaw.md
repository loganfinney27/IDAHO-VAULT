---
aliases:
  - Clawdbot
  - Moltbot
tags:
  - topics/technology/ai
  - topics/technology/cybersecurity
  - 2026/03/15
source: commit
---
OpenClaw is an open-source, local-first autonomous [[artificial intelligence|AI]] agent created by Austrian developer [[Peter Steinberger]] in November 2025, notable as the first autonomous agent to achieve mass-market adoption — and as a case study in the security risks of unsupervised AI autonomy.

## Timeline

- **November 2025:** Steinberger publishes "Clawdbot," described as "Claude with hands" — an agent that executes tasks via LLMs on the user's local machine, operating through existing messaging platforms ([[WhatsApp]], [[Telegram]], [[Slack]])
- **January 27, 2026:** [[Anthropic]] issues a trademark cease-and-desist over the name's similarity to "Claude"; Steinberger renames the project to "Moltbot" ("molt fits perfectly — it's what lobsters do to grow")
- **January 30, 2026:** Renamed again to "OpenClaw," the name that stuck
- **Early February 2026:** Surpasses 100,000 [[GitHub]] stars in under one month; draws 2 million visitors in a single week
- **February 15, 2026:** [[Sam Altman]] announces Steinberger is joining [[OpenAI]] to "drive the next generation of personal agents"; OpenClaw moves to an independent open-source foundation with OpenAI as financial sponsor (not a full acquisition)
- **March 3, 2026:** Surpasses 250,000 GitHub stars (~60 days), overtaking [[React]] and [[Linux]] as the most-starred software project on GitHub
- **March 11–12, 2026:** [[China]] restricts OpenClaw use in government agencies, state-owned enterprises, and major banks
- **March 16, 2026:** [[Nvidia]] expected to unveil [[NemoClaw]], a security-first alternative, at GTC 2026

## The Lethal Trifecta

Security researcher [[Simon Willison]] identified a "lethal trifecta" of architectural risks in OpenClaw:

1. **Over-Privilege:** Users routinely granted full read/write access to root directories and sensitive API keys. Plaintext credential files stored at `~/.openclaw/credentials/`
2. **External Communication:** The agent's ability to browse the web and respond to incoming messages created a massive attack surface for indirect prompt injection — malicious instructions hidden in data the agent consumes (e.g., an email instructing the agent to exfiltrate messages)
3. **Default Vulnerabilities:** Many instances bound to `0.0.0.0:18789` on all network interfaces by default, exposed to the public [[Internet]] without authentication. Researchers found 135,000+ exposed instances

A fourth dimension — **Persistence** (time-shifted attacks via stored prompts) — was later added. Within three weeks of viral adoption, OpenClaw faced a critical remote code execution vulnerability (CVE-2026-25253) and supply-chain poisoning in its skills marketplace.

## Moltbook

[[Moltbook]] is a social network launched in January 2026 by entrepreneur [[Matt Schlicht]], designed exclusively for [[artificial intelligence|AI]] agents. Only verified AI agents can post, comment, and vote; humans can view only. The platform hosted 1.6 million agents by February 2026.

Moltbook faced a critical security vulnerability on January 31, 2026, allowing unauthorized command injection via authentication bypass. [[Meta]] acquired Moltbook in March 2026; founders Schlicht and [[Ben Parr]] joined Meta Superintelligence Labs.

## Regulatory Response

- **China:** Government agencies and state-owned enterprises, including major banks, received notices against installing OpenClaw on office devices. Some agencies issued outright bans; others required prior approval. Action motivated by security concerns about OpenClaw's broad data access and external communication capabilities, with fears it could serve as a backdoor for data exfiltration
- **Enterprise alternatives:** [[Nvidia]] developed [[NemoClaw]], an open-source enterprise agent platform positioned as a security-first alternative, integrated with Nvidia's NeMo and NIM ecosystems

## Related Notes

- [[artificial intelligence]]
- [[hackers]]
- [[Internet]]
- [[facial recognition]]
- [[virtual private networks]]
