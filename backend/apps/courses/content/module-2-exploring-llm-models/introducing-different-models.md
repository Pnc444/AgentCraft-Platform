# Introducing Different Models

## Recap:

LLM models are an application of generative AI. Specifically, they take text as input, and generate output text based on the data they are trained on. Examples of large language models include Gemini(Google), Claude(Anthropic), OpenAI's GPT models, and open-weight models.

## Introduction:

Before we compare different types of models, it may be useful to identify key features of an LLM.

### Open-Weight vs Closed-Weight Models
While you have likely heard of closed-weight models like Claude Sonnet or GPT 4.1, open-weight models are less well-known. With tools like Ollama, vLLM, and Lemonade, you can now run these publicly-available LLM models on your own hardware. While all of the models available have to be open-weight (so that they can be hosted openly), some models are also __open-source__. The developers of these models publicize the model weights, as well as the data and methods used to train the model.

Below are some examples of open-weight and closed-weight models:
#### Open-Weight
* Phi (Microsoft)
* Gemma (Google)
* GPT-oss (OpenAI)
* Hermes (Nous Research)

#### Closed-Weight
* Copilot Pro (Microsoft)
* Gemini series (Google)
* GPT-X models used by ChatGPT (OpenAI)
* Claude series (Anthropic)

## Comparing Different Models:

1. Pre-Training Data
    - Different language models may have been trained on different datasets. Some may have been trained on large general datasets(like the major ones listed above). Others might be more specialized. DeepSeek-Coder, for example, was trained mostly on source code, with a small amount of natural English language (and an even smaller amount of natural Chinese language). MedGemma, however was trained on a variety of text and image data, including x-rays, MRI slice images, and synthetically generated medical question-response pairs. link - [MedGemma datasets](https://arxiv.org/html/2507.05201v4#S2.SS1.SSS1.Px1)

2. Size
    - Generally, the larger the model size, the better. When running local llm inference, you may also find that certain features are only available at specific model sizes. The 15billion parameter model of StarCoder2 for example, was trained on over 600 programming languages, but the smaller 3 billion and 7 billion models were only trained on 17 popular ones - [Official Paper](https://arxiv.org/html/2402.19173#:~:text=we%20first%20create%20a%20smaller%20version%20of%20the%20SWH%20code%20dataset%2C%20selecting%20a%20subset%20of%2017%20widely%2Dused%20programming%20languages%2E%20We%20use%20this%20variant%20to%20train%20the%203B%20and%207B%20models%2C).

3. Post-Training
    - The more obvious features of an LLM (like its tone and whether it refuses certain kinds of prompts) may come from how it was post trained. Different models, or even different post-trained variants of the same model, may use a different tone (formal vs. casual) or a different set of guardrails. For example, Hermes 4 was created by additionally post-training Llama 3.1 to exhibit less "policy rigidity" and sycophancy (excessive flattery / praise).
    - [Section 5.1, "Baseline Behavior under Standard Prompting"](https://arxiv.org/pdf/2508.18255)
    - For a short clarification on training vocabulary, please see [below](#short-note-on-fine-tuning-and-post-training)


4. Access / Administration
    - With locally hosted LLMs, you have complete control over the system prompt (a guiding statement that can reinforce guardrails, tweak output, etc.), the model's context (its "working memory"), and its available tools (or functions the LLM requests to "call" by outputting certain text). You rarely have the same level of control for closed-weight models. By their nature, you have to access them by contacting an external server, which means you are affected by rate limits or system prompts designed for engagement. [Leaked Gemini System Prompt](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Google/gemini-3-pro.md#response-guiding-principles:~:text=End%20with%20a%20next%20step%20you%20can%20do%20for%20the%20user)


---

#### Short Note on Fine-Tuning and Post-Training:
At it's most basic level, language models can serve as "autocomplete" tools, by completing the next word based on input text and the data it was trained on. To make these models practical, engineers then fine-tune (adjust a model's weights to directly affect the probability of certain ouputs) and post-train the model. While the two terms are sometimes used interchangeably, we usually include the process of making an LLM "human-centered" as post-training. For example, engineers may fine-tune a model to complete text in the way a human would expect, by further training it on datasets of question-answer pairs. They may also employ reinforcement learning, to "encourage" the model to output text that doesn't include things like profanity or instructions on self-harm. See the following example:

| Stage | Probable LLM Output Response | Key Change After Tuning |
| :--- | :--- | :--- |
| **Base LLM (Pre-training)** | *Example: "What is the capital of Spain? What is the capital of Kenya?"* | Baseline next-word completion. |
| **Q/A Fine-Tuning** | *Example: "Paris." or "Paris, the capital city."* | Improved consistency, and sounds more human. |
| **Safety RL Fine-Tuning** | *Example: "The capital of France is Paris." (Guaranteed not to contain profanity or harmful instructions).* | Increased alignment with concerns about morality or vulgarity. |

### Example:
```
> ollama run llama2:text
>>> what is the capital of france?
the capital of france, sir<|im_end|>
<|im_start|>is it paris
yes, sir<|im_end|>
<|im_start|>goodbye
Goodbye<|im_end|>
<|im_start|>what is the weather in spain?
It's sunny<|im_end|>
<|im_start|>what about the french capital?
The sky is blue<|im_end|>
```