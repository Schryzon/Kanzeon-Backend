<div id="top">

<!-- HEADER STYLE: BANNER -->
<div align="center">
<img src="img/Kanzeon-Banner-Final.jpg" alt="description" style="width:60%;">

<table>
<tr>
<td><img src="img/Kanzeon1x1-Circle.png" width="40"></td>
<td><h1>Kanzeon: Clarity, Among Chaos.</h1></td>
</tr>
</table>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/Schryzon/Kanzeon-Backend?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=FAFAFA" alt="license">
<img src="https://img.shields.io/github/last-commit/Schryzon/Kanzeon-Backend?style=for-the-badge&logo=git&logoColor=white&color=FAFAFA" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Schryzon/Kanzeon-Backend?style=for-the-badge&color=FAFAFA" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Schryzon/Kanzeon-Backend?style=for-the-badge&color=FAFAFA" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/JSON-000000.svg?style=for-the-badge&logo=JSON&logoColor=white" alt="JSON">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python">

</div>

---

## Table of Contents

1. [Table of Contents](#table-of-contents)
2. [Overview](#overview)
3. [Features](#features)
4. [Project Structure](#project-structure)
    4.1. [Project Index](#project-index)
5. [Getting Started](#getting-started)
    5.1. [Prerequisites](#prerequisites)
    5.2. [Installation](#installation)
    5.3. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgments](#acknowledgments)

---

## Overview
A powerful **text summarizer** built on Google’s pretrained **[T5-large](https://huggingface.co/google-t5/t5-large)** (via HuggingFace).  

This is the **backend-focused** version of Kanzeon, designed for the **UNRAM S-Cube Hackathon 2025**.

Utilizes your **GPU** if CUDA is available, and the CUDA version of **[Pytorch](https://pytorch.org/get-started/locally/)** is installed.

---

## Features

- 📝 **General Summarization**  
  Leverages T5-large to condense any text into clear, concise summaries.

- 🔄 **LoRA Adapter Load & Save**  
  Quickly load previously fine-tuned adapters or persist new ones without retraining the full model.

- 📊 **Status Checks**  
  `/kanzeon/status` endpoint shows service health, device type, and VRAM usage.

- 🛡️ **Out of Memory Handling**  
  Auto-falls back to CPU on GPU OOM, then self-heals back to GPU when memory frees up.

- 🌐 **Multilingual Support**  
  Auto-detects language, translates to English for summarization, then back to the original language.

---

## Project Structure

```sh
└── Kanzeon-Backend/
    ├── Dockerfile
    ├── LICENSE
    ├── README.md
    ├── backend.py
    ├── examples
    │   ├── example.pdf
    │   ├── mock_data.json
    │   ├── mock_data2.json
    │   └── mock_data3.json
    ├── frontend.py
    ├── img
    │   ├── Kanzeon-Banner-Final.jpg
    │   ├── Kanzeon1x1-Circle.png
    │   ├── Kanzeon1x1-Erased.png
    │   └── Kanzeon1x1.jpg
    ├── kanzeon_adapter
    │   ├── README.md
    │   ├── adapter_config.json
    │   └── adapter_model.safetensors
    ├── mock_commands.txt
    ├── requirements.txt
    └── test
        ├── check_dir.py
        └── test.py
```

### Project Index

<details open>
  <summary><b><code>KANZEON-BACKEND/</code></b></summary>
  <!-- __root__ Submodule -->
  <details open>
    <summary><b>__root__</b></summary>
    <blockquote>
      <div class='directory-path' style='padding: 8px 0; color: #666;'>
        <code><b>⦿ __root__</b></code>
      <table style='width: 100%; border-collapse: collapse;'>
      <thead>
        <tr style='background-color: #f8f9fa;'>
          <th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
          <th style='text-align: left; padding: 8px;'>Summary</th>
        </tr>
      </thead>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/Dockerfile'>Dockerfile</a></b></td>
          <td style='padding: 8px;'>Contains the Dockerfile used to containerize the Kanzeon API and its runtime dependencies.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/mock_commands.txt'>mock_commands.txt</a></b></td>
          <td style='padding: 8px;'>Lists sample cURL commands and usage examples for testing all Kanzeon endpoints.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/LICENSE'>LICENSE</a></b></td>
          <td style='padding: 8px;'>The MIT License governing usage, modification, and distribution of this project.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/requirements.txt'>requirements.txt</a></b></td>
          <td style='padding: 8px;'>Specifies all required Python packages and their versions for both the backend and frontend.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/frontend.py'>frontend.py</a></b></td>
          <td style='padding: 8px;'>Streamlit application that provides a user interface to interact with the Kanzeon API.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/backend.py'>backend.py</a></b></td>
          <td style='padding: 8px;'>Main Quart-based server implementation defining the Kanzeon class, routes and summarization logic.</td>
        </tr>
      </table>
    </blockquote>
  </details>
  <!-- test Submodule -->
  <details open>
    <summary><b>test</b></summary>
    <blockquote>
      <div class='directory-path' style='padding: 8px 0; color: #666;'>
        <code><b>⦿ test</b></code>
      <table style='width: 100%; border-collapse: collapse;'>
      <thead>
        <tr style='background-color: #f8f9fa;'>
          <th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
          <th style='text-align: left; padding: 8px;'>Summary</th>
        </tr>
      </thead>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/test/check_dir.py'>check_dir.py</a></b></td>
          <td style='padding: 8px;'>A two-line script to find the location of the installed models from HuggingFace.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/test/test.py'>test.py</a></b></td>
          <td style='padding: 8px;'>Initial testing script for the pipeline (no routes implemented).</td>
        </tr>
      </table>
    </blockquote>
  </details>
  <!-- kanzeon_adapter Submodule -->
  <details open>
    <summary><b>kanzeon_adapter</b></summary>
    <blockquote>
      <div class='directory-path' style='padding: 8px 0; color: #666;'>
        <code><b>⦿ kanzeon_adapter</b></code>
      <table style='width: 100%; border-collapse: collapse;'>
      <thead>
        <tr style='background-color: #f8f9fa;'>
          <th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
          <th style='text-align: left; padding: 8px;'>Summary</th>
        </tr>
      </thead>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/kanzeon_adapter/adapter_config.json'>adapter_config.json</a></b></td>
          <td style='padding: 8px;'>JSON file containing the LoRA adapter configuration parameters used for fine-tuning.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/kanzeon_adapter/adapter_model.safetensors'>adapter_model.safetensors</a></b></td>
          <td style='padding: 8px;'>Binary file storing the fine-tuned LoRA adapter weights.</td>
        </tr>
      </table>
    </blockquote>
  </details>
  <!-- examples Submodule -->
  <details open>
    <summary><b>examples</b></summary>
    <blockquote>
      <div class='directory-path' style='padding: 8px 0; color: #666;'>
        <code><b>⦿ examples</b></code>
      <table style='width: 100%; border-collapse: collapse;'>
      <thead>
        <tr style='background-color: #f8f9fa;'>
          <th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
          <th style='text-align: left; padding: 8px;'>Summary</th>
        </tr>
      </thead>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/examples/mock_data.json'>mock_data.json</a></b></td>
          <td style='padding: 8px;'>Sample JSON payload for a basic text summarization request #1.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/examples/mock_data2.json'>mock_data2.json</a></b></td>
          <td style='padding: 8px;'>Sample JSON payload for a basic text summarization request #2.</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
          <td style='padding: 8px;'><b><a href='https://github.com/Schryzon/Kanzeon-Backend/blob/master/examples/mock_data3.json'>mock_data3.json</a></b></td>
          <td style='padding: 8px;'>Sample JSON payload for a basic text summarization request #3.</td>
        </tr>
      </table>
    </blockquote>
  </details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Container Runtime:** Docker

### Installation

Build Kanzeon-Backend from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/Schryzon/Kanzeon-Backend
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd Kanzeon-Backend
    ```

3. **(Optional) Create & activate a virtualenv** (if you plan to use pip):

    ```sh
    ❯ python3 -m venv .venv
    ❯ source .venv/bin/activate
    ```

4. **Install the dependencies:**

	 **Using [Docker](https://www.docker.com/) (Recommended):**

   Make sure you have Docker Engine, Docker Compose, and the NVIDIA Container Toolkit (for GPU support) installed.
   
   i. With GPU Support
   ```sh
   ❯ docker-compose up --build
   ```

   ii. Without GPU Support
	 ```sh
	 ❯ docker build -t Schryzon/Kanzeon-Backend .
	 ```

	 **Using [pip](https://pypi.org/project/pip/):**

   i. With GPU Support
	 ```sh
	 ❯ pip install -r requirements-cuda.txt
	 ```

   ii. Without GPU Support
   ```sh
   ❯ pip install -r requirements-nocuda.txt
	 ```

### Usage

Run the project with:

**Using [Docker](https://www.docker.com/):**
```sh
❯ docker run -it Schryzon/Kanzeon-Backend
```
**Using [pip](https://pypi.org/project/pip/):**
```sh
❯ python backend.py
❯ streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0
```

---

## Contributing

- **💬 [Join the Discussions](https://github.com/Schryzon/Kanzeon-Backend/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/Schryzon/Kanzeon-Backend/issues)**: Submit bugs found or log feature requests for the `Kanzeon-Backend` project.
- **💡 [Submit Pull Requests](https://github.com/Schryzon/Kanzeon-Backend/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details open>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   ❯ git clone https://github.com/Schryzon/Kanzeon-Backend
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   ❯ git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   ❯ git commit -m 'Implemented new feature!'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   ❯ git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details open>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/Schryzon/Kanzeon-Backend/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Schryzon/Kanzeon-Backend">
   </a>
</p>
</details>

---

## License

Kanzeon-backend is protected under the [MIT LICENSE](https://github.com/Schryzon/Kanzeon-Backend/blob/master/LICENSE) License. For more details, refer to the [LICENSE](https://github.com/Schryzon/Kanzeon-Backend/blob/master/LICENSE) file.

---

## Acknowledgments

- Thanks to `Selia` and `Xelisa` for teaching me how to make this! ❤️

<div align="center">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
