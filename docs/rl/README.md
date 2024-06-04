# Reinforcement Learning

## Concept

### Random Variable

A variable whose values depend on outcomes of a random event.

Uppercase letter $X$ for random variable.

Lowercase letter $x$ for observed value.

### Probability Density Function (PDF)

PDF provides a relative likelihood that the value of the random variable would equal that sample.

Random variable $X$ is in the domain $\mathcal{X}$.

For continuous distribution, $\int_\mathcal{X}p(x) \mathrm{d}x = 1$.

For discrete distribution, $\sum_{x\in\mathcal{X}}p(x)=1$.

### Expectation

Random variable $X$ is in the domain $\mathcal{X}$.

For continuous distribution, the expectation of $f(X)$ is:
$$\mathbb{E}[f(X)] = \int_\mathcal{X}p(x)\cdot f(x)\mathrm{d}x$$

For discrete distribution, the expectation of $f(X)$ is:
$$\mathbb{E}[f(X)] = \sum_{x\in\mathcal{X}}p(x)\cdot f(x)$$

### Terminologys

State: $s$

Action: $a$

Policy function $\pi$: ($s$, $a$) $\mapsto$ [0, 1]:
$$\pi(a|s)=\mathbb{P}(A=a|S=s)$$

Reward: $R$

State Transition:
$$p(s'|s,a)=\mathbb{P}(S'=s'|S=s,A=a)$$

Trajectory: list of (state, action, reward)

Return: cumulative discounted future reward ($\gamma$ is discount rate)
$$U_t=R_t+\gamma\cdot R_{t+1}+\gamma^2\cdot R_{t+2}+\gamma^3\cdot R_{t+3}+...$$

Action-Value Function for policy $\pi$: 
$$Q_\pi(s_t, a_t)=\mathbb{E}[U_t|S_t=s_t,A_t=a_t]$$
- For policy $\pi$, $Q_\pi(s, a)$ evaluates how good it is for an agent to pick action $a$ while being in state $s$.

Optimal Action-Value Function (upper bound of $Q$):
$$Q^*(s_t,a_t)=\underset{\pi}{\mathrm{max}}\ Q_\pi(s_t,a_t)$$

State-Value Function:
$$V_\pi(s_t)=\mathbb{E}_A[Q_\pi(s_t,A)]=\sum_a\pi(a|s_t)\cdot Q_\pi(s_t,a)=\int_a\pi(a|s_t)\cdot Q_\pi(s_t,a)\mathrm{d}a$$
- For fixed policy $\pi$, $V_\pi(s)$ evaluates how good the situation is in state $s$.
- $\mathbb{E}[V_\pi(S)]$ evaluates how good the policy $\pi$ is.

The agnet can be controlled by either $\pi(a|s) $(policy-based method) or $Q^*(s,a) $(value-based method).

## Value-based Method

Optimal Action-Value Function
$$Q^*(s_t,a_t)=\underset{\pi}{\mathrm{max}}\ Q_\pi(s_t,a_t)$$
- Whatever policy function $\pi$ is used, the result of taking $a_t$ at state $s_t$ cannot be better than $Q^*(s_t,a_t)$

### Deep Q-Network (DQN)

Goal: maximize the total reward

If we know $Q^*(s,a)$, the best action ought to be $a^*=\underset{a}{\mathrm{argmax}}\ Q^*(s,a)$. ($Q^*$ is an indication for how good it is for an agent to pick $a$ while being in state $s$.)

How to get $Q^*(s,a)$? Use neural network $Q(s, a; \mathbf{w})$ to approximate $Q^*(s,a)$.

#### Temporal Difference (TD) Learning

$U_t=R_t+\gamma\cdot U_{t+1}$

$\underbrace{Q(s_t,a_t;\mathbf{w})}_{\approx\mathbb{E[U_t]\ (\mathrm{Prediction})}}\approx\mathbb{E}[R_t+\gamma\cdot \underbrace{Q(S_{t+1},A_{t+1};\mathbf{w})}_{\approx\mathbb{E[U_{t+1}]\ (\mathrm{TD\ Target})}}]$

#### One Iteration of TD Learning

1. Observe state $S_t=s_t$ and Action $A_t=a_t$.

2. Predict the value: $q_t=Q(s_t,a_t;\mathbf{w}_t)$.

3. Environment provides new state $s_{t+1}$ and reward $r_t$.

4. Compute TD target: $y_t=r_t+\gamma\cdot Q(s_{t+1},a_{t+1};\mathbf{w})=\gamma\cdot\underset{a}{\mathrm{max}}\ Q(s_{t+1},a;\mathbf{w})$.

5. Calculate Loss: $L_t=\frac12[q_t-y_t]^2$.

6. Gradient Descent: $\mathbf{w}_{t+1}=\mathbf{w}_t-\eta\cdot\frac{\partial L_t}{\partial\mathbf{w}}|_{\mathbf{w}=\mathbf{w}_t}=\mathbf{w}_t-\eta\cdot(q_t-y_t)\cdot\frac{\partial Q(s_t,a_t;\mathbf{w})}{\partial\mathbf{w}}|_{\mathbf{w}=\mathbf{w}_t}$.

## Policy-based Method

Policy function $\pi(a|s)$ is a probability density function (PDF).

Policy Network: Use a neural network $\pi(a|s;\mathbf{\theta})$ to approximate policy function $\pi(a|s)$.

Approximate value function $V(s_t;\mathbf{\theta})=\sum_a\pi(a|s_t;\mathbf{\theta})\cdot Q_\pi(s_t,a)$.

Policy-based Learning: Learn $\theta$ that maximizes $\mathcal{J}(\mathbf{\theta})=\mathbb{E}_S[V(S;\mathbf{\theta})]$.
- update policy by policy stochastic gradient ascent: $\mathbf{\theta}\leftarrow\mathbf{\theta}+\eta\cdot\frac{\partial V(s;\mathbf{\theta})}{\partial\mathbf{\theta}}$.

  $\begin{aligned}\frac{\partial V(s;\mathbf{\theta})}{\partial \mathbf{\theta}} &= \frac{\partial\sum_a\pi(a|s;\mathbf{\theta})\cdot Q_\pi(s,a)}{\partial\mathbf{\theta}}\\ &= \sum_a\frac{\partial\pi(a|s;\mathbf{\theta})\cdot Q_\pi(s,a)}{\partial\mathbf{\theta}}\\ &= \sum_a\frac{\partial\pi(a|s;\mathbf{\theta})}{\partial\mathbf{\theta}}\cdot Q_\pi(s,a)\ \mathrm{(pretend}\ Q_\pi\ \mathrm{is\ independent\ of} \ \theta.)\\ &= \sum_a\pi(a|s;\mathbf{\theta})\cdot\frac{\partial\ \mathrm{log}\ \pi(a|s;\mathbf{\theta})}{\partial\mathbf{\theta}}\cdot Q_\pi(s,a)\\ &= \mathbb{E}_A[\frac{\partial\ \mathrm{log}\ \pi(A|s;\mathbf{\theta})}{\partial\mathbf{\theta}}\cdot Q_\pi(s,A)]\end{aligned}$

- This derivation is over-simplified and not rigorous, ignoring the derivatice of $Q_\pi$.

### Two forms of policy gradient
- Form1 for discrete action space: $\frac{\partial V(s;\mathbf{\theta})}{\partial \mathbf{\theta}} =\sum_a\frac{\partial\pi(a|s;\mathbf{\theta})}{\partial\mathbf{\theta}}\cdot Q_\pi(s,a)$

- Form2 for continuous action space: $\frac{\partial V(s;\mathbf{\theta})}{\partial \mathbf{\theta}} =\mathbb{E}_{A\sim\pi(\cdot|s;\mathbf{\theta})}[\frac{\partial\ \mathrm{log}\ \pi(A|s;\mathbf{\theta})}{\partial\mathbf{\theta}}\cdot Q_\pi(s,A)]$

    Use Monte Carlo approximation to approximate expectation.

    1. Randomly sample an action $\hat{a}$ according to the PDF $\pi(\cdot|s;\mathbf{\theta})$.
    2. Calculate $\mathbf{g}(\hat{a};\mathbf{\theta})=\frac{\partial\ \mathrm{log}\ \pi(\hat{a}|s;\mathbf{\theta})}{\partial\mathbf{\theta}}\cdot Q_\pi(s,\hat{a})$.
    
        Obviously, $\mathbb{E}_A[\mathbf{g}(A;\mathbf{\theta})]=\frac{\partial V(s;\mathbf{\theta})}{\partial \mathbf{\theta}}$, $\mathbf{g}(\hat{a};\mathbf{\theta})$ is an unbiased estimate of $\frac{\partial V(s;\mathbf{\theta})}{\partial \mathbf{\theta}}$.
    
    3. Use $\mathbf{g}(\hat{a};\mathbf{\theta})$ as an approximation to the policy gradient $\frac{\partial V(s;\mathbf{\theta})}{\partial \mathbf{\theta}}$.

    This approach alse works for discrete actions.

### One Iteration

1. Observe the state $s_t$.

2. Randomly sample action $\hat{a}$ according to $\pi(\cdot|s;\mathbf{\theta})$.

3. Compute $q_t\approx Q_\pi(s_t,a_t)$ (some estimate).

4. Differentiate policy network: $\mathrm{\mathbf{d}}_{\theta,t}=\frac{\partial\ \mathrm{log}\ \pi(a_t|s_t;\mathbf{\theta})}{\partial\mathbf{\theta}}|_{\mathbf{\theta}=\mathbf{\theta}_t}$.

5. (Approximate) policy gradient: $\mathbf{g}(a_t;\mathbf{\theta}_t)=q_t\cdot\mathrm{\mathbf{d}}_{\theta,t}$.

6. Update policy network: $\mathbf{\theta}_{t+1}=\mathbf{\theta}_t+\eta\cdot\mathbf{g}(a_t;\mathbf{\theta}_t)$.

**How to estimate $q_t$?**

### REINFORCE

Play the game to the end and generate the trajectory:
$$s_1,a_1,r_1,\ s_2,a_2,r_2,\ ...,\ s_T,a_T,r_T$$

Compute the discounted return $u_t=\sum_{k=t}^T\gamma^{k-t}r_k$, for all $t$.

Since $Q_\pi(s_t,a_t)=\mathbb{E}[U_t]$, we can use u_t to approximate $Q_\pi(s_t,a_t)$.

### Actor-Critic Method

Approximate $Q_\pi(s,a)$ using a neural network $q_\pi(s,a;\mathbf{w})$.

$$V(s_t;\mathbf{\theta})=\sum_a\pi(a|s)\cdot Q_\pi(s,a)\approx\sum_a\pi(a|s;\mathbf{\theta})\cdot Q_\pi(s,a;\mathbf{w})$$

Training: Update the parameters $\mathbf{\theta}$ and $\mathbf{w}$.

Update policy network $\pi(a,s;\mathbf{\theta})$ to increase the state-value $V(s;\mathbf{\theta},\mathbf{w})$, supervision is purely from the value network (critic).

Update value network $Q_\pi(s,a;\mathbf{w})$ to better estimate the return, supervision is purely from the rewards.

1. Observe state $s_t$ and randomly sample $a_t\sim\pi(\cdot|s_t;\mathbf{\theta}_t)$.

2. Perform $a_t$; then the environment gives new state $s_{t+1}$ and reward $r_t$.

3. Randomly sample $\tilde{a}_{t+1}\sim\pi(\cdot|s_{t+1};\mathbf{\theta}_t)$.

4. Evaluate value network: $q_t=q(s_t,a_t;\mathbf{w}_t)$ and $q_t=q(s_{t+1},a_{t+1};\mathbf{w}_t)$.

5. Cpmpute TD error: $\delta_t=q_t-(r_t+\gamma\cdot q_{t+1})$.

6. Update value network: $\mathbf{w}_{t+1}=\mathbf{w}_t-\alpha\cdot\delta_t\cdot\frac{\partial~q(s_t,a_t;\mathbf{w})}{\partial~\mathbf{w}}|_{\mathbf{w}=\mathbf{w}_t}$.

7. Update policy network: $\mathbf{\theta}_{t+1}=\mathbf{\theta}_t+\beta\cdot\delta_t\cdot\frac{\partial~\mathrm{log}~\pi(a_t|s_t;\mathbf{\theta})}{\partial~\mathbf{\theta}}|_{\mathbf{\theta}=\mathbf{\theta}_t}$.

   Using $q_t$ and $\delta_t$ here has the same expectation, while using $\delta_t$ (also called advantage) has the smaller variance.

## PPO for LLM

[reference](https://zhuanlan.zhihu.com/p/645225982)

Pseudocode for the overall algorithm.

```python
policy_model = load_model()
ref_policy_model = policy_model.copy()

for k in range(20000):
    # Sampling
    prompts = sample_prompt()
    responses = respond(policy_model, prompts)
    old_log_probs, old_values = analyze_responses(policy_model, prompts, responses)

    # Reward
    scores = reward_model(prompts, responses)
    ref_log_probs, _ = analyze_responses(ref_policy_model, prompts, responses)
    rewards = reward_func(scores, old_log_probs, ref_log_probs)
    
    # Leaning
    advantages = advantage_func(rewards, old_values)
    for epoch in range(4):
        log_probs, values = analyze_responses(policy_model, prompts, responses)
        actor_loss = actor_loss_func(advantages, old_log_probs, log_probs)
        critic_loss = critic_loss_func(rewards, values)
        loss = actor_loss + 0.1 * critic_loss
        train(loss, policy_model.parameters())
```

### Sampling

Sample m prompts from the pool and generate responses using old_policy, the output are as follows:

- responses: m strings with n tokens in each string.

- old_log_probs: actor(old_policy) output tensor with the shape of [m, n], contains the logarithmic probability of tokens in the response $\mathrm{log(}p\mathrm{(token|context))}$.

- old_values: critic output tensor with the shape of [m, n], contains the estimated revenue of the critic for each token generation.

### Reward

Score each response using the Reward Model, and include a term in the reward thatt penalizes the KL divergence between the learned RL policy $\pi_\phi^{\mathrm{RL}}$ with parameters $\phi$ and the original SFT model $\pi^{\mathrm{SFT}}$.

$
\begin{aligned}
S(x,y)&=r_\theta(x,y)-\beta\cdot\mathrm{log}[\pi_\phi^{\mathrm{RL}}(y|x)/\pi^{\mathrm{SFT}}(y|x)]\\&=r_\theta(x,y)-\beta\cdot[\mathrm{log}~\pi_\phi^{\mathrm{RL}}(y|x)-\mathrm{log}~\pi^{\mathrm{SFT}}(y|x)]
\end{aligned}
$

And for each token, the reward would be:

$
\mathrm{reward}[i]=\left\{
\begin{aligned}
& \mathrm{ref\_log\_probs}[i]-\mathrm{old\_log\_probs}[i], & i<N \\
& \mathrm{ref\_log\_probs}[i]-\mathrm{old\_log\_probs}[i]+S, & i=N \\
\end{aligned}
\right.
$

- ref_log_probs: ref_policy output tensor with the shape of [m, n].
- The higher the ref_log_probs, the more recognized the output of old_policy by ref_policy, indicating that old_policy is more compliant and therefore deserves higher rewards.
- The higher the old_log_probs, the lower the reward. It serves as a regularization term, ensuring the diversity of probability distributions.

### Learning

Learning is the process of reinforcing advantageous actions.

Actual Return: rewards to go.

$$
\mathrm{return}[i]=\sum_{j=i}^N\mathrm{reward}[j]=\mathrm{reward}[i]+...+\mathrm{reward}[N]
$$

Expected Return: old_values output by critic.

Advantages: extent to which the actual returns exceed expected returns.

$$a[i]=\mathrm{return}[i]-\mathrm{old\_values}[i]$$

Reinforce Advantageous Actions:

$\begin{aligned}\mathrm{actor\_loss}&=-\frac1M\frac1N\sum_{i=1}^M\sum_{j=1}^Na[i,j]\times\frac{p(\mathrm{token}[i,j]|\mathrm{context})}{p_{\mathrm{old}}(\mathrm{token}[i,j]|\mathrm{context})}\\&=-\frac1{MN}\sum_{i=1}^M\sum_{j=1}^Na[i,j]\times\mathrm{exp}(\mathrm{log\_prob}[i,j]-\mathrm{old\_log\_prob}[i,j])\end{aligned}$

- Make mini batch and the log_prob will be constantly updated.
- $a$ represents the degree of reinforcing $p$.
- When the probability of generating a certain token is already high ($p_\mathrm{old}$ is large), even if the advantage of this action is significant, there is no need to further increase the probability aggressively, which is similat to reducing lr.

$\begin{aligned}\mathrm{critic\_loss}=\frac1{2MN}\sum_{i=1}^M\sum_{j=1}^N(\mathrm{values}[i,j]-\mathrm{returns}[i,j])^2\end{aligned}$