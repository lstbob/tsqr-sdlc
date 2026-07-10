---
title: "[Tech] Error handling and async patterns"
type: Tech
repo: tsqr-autheo
issue: https://github.com/lstbob/tsqr-autheo/issues/1
created: 2026-07-10
---

## Problem

Two runtime-affecting issues in Autheo.

### Inconsistent error handling strategy
Autheo uses a mixed approach: domain methods throw exceptions while application handlers return `Result<T>`:
- `User.Create()` throws `ArgumentException` when email is empty
- `RefreshToken.Rotate()` throws `InvalidOperationException` if token is inactive
- `PasswordResetToken.Verify()` throws on expiration

Application handlers use `Result<T>`, so these exceptions crash the request instead of returning a `ValidationError` to the client. This is the most dangerous error pattern in the codebase — a validation failure in `User.Create()` will return a 500 error to the client.

### Blocking async call in UserRepository
`UserRepository.Update()` uses `.GetAwaiter().GetResult()` — blocking the ASP.NET request thread:
```csharp
public void Update(User user)
{
    uow.Connection.ExecuteAsync(...).GetAwaiter().GetResult();
}
```
Under load this causes thread pool starvation — all threads blocked on I/O, new requests queue up, throughput collapses.

## Suggested Approach
1. Convert domain methods to return `Result<T>` instead of throwing; update callers to check `IsFailure`
2. Remove `.GetAwaiter().GetResult()` — either make `IRepository.Update` async (`Task UpdateAsync`) or use synchronous `db.Execute()`

## Affected Files
- `User.cs` (Create, etc.), `RefreshToken.cs` (Rotate), `PasswordResetToken.cs` (Verify)
- `UserRepository.cs:44-66`
- `IRepository.cs` interface definition
