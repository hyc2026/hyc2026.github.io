# LLM RL Training

## GRPO
GRPO eliminates the value function and estimates the advantage in a group-relative manner. For a specific input data $x$, the behavior policy $\pi_{\theta_\text{old}}$ samples a group of $G$ individual responses $\{ y_i\}_{i=1}^G$. Then, the advantage of the $i$-th response is calculated by normalizing the group-level rewards $\{ R_i \}_{i=1}^G$:

$$
\begin{aligned}
\mathcal{J}_\text{GRPO}(\theta)& = \mathbb{E}_{ x \sim \mathcal{D},\, \{y_i\}_{i=1}^G \sim \pi_{\theta_\text{old}}( \cdot | x) } \\&
\Bigg[ \frac{1}{G}\sum_{i=1}^{G} \frac{1}{|y_i|}\sum_{t=1}^{|y_i|} \Bigg( 
\min \Big( r_{i,t}(\theta) \hat{A}_{i,t},  
\ \text{clip} \Big( r_{i,t}(\theta), 1 - \varepsilon, 1 + \varepsilon \Big) \hat{A}_{i,t} \Big)
- \beta D_{\text{KL}}(\pi_{\theta} || \pi_{\text{ref}}) 
\Bigg) \Bigg]
\end{aligned}
$$

where

$$
\begin{aligned}
    r_{i,t}(\theta)=\frac{\pi_{\theta}(y_{i,t} \mid x, y_{i,<t})}{\pi_{\theta_{\text{old}}}(y_{i,t} \mid x,y_{i,<t})},\quad\hat{A}_{i,t} = \frac{R_i - \text{mean}(\{R_i\}_{i=1}^G)}{\text{std}(\{R_i\}_{i=1}^G)}.
\end{aligned}
$$

## DAPO
DAPO samples a group of outputs $\{y_i\}_{i=1}^G$ for each question $q$ paired with the answer $a$, and optimizes the policy via the following objective:
$$
\begin{aligned}
\mathcal{J}_{\text{DAPO}}(\theta) =\quad& \mathbb{E}_{ x \sim \mathcal{D},\, \{y_i\}_{i=1}^G \sim \pi_{\theta_\text{old}}( \cdot | x) }\\&
\Bigg[\frac{1}{\sum_{i=1}^{G}|y_i|}\sum_{i=1}^{G}\sum_{t=1}^{|y_i|} 
\min \Big( r_{i,t}(\theta) \hat{A}_{i,t},  
\ \text{clip} \Big( r_{i,t}(\theta), 1 - {\varepsilon_{\text{low}}}, 1 + {\varepsilon_{\text{high}}} \Big) \hat{A}_{i,t} \Big) \Bigg]\quad\text{s.t.}\ \Big|\{R_i\}\Big| > 1,
\end{aligned}
$$
where
$$
\begin{aligned}
    r_{i,t}(\theta)=\frac{\pi_{\theta}(y_{i,t} \mid x, y_{i,<t})}{\pi_{\theta_{\text{old}}}(y_{i,t} \mid x,y_{i,<t})},\quad\hat{A}_{i,t} = \frac{R_i - \text{mean}(\{R_i\}_{i=1}^G)}{\text{std}(\{R_i\}_{i=1}^G)}.
\end{aligned}
$$

DAPO introduces 4 key techniques to make RL shine in the long-CoT RL scenario.
- **Clip-Higher**, which promotes the diversity of the system and avoids entropy collapse;
- **Dynamic Sampling**, which improves training efficiency and stability;
- **Token-Level Policy Gradient Loss**, which is critical in long-CoT RL scenarios;
- **Overlong Reward Shaping**, which reduces reward noise and stabilizes training.

## GSPO
While the token-level importance weight $\frac{ \pi_{\theta} (y_{i,t} | x, y_{i,<t}) }{ \pi_{\theta_\text{old}} (y_{i,t} | x,y_{i,<t})}$ is problematic in GRPO, in the context of language generation, the *sequence-level* importance weight $\frac{ \pi_{\theta} (y | x) }{ \pi_{\theta_\text{old}} (y | x)}$ has a clear theoretical meaning: it reflects how far the response $y$ sampled from $\pi_{\theta_\text{old}} (\cdot | x)$ deviates from $\pi_{\theta} (\cdot | x)$, which naturally aligns with the sequence-level reward and can also serve as a meaningful indicator of the clipping mechanism.


Based on this straightforward observation, GSPO employs the following sequence-level optimization objective:

$$
\begin{aligned}
\mathcal{J}_\text{GSPO} (\theta) =
\mathbb{E}_{ x \sim \mathcal{D},\, \{y_i\}_{i=1}^G \sim \pi_{\theta_\text{old}}( \cdot | x) }
\left[ 
\frac{1}{G} \sum_{i=1}^{G}
\min \left( s_{i}(\theta)  \hat{A}_{i},  \, \mathrm{clip} \left( s_{i}(\theta), 1 - {\varepsilon}, 1 + {\varepsilon} \right) \hat{A}_{i} \right) 
\right]
\end{aligned}
$$

where we adopt the group-based advantage estimation:

$$
\begin{aligned}
\hat{A}_i = \frac{R_i - \text{mean}(\{R_i\}_{i=1}^G)}{\text{std}(\{R_i\}_{i=1}^G)},
\end{aligned}
$$

and define the importance ratio $s_{i}(\theta)$ based on sequence likelihood:

$$
\begin{aligned}
s_{i}(\theta) = \left( \frac{ \pi_{\theta} (y_i \mid x) }{ \pi_{\theta_\text{old}} (y_i \mid x)} \right)^{\frac{1}{|y_i|}}
=
\exp \left( \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \log \frac{ \pi_{\theta} (y_{i,t} \mid x, y_{i,<t}) }{ \pi_{\theta_\text{old}} (y_{i,t} \mid x,y_{i,<t})} \right).
\end{aligned}
$$

## Words of Experience

### Importance Sampling

The essence of importance sampling is that we want to compute expectations under a new distribution, but our data is drawn from an old distribution. We therefore use the probability ratio of the same action under the new and old policies as a correction weight:

$$
\mathbb{E}_{p_\text{new}}[f(x)]=\mathbb{E}_{p_\text{old}}\Big[\frac{p_\text{new}(x)}{p_\text{old}(x)}f(x)\Big]
$$

This allows us to evaluate the expected value under the new policy using offline data from the old policy, avoiding the need to resample after each update (thus lowering cost). However, if the gap between the new and old policies is too large, the variance of the weights can become very high, leading to unstable training.

### DAPO - Token-Level Gradient Loss

DAPO fixes the problem that, in GRPO, the gradient weight for each token decreases as the sampled response length increases.

However, this is not always effective. When implementing length penalties on outputs, i.e. outputs exceeding a certain length threshold will be given a large penalty, using token level gradient loss will result in a much larger number of tokens with negative advantages than positive advantages, leading to training crashes. Under this situation, sequence level gradient loss or token level whiten should be used after calculating the advantage.

### GSPO - Addressing GRPO Instability in MoE Training

GSPO changes the optimization granularity from token-level to sequence-level. The motivation behind this shift stems from the fact that, during training with MoE architectures, GRPO’s importance sampling introduces large variance and instability. The core idea of GSPO is to reduce reliance on per-token optimization during reward processing while placing more emphasis on the overall sequence outcome. Below, we introduce the main concepts behind GSPO.

Traditional algorithms such as PPO and GRPO typically optimize each token in the model’s output individually, giving some tokens higher weights and others lower. While this aims for fine-grained optimization, in long-text, large-model scenarios it can instead introduce noise and reward bias, causing the model to lose direction, or even collapse suddenly. The root of the problem is that **we evaluate the model based on the full response, yet train it token-by-token, leading to a mismatch between the reward granularity and the optimization objective**. GSPO aligns the reward and the optimization target by switching from per-token scoring to sequence-level optimization. This shift offers two main benefits: 

1. Stability – GSPO optimizes entire sequences, reducing the training noise from token-level fluctuations.
2. Efficiency – GSPO filters and retains only high-quality samples for optimization, accelerating convergence and improving results. 

In MoE architectures, the benefits are even greater: **since only a small subset of expert modules is activated per inference, the routing path is dynamic and hard to control**. Traditional methods often rely on Routing Replay, recording expert activations during inference and enforcing the same routing during training, to ensure consistency. While effective, this greatly increases engineering cost and limits performance. GSPO’s sequence-level logic naturally **avoids the need for Routing Replay**, making MoE training lighter and more stable. For the growing number of large MoE models, this is a valuable breakthrough.

The problem in large-model training is that importance sampling is performed per-token, and a single token’s ratio cannot meaningfully perform distribution correction. Instead, it introduces high-variance noise, especially in the unstable MoE setting. This suggests that GRPO’s token-level computation may be inherently suboptimal.

#### Why does GRPO struggle to converge in MoE architectures?
Expert activation volatility: New and old policies may activate different experts, introducing structural bias and noise. When $\pi_{\theta_\text{old}}$ is updated, the router may also change, so the two policies could activate completely different sets of experts, even if only one training step has passed. This causes large fluctuations in output probabilities, triggering clipping abnormally often. Clipped tokens contribute no gradient, and those that remain often contain noise.

In theory, the importance ratio should reflect probability changes caused by parameter updates under the same structure. But expert changes lead to unpredictable, high-variance fluctuations unrelated to the optimization direction. This variance distorts policy gradient estimates, making training unstable and even causing collapse.

#### Routing Replay before GSPO
Routing Replay records the expert activations during sampling from $\pi_{\theta_\text{old}}$ and forces $\pi_{\theta_\text{old}}$ to use the same routing path during training. The downside: high engineering and infrastructure cost, and inefficiency, $\pi_{\theta}$ might have found a better routing path but is forced to follow the old one.

While traditional methods use Routing Replay to mitigate expert activation mismatches, GSPO bypasses this dependency entirely, reducing structural variance at its root.

#### GSPO loss design

> If the reward is sequence-level, the importance ratio should also be sequence-level.

From the above, GSPO replaces GRPO’s per-token ratio with a sequence-level ratio, which is no longer tied to the step index $t$. The idea is to drop the token-level objective in favor of sequence-level scaling. This naturally leads to GSPO’s new optimization target: replacing token-level importance ratios with sequence-level ones.

We can view the token-level optimization objective as a first-order approximation to the sequence-level objective that we truly aim to optimize, as long as $\pi_\theta$ is close to $\pi_{\theta_\text{old}}$.

Sequence-level ratios are length-normalized to reduce variance and keep values on a consistent scale. Without normalization, answers of different lengths would make the ratio highly length-sensitive. Since all tokens from the same sequence share the same importance ratio, clipping (if triggered) will clip the entire sequence, not just certain tokens.