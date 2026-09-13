# Week 1 — What is a rollout, formally?

Let $\Omega = \bigcup_{n=0}^{N} (S\times A)^n \times S$ for finite state/action sets $S, A$ —
the set of all finite agent trajectories. This is a finite union of finite sets, hence
countable. Take $\mathcal F = 2^\Omega$ (every subset is an event); this needs no further
construction, because the pathologies that force $\sigma$-algebras to be built by extension
theorems exist only on uncountable spaces — on a countable $\Omega$, closure under complement
and countable union is automatic. Define $m(\tau)$ for $\tau=(s_0,a_0,s_1,a_1,\dots)$ by the
chain rule,
$$m(\tau) = \mu_0(s_0)\,\pi(a_0\mid s_0)\,T(s_1\mid s_0,a_0)\,\pi(a_1\mid s_1)\,T(s_2\mid s_1,a_1)\cdots,$$
and set $\mathbb P(A) = \sum_{\tau \in A} m(\tau)$ for any $A \in \mathcal F$. A rollout,
formally, is a draw $\tau \sim \mathbb P$ — one i.i.d. sample from $m$ — and any statistic
built from a batch of rollouts (empirical success rate, a bootstrap CI) is a function of
finitely many such draws.
