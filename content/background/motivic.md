---
title: Motivic Segre Thom polynomials
---

# Motivic Segre Thom polynomials

!!! note "Draft"
    This page was written in November 2026, when the first data of this kind were added. It still has to be checked
    and completed.

## Where they fit

The motivic Segre Thom polynomial is to the K-theoretic Thom polynomial what the SSM-Thom polynomial is to the Thom
polynomial.

| | Cohomology | K-theory |
|---|---|---|
| Class of the closure $\overline\eta$ | [Thom polynomial](thom-polynomials.md) | [K-theoretic Thom polynomial](k-theory.md), in two versions: push-forward and MS<sub>0</sub> |
| Its one-parameter deformation | [SSM-Thom polynomial](ssm.md) | motivic Segre Thom polynomial |
| How the first row is recovered from the second | the lowest-degree part | the coefficient of $z^0$ (of the class of the closure) is the MS<sub>0</sub> version |
| Written in | Schur polynomials $s_\lambda$ | double stable Grothendieck polynomials $G_\lambda$ |

## Definition

Let $\eta$ be a singularity and $\overline\eta\subset V$ its closure in the space $V$ of germs
$(\mathbb C^n,0)\to(\mathbb C^{n+l},0)$. The motivic Segre class of the closure is

$$\mathrm{ms}_l(\overline\eta)=\frac{mC_y(\overline\eta\subset V)}{\lambda_y(T^*V)},$$

where $mC_y$ is the motivic Chern class. On the portal it is written in the parameter $z$, with $y=-z/(1+z)$, as a series

$$\mathrm{ms}_l(\overline\eta)=\sum_\lambda c_\lambda(z)\,G_\lambda ,\qquad c_\lambda(z)\in\mathbb Z[z]\ \text{of degree } \lvert\lambda\rvert .$$

Infinitely many partitions occur, but only finitely many at each order of $z$; every series on the portal is given up to
a stated order of $z$.

The same class can be taken for the singularity locus $\eta$ itself instead of its closure; see
[Orbit and closure](conventions.md#orbit-and-closure). The data files say which of the two they contain.

## Relation to the other classes

* The coefficient of $z^0$ of $\mathrm{ms}_l(\overline\eta)$ is the **MS<sub>0</sub> version** of the K-theoretic Thom
  polynomial (the class of $mC_0$ of the closure). It is a finite sum.
* The MS<sub>0</sub> version equals the **push-forward version** when the closure has mild singularities. Among the
  singularities on the portal this holds for $A_1$, $A_2$ and the Thom–Boardman classes $\Sigma^r$, and it fails for
  $A_3$ and $I_{2,3}$: for example the coefficient of $G_{2,2}$ is $-4$ in the push-forward version of $A_3$ at $l=0$
  and $-5$ in the MS<sub>0</sub> version.
* The lowest-degree part of either version, with $G_\lambda$ replaced by $s_\lambda$, is the Thom polynomial.
* The coefficients of $z^{\lvert\lambda\rvert}$ in $c_\lambda(z)$, with $G_\lambda$ replaced by $s_\lambda$, give the
  SSM class of the closure. This was compared with the SSM-Thom polynomials of the portal (which are classes of the
  singularity locus itself): for $l=0,\dots,3$, in all degrees available on both sides,
  $\mathrm{SSM}(A_0)=1-\mathrm{SSM}(\overline{\Sigma^1})$ and
  $\mathrm{SSM}(A_1)=\mathrm{SSM}(\overline{\Sigma^1})-\mathrm{SSM}(\overline{A_2})$.

## How certain the entries are

Every K-theoretic entry carries two labels, one for the formula it comes from and one for its expansion in
Grothendieck polynomials. They are shown next to the entry, with the details under "Status".

| Label | Meaning |
|---|---|
| formula: theorem | a theorem in the literature |
| formula: resolution model | Kazarian's resolution models, used in K-theory as the push-forward of the structure sheaf of the resolution; this K-theoretic form is not published or refereed |
| formula: argued | a proof is sketched, not complete; details will be in the paper in preparation |
| formula: not yet checked | stated, but not yet checked; details will be in the paper in preparation |
| expansion: theorem | the expansion itself is a theorem |
| expansion: verified numerically | computed, and compared with the formula at random points (a probabilistic identity test) |
| partial | only a stated block of partitions is given; nothing is claimed about the other coefficients |

"Completeness" says which coefficients an entry claims to list. For the series in $z$ it is stated in terms of
$d_l(\lambda)=\max\{d:\lambda_d\ge d+l\}$ (for $l=0$ the size of the Durfee square of $\lambda$).

## On the portal

The [K-theory tables](../tables/ktp.md) list what is recorded, by relative dimension. Each entry also appears on the
page of its singularity, in the sections "K-theoretic Thom polynomials" and "Motivic Segre Thom polynomials".

## References

* L. M. Fehér, R. Rimányi: *K theory Thom polynomials*, in preparation, 2026. Unless an entry says otherwise, the
  K-theoretic data of the portal are from this work.
* R. Rimányi, A. Szenes: *Residues, Grothendieck polynomials, and K-theoretic Thom polynomials*, Int. Math. Res. Not.
  IMRN, [doi:10.1093/imrn/rnac345](https://doi.org/10.1093/imrn/rnac345).
* L. M. Fehér, R. Rimányi, A. Weber: *Motivic Chern classes and K-theoretic stable envelopes*.
* M. Kazarian: *Non-associative Hilbert scheme and Thom polynomials*, arXiv:1712.09270.
