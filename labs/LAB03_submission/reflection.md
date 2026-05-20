# Lab 3 Reflection — Movie Genre Classification

## Results Table

| Genre         | Part A Accuracy | Part B Accuracy |
|---------------|-----------------|-----------------|
| Animation     | 86.7%           | 85.3%           |
| Comedy        | 74.7%           | 81.3%           |
| Documentary   | 81.3%           | 84.7%           |
| Horror        | 79.3%           | 80.7%           |
| Romance       | 74.0%           | 65.3%           |
| Sci-Fi        | 62.0%           | 59.3%           |
| **Overall**   | 76.3%           | 76.1%           |

---

1. Architecture Choices
Image branch — I went with four ConvBlocks stacked sequentially (Conv2d → BatchNorm2d → ReLU → MaxPool2d), pushing channels from 3 up to 128 across the four stages. A 128×128 input shrinks down to an 8×8 feature map by the end, which I then collapse with global average pooling before projecting to a 128-d vector. I chose BatchNorm mainly because the poster images are all over the place visually — you've got clean Pixar frames sitting next to grainy 80s horror stills — and without it the network was pretty finicky about learning rate.
Tabular branch — This one has two parallel sub-branches that merge at the end. The numeric side handles the seven standardised features (runtime, vote average, etc.) through two FC layers. The embedding side builds separate lookup tables for cast, directors, writers, production companies, and MPAA rating, keeping only the top 50 tokens per field. List fields get mean-pooled; the rating field gets looked up directly. Everything concatenates and projects down to 128-d. I went with mean pooling over max pooling because for genre prediction I figured the overall profile of a film's cast and crew matters more than picking out a single standout name — though I'd actually revisit that decision now (more on that later).
I did try collapsing everything into one flat MLP at first instead of separating the numeric and embedding paths, and it was noticeably worse. My best guess is that numerics and embeddings are just too different in character, even post-standardisation, and keeping them separate until they've each been transformed first seems to help.
Fusion head — Concatenate the 128-d image and tabular vectors, then FC(256) → ReLU → Dropout(0.4) → FC(128) → ReLU → Dropout(0.2) → FC(6). Nothing fancy.

2. Overfitting
Honestly, overfitting was less of a problem than I expected. By epoch 20 the model was sitting at 76.8% training accuracy and 78.0% validation — so validation was actually higher, which happens when dropout is regularising training but not inference. The gap never really got wider than 2–3 points at any stage.
I threw a few things at it simultaneously, so it's hard to cleanly separate what helped most, but my rough ranking:

Dropout was the biggest lever. Early on I ran a version without it and training accuracy shot past validation within the first five epochs.
Weight decay (1e-3 via AdamW) — especially useful for the embedding tables, where a lot of tokens appear in only a handful of films.
Keeping the vocabulary small (top 50) — this stopped the embeddings from essentially memorising obscure actors or one-off directors.
Cosine annealing — kept the model from thrashing around late in training and validation accuracy was still ticking up at epoch 16–19.


3. Part A vs. Part B
The final test numbers ended up almost identical — 76.3% for Part A, 76.1% for Part B — which was surprising to me given how differently they trained early on. Part B hit 73.3% validation accuracy by epoch 2; Part A wasn't there until around epoch 7. That gap makes sense: ResNet18 walks in with features already distilled from 1.2 million images, so the projection head has something useful to work with from day one.
But the frozen backbone also puts a ceiling on things. ImageNet is full of photographs; movie posters — especially for animation or sci-fi — often look nothing like that. Part A had the freedom to learn filters specific to illustrated textures, bold typography, and stylised colour, and I think that's why it caught up by the end despite the slower start.
The per-class breakdown tells the more interesting story. Part B did better on Comedy (+6.6%), Documentary (+3.4%), and Horror (+1.4%) — genres where posters tend to look photographic (real faces, real locations). Part A did better on Romance (+8.7%), Animation (+1.4%), and Sci-Fi (+2.7%) — genres that lean on illustration or stylised design. That split is pretty much exactly what you'd predict from the ImageNet distribution argument.

4. What the Tabular Branch Is Actually Doing
Animation is the easiest class (86.7% / 85.3%), and I'm fairly confident that's the tabular branch doing most of the work. Animated films are just metadata-distinctive: G and PG ratings, a short list of recurring production companies (Disney, Pixar, DreamWorks all crack the top 50), and runtime patterns that differ from live-action. Even a conservative 50-token vocabulary picks that up cleanly.
Sci-Fi is the hardest (62.0% / 59.3%), and tabular features don't rescue it much. The genre is all over the map — wide budget range, no consistent MPAA rating, directors who typically make one sci-fi film and move on. There's also a lot of cast overlap with Action and Thriller. Visually, sci-fi posters lean dark and desaturated, which looks a lot like horror or action aesthetically.
Romance (74.0% / 65.3%) — Part B took a real hit here. Romantic comedy posters in particular share a lot of visual DNA with straight comedy (warm tones, faces centred), and pretrained ImageNet features don't seem to split them well. Tabular features help a bit (PG-13 skew, some recurring writers) but not enough to make up for it.
Documentary (81.3% / 84.7%) was the second-best class. The metadata is fairly distinctive — low budgets, small casts, niche production companies — and Part B's stronger result suggests documentary posters, often built around a single striking face or photograph, actually align pretty well with ImageNet-style visual features.
I should caveat all of this: without running image-only and tabular-only ablations I'm partly speculating on how much each branch is contributing. The animation/sci-fi gap at least is plausibly tabular-driven given how strong those metadata signals are, but I'd want the ablation to be sure.

5. What I'd Do Differently
The thing I'd try first is unfreezing ResNet18's layer4 block after the frozen run stabilises, using a much lower learning rate for the backbone (~1e-4) while keeping the rest of the network at normal speed. You'd get the early-epoch benefit of transfer learning without being stuck behind the ImageNet ceiling forever.
Second, I'd push the vocabulary larger — probably 200 tokens — but pair it with stronger embedding regularisation, either higher dropout on that sub-branch or per-embedding weight decay. At 50 tokens the model is being pretty conservative, and there are genre-defining directors and production companies that probably don't make the cut, especially for sci-fi and romance.
Third, I'd swap in max pooling for the list embeddings, particularly for directors. One filmmaker can basically define a genre (or at least be highly predictive of it), and mean pooling just averages that signal away with everyone else on the crew list. I mentioned above that I chose mean pooling deliberately, but honestly I think that was the wrong call.
Finally, sci-fi sitting at 62% while animation sits at 87% is a pretty uncomfortable gap. I'd experiment with focal loss or label smoothing to shift gradient attention toward the hard classes — probably without hurting overall accuracy much, since the model already has animation basically solved.