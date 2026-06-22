---
name: ftg-match
description: Match a paper or research topic to Finance Theory Group (FTG) members with relevant expertise. Use when the user needs to find a discussant, referee, or collaborator from the FTG membership for a specific paper or research area.
allowed-tools: Read WebFetch WebSearch Grep Agent
---

# FTG Member Matching Skill

Match a paper or research topic to Finance Theory Group (FTG) members with relevant expertise.

## Input

The user will provide one of:
- A paper title, abstract, or PDF path
- A research topic or set of keywords
- A description of the expertise needed

Optional constraints:
- Exclude specific people (e.g., coauthors, colleagues)
- Seniority preference (junior, mid-career, senior)
- Geographic preference (international, US-based)
- Must be in a finance department (not accounting/economics)

## Process

1. **Read the FTG member list** from the project directory or from the canonical location. The full FTG membership (288 members as of April 2026) is stored at:
   - Primary: `ftg_members.md` in the current project directory
   - If not found, fetch from https://www.financetheory.org/members (note: the site uses dynamic loading, paginate with `?page=N` for N=1..6)

2. **Identify the paper's key theoretical themes.** Extract:
   - Core model type (e.g., Kyle, Grossman-Stiglitz, general equilibrium, mechanism design)
   - Economic mechanisms (e.g., disagreement, information acquisition, moral hazard, adverse selection)
   - Market setting (e.g., equity, debt, derivatives, lending, OTC)
   - Policy relevance (e.g., disclosure regulation, short-selling bans, capital requirements)

3. **Search for matching FTG members.** For each candidate:
   - Search the web for their research page / Google Scholar / SSRN
   - Check if their published work overlaps with the paper's themes
   - Verify their current department and rank
   - Note any JF/RFS/JFE publications
   - Check if they are cited in or acknowledged by the paper (if a PDF is provided)

4. **Rank candidates** by:
   - Direct topical overlap (most important)
   - Methodological fit (same modeling tradition)
   - Availability likelihood (mid-career > very senior)
   - Diversity value (international, institutional variety)

5. **Check for conflicts.** Flag if a candidate is:
   - A coauthor of a paper author
   - Acknowledged in the paper
   - At the same institution as the person requesting the match
   - Already committed to another role at the same conference

## Output

Present a ranked table with 5-7 candidates:

| Rank | Name | Affiliation | Rank/Seniority | Key paper(s) | Fit rationale |
|------|------|------------|----------------|--------------|---------------|

Then provide a brief recommendation of the top 1-2 picks with reasoning.

## Notes

- FTG members are finance theorists by definition, so the "finance department" constraint is usually satisfied, but always verify.
- The FTG list may become stale. If the stored list is more than 1 year old, re-fetch from the website.
- Some FTG members are at central banks or policy institutions (e.g., Fed, ECB) — flag any constraints on public commentary.
- WashU Olin colleagues of Brett Green should be flagged (but not automatically excluded).
