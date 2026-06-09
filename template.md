---
title: "The Title of Your Research Paper"
author:
  - "First Author Name^1^"
  - "Second Author Name^2^"
date: "\today"
abstract: |
  This is the abstract of the paper. It should be a concise summary of the problem, methodology, key findings, and implications of your research. 
bibliography: references.bib
csl: apa.csl
output: pdf_document
---

# 1. Introduction

Write your introduction here. Cite sources using bracketed citations, like this [@author_year]. 

## 1.1 Background Context

To emphasize a word, use *italics* or **bold** text. To add an inline mathematical formula, use single dollar signs, for example, $E = mc^2$.

# 2. Methodology

Describe the methods used in your study. For block mathematical equations, use double dollar signs:

$$
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$

## 2.1 Data Collection

Use standard Markdown tables to present study variables:


| Variable | Definition | Expected Impact |
| :--- | :--- | :--- |
| Variable A | Independent variable | Positive |
| Variable B | Dependent variable | Negative |

# 3. Results

Present your findings in this section. You can reference figures and tables by labeling them or linking to your image paths: `![Figure 1: Study model.](figures/figure1.png)`

# 4. Discussion

Interpret your results here. Compare your findings with existing literature [@smith2024].

# 5. Conclusion

Summarize the main points and provide avenues for future research.

# References
