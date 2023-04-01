# DoccGPT Data

This repository allows you to generate a dataset of well-documented Swift code. I created it in an attempt to improve [DoccGPT](https://github.com/gonzalonunez/docc-gpt) by fine-tuning one of OpenAI's base models.

I am sad to report that it doesn't look like it is immediately worth it. It might be after significantly more fine-tuning (and significantly more dollars), but even then given the context windows of the soon-to-land GPT-4 models there is likely no point in paying so much to get a good base model that still has a context window of 2048 tokens. Hopefully we can fine-tune GPT-4 in the future, or perhaps we may not even need to.

Here's an overview of what I did:

1. Ran through the directions in the README to generate the `data.jsonl` file. This results in a little over 200 viable prompt/completion pairs, which is the minimum number of examples that OpenAI suggests for fine-tuning.

2. Then, I fine-tuned `ada` for $0.40. It was able to put comments in the right place for a simple `enum`, but the comments failed to describe the code well.

3. Lastly, I fine-tuned `davinci` for about $30. It left better comments, also in the right places, but at the end of the day the fine-tuned model's performance is still not even remotely close to what I was seeing with the more advanced out-of-the-box models. It struggled to document all of the fields in a simple `User` `struct` with 4 properties and a function.

## Basic usage

1. Clone the repository and its submodules:

```
git clone --recurse-submodules git@github.com:gonzalonunez/docc-gpt-data.git
```

2. If you have already cloned it, you can also update the submodules:

```
git submodule update --init --recursive
```

3. Ensure that you have [yonaskolb/Mint](https://github.com/yonaskolb/Mint) installed, and use it to install [ross](https://github.com/gonzalonunez/ross).

```
mint install gonzalonunez/ross
```

4. Ensure that you have [apple/swift-format](https://github.com/apple/swift-format) installed. We use this in the next step in order to format files after cleaning them up.

```
brew install swift-format
```

5. Run `python generate.py` to generate prompt/completion pairs in `/files`. This will generate hundreds of folders based on the `.swift` files in the repository, which come from the repository's submodules. Each folder contains a `Prompt.swift` file and a `Completion.swift` file, which are both modified copies of an original source file. `Prompt.swift` is `Completion.swift` but with all DocC comments removed by [ross](https://github.com/gonzalonunez/ross).

6. Run `python data.py`. This takes all of the prompt/completion pairs in `/files` and formats them in such a way that they can later be used to fine-tune an OpenAI Model. The formatted data is saved into a JSON file named `data.jsonl`. You can now delete the `/files` directory if you'd like to, but I find that it's nice to inspect manually before spending the time/money to fine-tune a model.

7. This `data.jsonl` file is what you will pass over to OpenAI for fine-tuning. Follow the instructions [here](https://platform.openai.com/docs/guides/fine-tuning/cli-data-preparation-tool) and fine-tine your model. Using OpenAI's tool will take care of removing examples that are too long.

```
OPENAI_API_KEY=<YOUR_KEY> openai tools fine_tunes.prepare_data -f data.jsonl
```

After using OpenAI's [CLI preparation tool](https://platform.openai.com/docs/guides/fine-tuning/cli-data-preparation-tool), you should see the following message:

> After you’ve fine-tuned a model, remember that your prompt has to end with the indicator string `\n\n###\n\n` for the model to start generating completions, rather than continuing with the prompt. Make sure to include `stop=[" <END>"]` so that the generated texts ends at the expected place.
