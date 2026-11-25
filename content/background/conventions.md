---
title: Conventions and notation
---

# Conventions and notation

!!! note "Draft"
    This page collects the notation used on the old site in one place. It was assembled during the migration and
    still needs to be checked and completed.

## Thom polynomials

For a contact singularity $\Sigma_Q$ of relative dimension $l$ (map germs $(\mathbb{C}^n,0)\to(\mathbb{C}^{n+l},0)$),
the Thom polynomial depends only on the *quotient Chern classes* $c_i$, defined by

$$\frac{1+b_1t+b_2t^2+\dots}{1+a_1t+a_2t^2+\dots}=1+c_1t+c_2t^2+\dots,$$

where $a_i$ and $b_i$ are the Chern classes of the source and the target. For a partition
$\lambda=(\lambda_1,\dots,\lambda_r)$ the Schur polynomial is $s_\lambda=\det(c_{\lambda_i+j-i})_{i,j=1,\dots,r}$.
See [What is a Thom polynomial](thom-polynomials.md) for the definitions.

In the data files (Maple syntax): `c[i]` is $c_i$, and `s[[3,1]]` is $s_{(3,1)}$.

## SSM-Thom polynomials

An SSM-Thom polynomial is written as a series in an auxiliary variable `t` that records the cohomological degree:
`+t^4*( ... ) +t^5*( ... ) + ...`. The lowest-degree part (degree = codimension) is the ordinary Thom polynomial.
Each series is known only up to a certain degree, recorded in the data file as `computed-up-to-degree`.

## Multi-singularities: pushforward notation

On the multi-singularity pages, `s[[i1,i2,...]]` denotes the pushforward $f_*(c_{i_1}c_{i_2}\cdots)$ and
`sc[[i1,i2,...]]` denotes $f_*(\mathrm{Schur}(i_1,i_2,\dots))$. The older target page (April 2025) wrote `s[i,j]`
for `s[[i,j]]`; the data files use the double brackets throughout.

The target codimension on the older page was written as "$k(+1)$". *To be explained.*

Multi-singularities are named by their points with multiplicities, for example $2\mathrm{A}_0+\mathrm{A}_2$; the
points are ordered as in Mather's list. In file and page names this is written `2A0+A2`, and the empty
multi-singularity is `EMPTY` (page: `empty`). *This naming is provisional.*

## Thom series

See the introduction of the [Thom series](../tables/thom-series.md) page: residue presentations $F_{Q,\omega}$ for a
filtration profile $\omega$, the variables $d_i$ with $\mathrm{Tp}(\Sigma^l_Q)=\mathrm{Ts}_Q|_{d_i=c_{l+1+i}}$, and
$\Delta_\lambda=\det(d_{\lambda_i+j-i})$.

## K-theory

K-theoretic Thom polynomials and motivic Segre Thom polynomials are written in double stable Grothendieck polynomials
$G_\lambda$, in the convention of Rimányi–Szenes. (The old portal wrote $g_\lambda$ for the same polynomials.)

*Variables.* $\alpha_1,\dots,\alpha_n$ are the K-theoretic Chern roots (classes of line bundles) of the source and
$\beta_1,\dots,\beta_{n+l}$ those of the target. Any one of the following fixes the convention:

* with $\alpha_i=e^{a_i}$, $\beta_j=e^{b_j}$ one has $G_\lambda=s_\lambda+{}$higher order terms, where $s_\lambda$ is
  the Schur polynomial of the Thom polynomial pages ($s_{1}=c_1$, $s_{2}=c_2$, $s_{1,1}=c_1^2-c_2$);
* for one source and one target variable, $G_{(m,1^j)}=(1-\alpha/\beta)(1-\alpha)^{m-1}(1-1/\beta)^j$ and every other
  $G_\lambda$ is $0$;
* test case: the push-forward K-theoretic Thom polynomial of $A_2$ for $l=0$ is
  $G_{1,1}+2G_{2}-2G_{2,1}-G_{3}+G_{3,1}$.

*Two versions of the K-theoretic Thom polynomial.* The **push-forward version** is the class of the structure sheaf of
a resolution of the closure, pushed forward. The **MS<sub>0</sub> version** is the coefficient of $z^0$ of the motivic
Segre Thom polynomial of the closure. They agree when the closure has mild singularities
(see [K-theoretic Thom polynomials](k-theory.md) and [Motivic Segre Thom polynomials](motivic.md)).

*The parameter of the motivic class* is $z$, with $y=-z/(1+z)$.

*In the data files* (Maple syntax) `gr[[3,1]]` is $G_{(3,1)}$. This is the name used by the Maple package "Double
stable Grothendieck polynomials" on the [Downloads](../downloads.md) page, so that `subs(GR[k,l], ...)` turns an
expansion into a polynomial in the $\alpha_i,\beta_j$. *(To be confirmed: that the package follows the same
convention.)* A K-theoretic Thom polynomial is written with one line per degree $\lvert\lambda\rvert$; a motivic Segre
Thom polynomial as `+z^0*( ... ) +z^1*( ... ) + ...`, known up to the order recorded as `computed-up-to-z-order`.

Every K-theoretic data file also records how certain it is (`formula-status`, `expansion-status`, `completeness`);
the labels are explained on the [Motivic Segre Thom polynomials](motivic.md#how-certain-the-entries-are) page.

## Orbit and closure

A singularity $\eta$ is a locally closed set of germs; its closure $\overline\eta$ also contains the more degenerate
singularities. Which of the two a class refers to depends on the kind of class.

| Class | Refers to |
|---|---|
| Thom polynomial | the closure (it is the fundamental class of $\overline\eta$) |
| K-theoretic Thom polynomial, both versions | the closure |
| SSM-Thom polynomial | either; **the portal holds the class of the singularity locus $\eta$ itself** |
| Motivic Segre Thom polynomial | either; **so far the portal holds the class of the closure $\overline\eta$** |

The two variants carry the same information once the whole hierarchy is known: the class of the closure is the sum of
the classes of all singularities contained in it. For example, for $l=0$,
$\mathrm{SSM}(\overline{\Sigma^1})=\mathrm{SSM}(A_1)+\mathrm{SSM}(\overline{A_2})$ and
$\mathrm{SSM}(A_0)=1-\mathrm{SSM}(\overline{\Sigma^1})$.

Both variants are shown on the page of the singularity, in the same section, labelled "closure" or "orbit". In the
data files the header line `locus:` says which one a file contains, and for motivic Segre Thom polynomials it is also
part of the file name: `ms_closure_l0.txt`, `ms_orbit_l0.txt`.

A [Thom–Boardman class](../singularities/thom-boardman.md) and the contact singularity that is open and dense in it
have the same closure, hence the same closure-type classes; these are stored once, on the page of the Thom–Boardman
class, and the page of the contact singularity points there.

## Convention versions

Each data file records the convention it follows (`convention:` line). The labels used for now are
"TPP 2025" (Thom polynomials and SSM-Thom polynomials) and "TPP 2026" (Thom series, whose signs and orientations were
revised in 2026). *These labels are placeholders to be defined here.*
