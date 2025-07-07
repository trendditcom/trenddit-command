# Trenddit supercharges you with AI

Use Trenddit to supercharge your productivity and workflow with personal, fast, and quality AI. Turn your Terminal into a configurable, interactive, and unobtrusive personal AI app. Power of 15 LLMs and 7 providers at your finger tips. Pair with workflows in Markdown, VS Code, Obsidian, and GitHub. Get productive fast with three simple commands.

**Command Is All You Need:** So, the LLM science fans will get the pun in our tagline. It is a play on the famous paper that introduced the world to Transformer model architecture - Attention is all you need. With Trenddit a simple command via your favorite terminal or shell is all you need to bend an large or small language model to your wishes. Trenddit provides a rich UI right there within your command prompt. No browser tabs to open, no apps to install, no context switching... just pure, simple, fast workflow. Try it with a simple command like `ask "create a table of planets"` and see your Terminal come to life just like a chat UI with fast streaming responses, markdown formatted tables, and even code blocks with color highlights if your prompt requires code in response! Trenddit has released 14 commands to help customize your personal AI workflow.

**Top Models and Providers:** You can switch private models or hosted frontier LLMs with ease. Trenddit comes with configurable support for more than 15 leading models (GPT 4o, Sonnet 3.5, Gemini 1.5 Pro, Mistral NeMo, Sonar Llama 3.1...) from 7 providers (Ollama, Anthropic, OpenAI, Groq, Google, Bedrock, and Perplexity).

**Markdown Workflows:** Trenddit works with markdown content (text files with simple formatting commands). So you can use it with many popular tools like VS Code and Obsidian to quickly and seamlessly design a custom workflow that enhances your craft.

**Do More With Less:** Trenddit is very simple to use out of the box as you learn its handful of powerful commands. As you get comfortable you can customize Trenddit commands simply by changing one configuration file and align Trenddit to suit your workflow. Everything in Trenddit has sensible defaults to get started quickly. 

**Make It Your Own:** When you are ready, everything is configurable and extensible including commands, models, providers, prompts, model parameters, folders, and document types. Another magical thing happens when the interface to your generative AI is a humble command prompt. You will experience a sense of being in control. In control of your workflow, your privacy, your intents, and your artifacts. You are completely in control of your personal AI workflow with Trenddit.

## Quick Start

Go to a folder where you want to initialize Trenddit. This could be your Obsidian vault or a VC Code project folder or even an empty folder.

```bash
pip install -U trenddit-command # upgrade or install latest Trenddit
tc init # copies config file, quick start samples
tc id # identifies active provider and model
ask "How old is the oldest pyramid?" # start prompting the model
```

### Models Setup
You will need to setup model-provider keys. Edit your environment config `~/.zshrc` like so.

```bash
export ANTHROPIC_API_KEY= # https://docs.anthropic.com/en/api/getting-started
export OPENAI_API_KEY= # https://openai.com/index/openai-api/
export GROQ_API_KEY= # https://console.groq.com/keys
export GEMINI_API_KEY= # https://ai.google.dev/gemini-api
export PERPLEXITY_KEY= # https://www.perplexity.ai/settings/api
```

If you do not want to use any of the model then all you need to do is remove the corresponding entries from `trenddit-command.yml` in the `model-mapping` and the `provider-model-mapping` sections. Also ensure that the other model configs only refer to available models.

For local models [install Ollama](https://ollama.com/) and download the latest [models](https://ollama.com/library) you want to run.

Now you are ready to test all models and providers.

```bash
tc test ask
tc test vision
```

### Python Environment Setup (optional)

*Skip this section if you have your Python environment already working.*

First, you should be running the latest Python on your system with Python package manager upgraded to the latest.

```bash
python --version
# should return Python 3.12.x or higher as on Sep'24
```

1. Optionally install latest [Python on Mac](https://docs.python-guide.org/starting/install3/osx/). 
2. Safely install Trenddit. Follow [this thread](https://apple.stackexchange.com/questions/237430/how-to-install-specific-version-of-python-on-os-x) to setup `pyenv` version manager.

First change to the directory to your VS Code workspace, Obsidian vault, or folder where you want to install Trenddit. Next create the virtual environment.

```bash
python -m venv env
```

Now you can activate your virtual environment like so. You will notice that directory prefixed with `(env)` to indicate you are now running in the virtual environment.

```bash
. env/bin/activate
```

To leave the virtual environment using `deactivate` command. Re-enter using same command as earlier.

Now you are ready to install Trenddit.

### Development Setup with Poetry

If you're working with the source code or want to contribute to the project, you can use Poetry for dependency management:

```bash
# Clone the repository and navigate to the project directory
cd /path/to/trenddit-command

# Activate poetry environment
poetry shell

# Install the package locally in development mode
poetry install

# Copies config file, quick start samples
tc init

# Verify installation and check current model
tc id

# Test the CLI
ask "How old is the oldest pyramid?"
```

Alternatively, you can run commands without activating the poetry shell:

```bash
# Install dependencies without activating shell
poetry install

# Run commands with poetry
poetry run tc id
poetry run ask "How old is the oldest pyramid?"
```

## Command Reference

*Note that `tc`, `ask`, `image` and `refer` are four top level commands available to you when you install Trenddit.

| Command      | Example and Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ***ask**     | `ask "your prompt"`<br>Prompt the LLM for a fast, crisp (default up to 300 words), single turn response<br><br>`ask`<br>Browses the configured prompts folder, lists prompt templates for user to run.                                                                                                                                                                                                                                                                                                                   |
| **audit**    | `tc audit`<br>Analyze your own usage of Trenddit over time with an insightful command line dashboard and markdown report.                                                                                                                                                                                                                                                                                                                                                                                                            |
| **config**   | `tc config ask save true`<br>Edit `trenddit-command.yml` file config from command line                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **gather**   | `tc gather "webpage url"`<br>Cleanly scrape an article from a webpage, without the menus, sidebar, footer. Includes images. Saves as markdown formatted similar to the HTML source.<br> <br>Refer the scraped markdown content using `refer gather` command.<br>Use vision on scraped images using `tc vision` command.                                                                                                                                                                                                        |
| ***refer**   | `refer text-to-extract`<br>Browse a set of raw text files and run custom prompts to extract new structured content.<br><br>`refer inline-prompts-to-run`<br>Run prompts embedded inline within text to expand, change, and convert existing documents.<br><br>`refer intents`<br>Expand a set of intents and prompts within an intents template<br><br>`refer your-command`<br>You can configure your own extensions to refer command by simply copying and changing any of the existing `refer-existing` model configs. |
| **run**      | `tc run`<br>Browse `Code` folder for markdown files with code blocks, create, setup, and run the app in one single command!<br><br>The `Code` folder markdown files with code blocks are created using `ask` command running `Create Vite App.md` prompt template or similar.                                                                                                                                                                                                                                       |
| **id**       | `tc id`<br>Identifies the current provider and model for `ask` command<br><br>`tc id section-name`<br>Identifies the provider and model defined in specific section                                                                                                                                                                                                                                                                                                                                                            |
| ***image**   | `image`<br>Select a prompt template to generate an image.<br><br>`image "Prompt for image to generate"`<br>Prompt to generate an image.                                                                                                                                                                                                                                                                                                                                                                                  |
| **init**     | `tc init`<br>Initialize trenddit-command in any folder. Copies `trenddit-command.yml` default config and quick start Intents and Embeds folders and files. Checks before overwriting. Use --force option to force overwrite files and folders.                                                                                                                                                                                                                                                                                        |
| **intents**  | `tc intents "Financial Analysis"`<br>Interactively choose from a list of intents within a template to refer into content embeds                                                                                                                                                                                                                                                                                                                                                                                     |
| **merge**    | `tc merge "Source File"`<br>Finds `Source File updated` with placeholder tags `[merge here]` or as custom defined in `merge` config, then merges the two files into `Source File merged`. Use along with `refer inline-prompts-to-run` command to reduce number of tokens processed when editing long text for context but updating only a section.                                                                                                                                                                 |
| **split**    | `tc split "Large File"`<br>Use this command to split a large file into chunks within a specified ratio of target model context. You can configure target model and ratio in `split` section of the configuration. Original file remains untouched and new files with same name and `part #` suffix are created.                                                                                                                                                                                                     |
| **test**     | `tc test ask`<br>Tests trenddit-command command using all providers and models defined in `trenddit-command.yml` config and provides a test summary.<br><br>`tc test vision`<br>Test vision models.                                                                                                                                                                                                                                                                                                                                              |
| **trends**   | `tc trends`<br>Visualize latency and token length trends based on `tc test` runs for `ask` and `vision` commands across models and providers. You can trend for a period of days using  `--days 7` command option.                                                                                                                                                                                                                                                                                                             |
| **validate** | `tc validate "Financial Analysis"`<br>Validates prior generated embeds running another model and reports the percentage difference between validated and original content.                                                                                                                                                                                                                                                                                                                                          |
| **vision**   | `tc vision -p path/to/image.png "Describe this image"`<br>Runs vision models on images from local path (-p), url (-u), or camera (-c) and responds based on prompt.                                                                                                                                                                                                                                                                                                                                                 |


## Trenddit Expands Your Content

Using Trenddit with few simple commands in your Terminal you can create a simple yet powerful personal AI content manager with your Markdown tool of choice like Obsidian or VS Code. For example, you can write partial blogs posts, write your seed ideas, start with a list of intents and prompts, or capture partial notes from a lecture where you were slightly distracted. 

Then you can use `refer` command in conjunction with custom `refer-section` configs within `trenddit-command.yml` to expand this partial, incomplete, or seed content into complete posts, notes, articles, prompt templates, and even well-researched papers. You can experiment with choice of models and providers, tune model settings in the config by document type, define custom folders for your content, and specify document specific system prompts to get exactly the outcome you desire based on the type of the document. You just have to remember one simple command `refer` and you are all set.

As a quick example, check out the `Posts` folder with sample partially written post on startup growth strategies. Now view the related config section within `trenddit-command.yml` for expanding posts.

```yaml
refer-post-to-update:
  lookup-folder: Posts
  max-tokens: 4000
  model: sonnet
  provider: claude
  save: true
  save-folder: Posts
  system: You will be given a partially written blog post on a topic.
    Your job as an expert blog writer is to expand the post...
  temperature: 0.5
```

Please note that for brevity we are not listing the complete system prompt here. You can obviously change it to suit your workflow. For now, just run `refer post-to-update "startup-growth-hacking"` command within the working folder where you initialized Trenddit. Soon the model response starts streaming into your terminal. The expanded post is saved in the `Posts` folder with `updated` prefix so you can compare with the original.

To create a new document type like research papers, class notes, cooking recipes, or whatever, all you need to do is copy and customize one of the `refer-post-to-update` or `refer-intents-to-expand` sections into something like your custom `refer-notes-to-summarize` section. Then you can run a custom command on your new document type like `refer notes-to-summarize "your-notes-file"` and achieve the same results.

## Combining Trenddit Commands

When combined with other Trenddit commands this workflow can get even more powerful. As an example, start by defining your document template for a set of intents and prompts as a simple markdown. For example `Financial Analysis` or `Product Management` are shown here. Next add a few intents as headings like, `Macro Factors Impact Stocks` or `Top Companies by ROCE` and so on. Then add simple prompts under these intents to generate content. You can now use Trenddit to expand on the set of intents and prompts in your document template with the command `refer intents-to-expand "Financial Analysis"` and the model will brainstorm more related intents and prompts for you to use.

![](https://raw.githubusercontent.com/trenddit-command/assets/main/images/obsidian-trenddit-command.png)

Now run `tc intents-to-expand "Financial Analysis"` and choose among a list of intents to generate as content embeds. The response is saved under `Embeds` folder automatically and the embed is linked in your document template instantly. Rinse, repeat.

This workflow can get really useful very fast. As each template has linked embeds, Obsidian Graph view can be used to visualize the links. You can get creative and link related templates or even enhance generated embeds with more intents. Of course this also means you can use all the great Obsidian plugins to generate websites, PDFs, and more.  Your creativity + Obsidian + Trenddit = Magic!

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/trenddit-command-intents-workflow.webp)


## Test and Evaluate Models and Providers

Trenddit comes with configurable support for more than 15 leading models from five providers (Ollama, Anthropic, OpenAI, Groq, Google). The `tc test` command can be used to run each of the trenddit-command commands over all the provider and model combinations and respond with a summary of model test and evaluation results. Use this to quickly compare models and providers as well as when you add or remove a new model or provider in the config.

This command is super useful when comparing model response time (latency), response quality (does it follow the system and prompt instructions), response accuracy, and token length (cost) for the same prompt. You can configure the test prompts within `trenddit-command.yml` in the `test` section.

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/tc-test-ask.png)

The screenshot above demonstrates the `tc test ask` command in action, showing a comprehensive test run across 12 different model configurations from providers including Groq, Gemini, OpenAI, Bedrock, and Claude. Each model is tested with the same prompt asking about NBA basketball court dimensions. The results table displays provider names, model identifiers, configuration settings, execution status, response times (ranging from 0.47s to 5.79s), and token counts. This visual summary makes it easy to compare performance metrics across providers - for instance, Groq's Llama models show the fastest response times (under 0.5s), while Ollama's local models take 3-5 seconds. The 100% success rate indicates all models successfully responded to the test prompt.

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/test-summary.webp)

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/tc-test-vision.png)

Here is an example of running `tc test vision` command and resulting test summary. The screenshot shows a comprehensive test of vision capabilities across multiple providers and models using a challenging test image - a circular formation of approximately 100 people wearing blue shirts, photographed from above. The test prompt asks models to count the number of people in the image. The results reveal significant differences in vision model capabilities: only OpenAI's GPT-4o, Gemini models, Claude Sonnet-3.7, and Bedrock Sonnet-3.7 successfully processed the vision task, with response times ranging from 3.1s to 4.9s. Many models in the test suite (shown as "Skipped" with N/A values) are not equipped with vision capabilities, highlighting the importance of selecting appropriate models for vision tasks. This visual comparison helps users quickly identify which models support vision processing and their relative performance characteristics.

You can also notice the response times seem proportional to model size. For Claude, Opus > Sonnet > Haiku. For Gemini, Pro > Flash. For OpenAI, GPT-4o > GPT-4-mini.

You can similarly run `tc test ask` command to test across all models and providers. In this run you may find groq is among the fastest providers when it comes to response time.

Of course, you may need multiple test runs to get better intuition of response times as there are multiple factors which effect latency other than model size or architecture, like network latency, which may change across multiple test runs.

## Visualize Trends

Each `tc test` command run saves the test summary data in `Metrics` folder by timestamp and provider-model. Over time you can visualize trends of latency and token count metrics to see if models are performing consistently. Run `tc trends` command to view trends for 7 days (default).

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/trends.webp)

The visualization uses sparklines to show data trends over time. Use this to decide when/if to switch models based on performance trends.

## Run multiple models side by side

Want to compare multiple models side by side? All you need to do is open multiple shells or Terminal instances. Now in each of these, one by one, change the model, run same `ask "prompt"` and compare the results side by side. Simple!

![](https://raw.githubusercontent.com/trenddit-command/assets/main/images/compare-models-1.png)

![](https://raw.githubusercontent.com/trenddit-command/assets/main/images/compare-models-2.png)

As Trenddit commands use the `trenddit-command.yml` config in the current folder every time they run, you can create more complex parallel running, multi-model and cross-provider workflows by simply copying the config file into multiple folders and running commands there. This way you can be running some long running tasks on a local model in one folder and terminal. While you are doing your day to day workflow in another. And so on.


## Workflow freedom

There is no behavioral marketing or growth hacking a business can do within your command prompt. You guide your workflow the way you feel fit. Run the fastest model provider (Groq with Llama 3.1), or the most capable model right now (Sonnet 3.5 or GPT-4o), or the latest small model on your laptop (Mistral Nemo), or the model with the largest context (Gemini 1.5 Flash), you decide. Run with fast wifi or no-wifi (using local models), no constraints. Instantly search, research, Q&A to learn something or generate a set of artifacts to save for later. Switching to any of these workflows is a couple of changes in a config file or a few easy to remember commands on your terminal.

You can also configure custom model names to actual model version mapping for simplifying model switching commands. With the following mapping the commands to switch models are `tc config ask model llama` or `tc config intents model haiku` and so on.

```yaml
model-mapping:
  # Claude models
  sonnet: claude-3-5-sonnet-20240620
  opus: claude-3-opus-20240229
  haiku: claude-3-haiku-20240307
  
  # Ollama models
  llama: llama3.1
  gemma: gemma2
  mistral: mistral-nemo
  
  # Groq models
  groq-mixtral: mixtral-8x7b-32768
  groq-llama: llama2-70b-4096

  # OpenAI models
  gpt4mini: gpt-4o-mini
  gpt4o: gpt-4o

  # Gemini models
  gemini-pro: gemini-1.5-pro
  gemini-flash: gemini-1.5-flash
```



## Privacy controls 

You decide which model and provider you trust, or even choose to run an LLM locally on your laptop. You are in control of how private your data and preferences remain. Trenddit supports state of the art models from Anthropic, OpenAI, Google, and Meta. You can choose a hosted provider or Ollama as a local model provider on your laptop. Switch between models and providers using a simple command like `tc config ask model llama` to switch from the current model.

You can also load custom model config sets mapped to each command. Configure these in `trenddit-command.yml` file. Here is an example of constraining how `tc ask` and `tc intents` commands behave differently using local and hosted model providers.

```yaml
ask:
  provider: ollama
  model: mistral
  max-tokens: 300
  save: false
  system: Be crisp in your response. Only respond to the prompt 
	using valid markdown syntax. Do not explain your response.
  temperature: 0.3

intents:
  provider: claude
  model: sonnet
  max-tokens: 1000
  save: true
  folder: Embeds
  system: Only respond to the prompt using valid markdown syntax.
    When responding with markdown headings start at level 2. 
    Do not explain your response.
  temperature: 0.0
```


## Audit Trail

Trenddit saves a trail of commands, prompts, templates, lookup folders, and saved files in `trail.yml` file. You can visualize this anytime using `tc audit` command to gain insights of your Trenddit usage over time.

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/audit-summary.webp)

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/audit-prompt-analysis.webp)

## Intent driven 

Your intents are tasks you want to execute, goals you want to accomplish, plans you want to realize, decisions you want to make, or questions you want to answer. You control your entire Trenddit experience with your intents. You can save your intents as simple outline of tasks in a text file. You can recall them when you need. You can run models on your intents as you feel fit. You can save results based on your intents.

![](https://raw.githubusercontent.com/trenddit-command/trenddit-command/main/images/trenddit-command-intents.webp)

## Validate Generations

You can verify content generated by one LLM with validation from another model. Make sure you only run validate command after you have run `refer intents` command to generate the first pass of embeds. Use `tc validate "Financial Analysis"` or any intent template that you have created. The workflow for validation is similar to expand intents. Only in this case the validate model config decides which model and provider to use. You can also modify the validation prompt to check for any specific things relevant for your use case. The diff is calculated on original and validated text removing any newlines, white space, or markdown formatting when making the diff comparison using similarity scoring. Use this to automate quality validation of generated content.