# Time-Value-of-Money Equations

Reference for the equations a TI-89 TVM toolkit will evaluate. Conventions match
the TI financial calculators (BA II Plus, TI-83/84 TVM Solver, TI-89 Finance app)
so results can be cross-checked against them.

---

## 1. Variables

| Symbol | Meaning | Notes |
|---|---|---|
| `n`   | Number of periods | Need not be an integer when solved for |
| `i`   | Interest rate per period, as a decimal | e.g. `0.005` = 0.5 % per period; see §2 |
| `p`   | Present value | Cash flow at time 0 |
| `f`   | Future value | Cash flow at time `n` |
| `PMT` | Periodic payment | Level, one per period |
| `k`   | Payment timing | `0` = END (ordinary annuity), `1` = BEGIN (annuity due) |
| `I/Y` | Nominal annual interest rate, in percent | Only needed to derive `i` |
| `P/Y` | Payments per year | Default 1 |
| `C/Y` | Compounding periods per year | Default = `P/Y` |

### Sign convention

Cash **received** is positive, cash **paid out** is negative. A loan you take out
has `p > 0` and `PMT < 0`; a deposit has `p < 0` and `f > 0`. If every input has
the same sign there is no solution (nothing balances the cash flows).

---

## 2. Periodic rate

Convert the nominal annual rate to a rate per payment period:

```
              ⎛     I/Y     ⎞ (C/Y ÷ P/Y)
(2.1)   i  =  ⎜1 + ───────── ⎟              − 1
              ⎝    100·C/Y   ⎠
```

When `C/Y = P/Y` (the common case) this reduces to

```
(2.2)   i  =  I/Y ÷ (100·P/Y)
```

Inverse, used after solving for `i`:

```
(2.3)   I/Y  =  100·C/Y · [ (1 + i)^(P/Y ÷ C/Y) − 1 ]
```

---

## 3. The master TVM equation

Every TVM problem is one equation in five unknowns (`n`, `i`, `p`, `PMT`, `f`):
the cash flows, all moved to time `n`, must sum to zero.

```
(3.1)   p·(1+i)^n  +  PMT·(1+i·k)·[(1+i)^n − 1] / i  +  f  =  0        (i ≠ 0)

(3.2)   p  +  PMT·n  +  f  =  0                                       (i = 0)
```

Equivalent present-value form (divide 3.1 by `(1+i)^n`):

```
(3.3)   p  +  PMT·(1+i·k)·[1 − (1+i)^−n] / i  +  f·(1+i)^−n  =  0
```

The factor `(1+i·k)` is the only difference between END and BEGIN mode: in BEGIN
mode each payment earns one extra period of interest.

Shorthand used below:

```
G  = (1+i)^n                    growth factor
Q  = PMT·(1+i·k) / i            annuity constant
```

so (3.1) is simply `p·G + Q·(G − 1) + f = 0`.

---

## 4. Solving for each variable

### 4.1 Future value

```
(4.1)   f  =  −[ p·G + Q·(G − 1) ]                  (i ≠ 0)
        f  =  −( p + PMT·n )                        (i = 0)
```

### 4.2 Present value

```
(4.2)   p  =  −[ f + Q·(G − 1) ] / G                (i ≠ 0)
        p  =  −( f + PMT·n )                        (i = 0)
```

### 4.3 Payment

```
                     i · (p·G + f)
(4.3)   PMT  =  − ─────────────────────             (i ≠ 0)
                   (1 + i·k) · (G − 1)

        PMT  =  −( p + f ) / n                      (i = 0)
```

### 4.4 Number of periods

From `p·G + Q·(G − 1) + f = 0` → `G·(p + Q) = Q − f`:

```
              ln[ (Q − f) / (Q + p) ]
(4.4)   n  =  ───────────────────────               (i ≠ 0)
                    ln(1 + i)

        n  =  −( p + f ) / PMT                      (i = 0)
```

No solution if the log argument is ≤ 0 (the payment can never pay off the
balance, or signs are inconsistent).

### 4.5 Interest rate

There is **no closed form** for `i` in general — it must be found numerically.

*Special case, `PMT = 0`* (single lump sum):

```
(4.5)   i  =  ( −f / p )^(1/n) − 1
```

*General case* — find the root of the residual

```
(4.6)   R(i)  =  p·G  +  PMT·(1+i·k)·(G − 1)/i  +  f
```

with Newton's method, `i ← i − R(i) / R′(i)`, where

```
(4.7)   R′(i)  =  n·p·(1+i)^(n−1)
               +  PMT · [ k·(G − 1)/i
                         + (1+i·k) · ( n·i·(1+i)^(n−1) − (G − 1) ) / i² ]
```

Practical notes:

- Valid roots satisfy `i > −1`.
- A fixed starting guess such as `i₀ = 0.01` converges for ordinary loan and
  savings problems; add a guard that halves the step if it would land at or
  below `−1`. Stop when `|Δi| < 1e−12` or after ~50 iterations.
- Near `i = 0`, `(G−1)/i` loses precision; switch to (3.2) when `|i| < 1e−10`.
- More than one sign change in the cash flows can produce multiple roots.
- On the TI-89, `nSolve(R(i)=0, i)` (or `solve`) is an alternative to hand-coded
  Newton iteration.

Convert the result back to an annual rate with (2.3).

---

## 5. Amortization

Let `B_j` be the outstanding balance **immediately after payment j**, with `B₀ = p`.
It carries the same sign as `p`.

### 5.1 Balance after j payments

```
(5.1)   B_j  =  p·(1+i)^(j−k)  +  PMT·[ (1+i)^j − 1 ] / i      (i ≠ 0)
        B_j  =  p + j·PMT                                      (i = 0)
```

In END mode `B_n = −f`. In BEGIN mode payment `j` happens at time `j−1`, so
`B_n` is the balance one period before the end, and `B_n·(1+i) = −f`.

### 5.2 Interest and principal in payment j

```
(5.2)   INT_j  =  −i · B_{j−1}              (END, or BEGIN with j ≥ 2)
        INT_1  =  0                         (BEGIN mode only)

(5.3)   PRN_j  =  PMT − INT_j
```

`INT` and `PRN` carry the sign of `PMT`, and `B_j = B_{j−1} + PRN_j`.

### 5.3 Totals over payments j₁ … j₂

```
(5.4)   ΣPrn(j₁, j₂)  =  B_{j₂} − B_{j₁−1}

(5.5)   ΣInt(j₁, j₂)  =  (j₂ − j₁ + 1)·PMT − ΣPrn(j₁, j₂)
```

Note: real loans round `PMT` to cents, so the last payment usually differs
slightly. Amortization functions should take the (possibly rounded) `PMT` as an
input rather than recomputing it.

---

## 6. Interest-rate conversions

With `C` = compounding periods per year, rates in percent:

```
(6.1)   EFF  =  100 · [ (1 + NOM/(100·C))^C − 1 ]          nominal → effective

(6.2)   NOM  =  100 · C · [ (1 + EFF/100)^(1/C) − 1 ]      effective → nominal

(6.3)   EFF  =  100 · ( e^(NOM/100) − 1 )                  continuous compounding

(6.4)   NOM  =  100 · ln(1 + EFF/100)                      continuous, inverse
```

---

## 7. Uneven cash flows

For cash flows `CF₀, CF₁, …, CFₙ` at the end of periods `0 … n`:

```
                     n      CFⱼ
(7.1)   NPV(i)  =    Σ   ─────────
                    j=0  (1 + i)^j

(7.2)   IRR  =  the i for which NPV(i) = 0          (numerical, as in §4.5)

                     n
(7.3)   NPV′(i)  =  −Σ  j·CFⱼ / (1 + i)^(j+1)       (Newton derivative)
                    j=1
```

If a cash flow repeats `fⱼ` times (as on the TI cash-flow worksheets), expand it
into that many consecutive entries.

---

## 8. Useful special cases

```
(8.1)   Present value of a future value     p  =  f · (1+i)^−n        (timing-independent; see note)
(8.2)   PV of a perpetuity                  p  =  PMT / i
(8.3)   PV of a perpetuity due              p  =  PMT·(1+i) / i
(8.4)   PV of a growing annuity             p  =  PMT / (i − g) · [ 1 − ((1+g)/(1+i))^n ]     (i ≠ g)
                                            p  =  PMT · n / (1+i)                            (i = g)
(8.5)   Continuous compounding, lump        f  =  p · e^(r·t)
(8.6)   Rule of 72 (doubling estimate)      n  ≈  72 / I
```

(These return magnitudes; apply the sign convention as needed — e.g. (8.1)
becomes `p = −f·(1+i)^−n` under §1. Payment timing `k` only multiplies `PMT`,
so it has no effect on a single lump sum.)

---

## 9. Proposed TI-89 function set

| Function | Solves | Equation |
|---|---|---|
| `pf(f,i,n)` ✅ | p from a lump-sum f (magnitude, no sign flip) | 8.1 — [src/pf.txt](src/pf.txt) |
| `fp(p,i,n)` ✅ | f from a lump-sum p (magnitude, no sign flip) | inverse of 8.1 — [src/fp.txt](src/fp.txt) |
| `pa(a,i,n)` ✅ | p of an END annuity a (magnitude) | 4.2 with f=0, k=0 — [src/pa.txt](src/pa.txt) |
| `ap(p,i,n)` ✅ | END annuity a that repays p (magnitude) | 4.3 with f=0, k=0 — [src/ap.txt](src/ap.txt) |
| `fa(a,i,n)` ✅ | f of an END annuity a (magnitude) | 4.1 with p=0, k=0 — [src/fa.txt](src/fa.txt) |
| `af(f,i,n)` ✅ | END annuity a that accumulates to f (magnitude) | 4.3 with p=0, k=0 — [src/af.txt](src/af.txt) |
| `tvmfv(n,iy,p,pmt,py,cy,k)`   | f   | 4.1 |
| `tvmpv(n,iy,pmt,f,py,cy,k)`   | p   | 4.2 |
| `tvmpmt(n,iy,p,f,py,cy,k)`    | PMT | 4.3 |
| `tvmn(iy,p,pmt,f,py,cy,k)`    | n   | 4.4 |
| `tvmiy(n,p,pmt,f,py,cy,k)`    | I/Y | 4.5–4.7, 2.3 |
| `tvmbal(j,n,iy,p,pmt,py,cy,k)` | Balance after j | 5.1 |
| `tvmint(j1,j2,…)` / `tvmprn(j1,j2,…)` | ΣInt / ΣPrn | 5.4–5.5 |
| `toeff(nom,c)` / `tonom(eff,c)` | Rate conversion | 6.1–6.2 |
| `npv(i,list)` / `irr(list)` | Uneven cash flows | 7.1–7.3 |

TI-89 constraints worth designing around:

- A `Func` returns one value and cannot store to global variables; a `Prgm` can
  but returns nothing. A "solver screen" that fills in the missing variable would
  be a `Prgm`; the per-variable solvers above are `Func`s.
- Function names are limited to 8 characters.
- Arguments are positional only — consider a shared helper `tvmi(iy,py,cy)` for
  (2.1) so every function converts rates identically.
- Lists (`{…}`) are the natural input for cash-flow functions.
