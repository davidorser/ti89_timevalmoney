# TI-89 Time-Value-of-Money Functions

Six engineering-economics factor functions for the TI-89, built in one
conversation with Claude Code and tested on a real calculator.

## Backstory
In Oct. 2026, my aged TI-85 calculator died.  Taking with it a multitude of
programs I had written going back before I graduated undergrad in the year 
2000. After receiving my new TI-89 "Titanium" replacement calculator, I set
out with ClaudeAI to recreate the single most useful of those functions. The
Time-Value-of-Money (TVM) functions I first learned and programmed in 
Engineering Economics class in the year 1999.

## The Story
**[Read the project story → TI89_TVM_Project.html](TI89_TVM_Project.html)**: a
single self-contained page covering how the project was built, the formulas, the
.89f file format, and download links for every function. Download it and open it
in any browser; it works offline.

## Functions

All functions assume payments at the end of each period. `i` is the rate per
period as a decimal and `n` is the number of periods.

| Function | Finds | Formula |
|---|---|---|
| `pf(f,i,n)` | Present value of a future amount | `f/(1+i)^n` |
| `fp(p,i,n)` | Future value of a present amount | `p·(1+i)^n` |
| `pa(a,i,n)` | Present value of a series of payments | `a·(1−1/(1+i)^n)/i` |
| `ap(p,i,n)` | Payment that pays off a present amount | `p·i/(1−1/(1+i)^n)` |
| `fa(a,i,n)` | Future value of a series of payments | `a·((1+i)^n−1)/i` |
| `af(f,i,n)` | Payment that builds up to a future amount | `f·i/((1+i)^n−1)` |

## Layout

- [TI89_TVM_Project.html](TI89_TVM_Project.html): the project story and downloads
- [TVM_EQUATIONS.md](TVM_EQUATIONS.md): full equation reference
- `src/*.txt`: TI-BASIC source, one function per file
- `build/*.89f`: ready for TI Connect's "Send To TI Device"
- `tools/txt2ti89.py`: converts source into TI-89 variable files

## Build

```bash
python3 tools/txt2ti89.py src/*.txt
```

Functions are sent to the `main` folder (override with `--folder`). They are stored
as source text, and the calculator converts them the first time they run.

## License

[MIT](LICENSE) © 2026 David Orser
