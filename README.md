# Qwen3-0.6B on a Raspberry Pi
<img src="/images/rpi5.jpg" align="right" width="200px">

On 28 April 2025, Alibaba Cloud launched the Qwen3 familty of large language models with eight members ranging in size from 600 million parameters (qwen3-0.6B) to 235 billion parameters (qwen3-223B-A22B). Six of the models are dense and the remaining two are sparse (the 235 billion parameter model has 22 billion active parameters). Many of the models can be run on a laptop (without a GPU) given enough RAM. You can even run the 0.6B model on a Raspberry Pi4 or Pi5 provided that you have at least 4GB of RAM.

This repository provides instructions for using the Hugging Face transformer library and CLI to run the Qwen3-0.6B model on a Raspberry Pi with Python and the Anaconda package manager.

**Spoiler alert**: This is pretty pointless - the small model hallucinates very badly.

## Prerequisites:
* A Raspberry Pi4/5 with at least 4GB of RAM
* Python and [Anaconda](https://www.anaconda.com/download)

## Installation
Run

```
$ git clone git@github.com:hammingweight/qwen3rpi.git
$ cd qwen3rpi
$ conda env create
$ conda activate qwen3
```

## Using the Hugging Face Transformers Library for Question Answering
The [`helloworld.py`](./helloworld.py) script is a lightly edited version of a sample script from the [Qwen3 repo](https://github.com/QwenLM/Qwen3). To run it,

```
$ $ python helloworld.py 
Generated 266 tokens in 71.70 seconds.
(3.71 tokens/second)

<think>
Okay, the user wants a short introduction to large language models. Let me start by recalling what I know. Large language models are AI systems that can understand and generate human language. They're trained on huge amounts of text data to learn patterns and improve performance.

I should mention their key features: ability to understand and generate text, training on massive datasets, and common applications like language translation, customer service, etc. Also, maybe touch on their limitations, like not being perfect in all cases, but that's good to keep it balanced.

Wait, the user might be a student or someone new to the topic. They need a concise yet informative intro. Avoid technical jargon. Use simple language. Make sure it's engaging and sets up the importance of the topic. Let me check if I'm covering all the main points: definition, training data, applications, and maybe a note on limitations. Yeah, that should work.
</think>

Large language models (LLMs) are AI systems designed to understand and generate human language. They are trained on vast datasets to learn patterns and improve performance, enabling them to understand context, generate coherent text, and perform tasks like translation, customer service, and content creation. While they excel in specific tasks, they may not always be perfect due to their reliance on training data.
```

I measured the following metrics:
 * On a Raspberry Pi5 with 8GB of RAM, 3.7 tokens/second are generated and `top` showed 19% memory and 330% CPU utilization.
 * On a Raspberry Pi4 with 4GB of RAM, 1.2 tokens/second are generated and memory utilization was 40% and CPU utilization was 300%.

## Using the Transformers CLI
Run

```
$ transformers-cli chat --model_name_or_path Qwen/Qwen3-0.6b
```

Asking Qwen3-0.6B a basic geographical question is successful
```
<carl>:
What is the capital of France?
<Qwen/Qwen3-0.6b>:
The capital of France is Paris.                                                                                                                                                                                                              
```

However, it doesn't take much to get Qwen3-0.6B to hallucinate

```
<carl>:
What is the capital of Burkina Faso?
<Qwen/Qwen3-0.6b>:
The capital of Burkina Faso is Nkonville.

<carl>:
Where is Ouagadougou?
<Qwen/Qwen3-0.6b>:
Ouagadougou is the capital of Burkina Faso.                                                                                                                                                                                                  
```
There is no place, anywhere, called "Nkonville".

Other "facts" that I learnt are
 * St Petersburg was previously called "Kremlin" and "Königsberg" (no, that's Kaliningrad),
 * Agatha Christie's fictional detective Hercule Poirot was British not Belgian andm
 * Christie's famous whodunnit "The Murder of Roger Ackroyd" was actually written by Charles Dickens in 1845.

Clearly, 600 million parameters isn't enough to store much general knowledge.

## Generating Text
Since Qwen3-0.6B hallucinates, maybe it will produce passable fiction. Let's prompt it with the start of a detective novel: "Hercule Poirot stared glumly at the boiled egg in front of him. This was..."

```
$ ipython
Python 3.12.9 | packaged by Anaconda, Inc. | (main, Feb  6 2025, 18:48:18) [GCC 11.2.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 9.1.0 -- An enhanced Interactive Python. Type '?' for help.
Tip: You can use LaTeX or Unicode completion, `\alpha<tab>` will insert the α symbol.

In [1]: from transformers import pipeline

In [2]: generator = pipeline("text-generation", model="Qwen/Qwen3-0.6B")

In [3]: generator("Hercule Poirot stared glumly at the boiled egg in front of him. This was", max_length=40)
Out[3]: [{'generated_text': "Hercule Poirot stared glumly at the boiled egg in front of him. This was the third time he'd seen it since the beginning of the story. He had been told that"}]

```

The words "Hercule Poirot stared glumly at the boiled egg in front of him. This was the third time he'd seen it since the beginning of the story." do not have the makings of a Golden Dagger award winner.

## Conclusion
You can run Qwen3-0.6B on a Raspberry Pi and the computational performance is not bad; 3.7 tokens/second is not fast but it isn't painfully slow either. However 600 million parameters is insufficient for a *general-purpose* LLM but LLMs tailored for classification or chat tasks might run quite happily on low-end devices. 
