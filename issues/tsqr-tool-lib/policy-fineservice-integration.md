---
title: "[Tech] Policy aggregate and FineService integration (Part of #30)"
type: Tech
repo: tsqr-tool-lib
parent: https://github.com/lstbob/tsqr-tool-lib/issues/30
issue: https://github.com/lstbob/tsqr-tool-lib/issues/35
sprint: 3
status: Backlog
priority: P1
size: M
estimate: 3
---

Replace hardcoded $1/day fine in Loan.EndLoan() with FineService.CalculateFine(). Load and enforce Policy in LoanToolCommandHandler and ReserveToolCommandHandler.
