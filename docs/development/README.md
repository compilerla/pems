# Getting started with development

!!! info

    This guide will take you through the process of getting the [`pems`](https://github.com/compilerla/pems) project running in
    your local development environment.

    `pems` uses [VS Code devcontainers](https://code.visualstudio.com/docs/devcontainers/containers) to provide a
    platform-agnostic, standardized development environment.

    For more about why we use Dev Containers, check our Compiler's blog post:
    [_How to support a platform-agnostic engineering team with VS Code Dev Containers_](https://compiler.la/blog/2024/devcontainer-platform-agnostic-team).

## Prerequisites

This section describes the tooling you need to have installed and configured on your development machine before continuing.

### Git

Git is an open source version control system that we use in `pems` to track changes to the codebase over time. Many operating
systems come with Git already installed. Check if you have Git installed in a terminal with the following command:

```shell
git --version
```

If git is installed, the output should look similar to:

```console
$ git --version
git version 2.39.5
```

If Git is not installed, head to the [Git downloads page](https://git-scm.com/downloads) to get an installer for your operating
system.

### Docker and Docker Compose

Docker and Docker Compose (or just Compose) are key tools that allow for running the various services required for `pems`.

Confirm if you already have Docker installed, in a terminal:

```shell
docker --version
```

If Docker is installed, the output should look similar to:

```console
$ docker --version
Docker version 27.4.0, build bde2b89
```

And similarly to check if Compose is installed:

```shell
docker compose version
```

When Compose is installed, output will look similar to:

```console
$ docker compose version
Docker Compose version v2.31.0
```

There are different ways to acquire this software depending on your operating system. The simplest approach for Windows and
MacOS users is to install [Docker Desktop](https://docs.docker.com/desktop/).

??? warning "License requirements for Docker Desktop"

    Use of Docker Desktop is subject to [Docker's licensing terms](https://www.docker.com/legal/docker-subscription-service-agreement/).
    In particular, note that **Section 4.2** calls out government users specifically:

    > Government Entities shall not use Docker Desktop or access other Entitlements of the Service without purchasing a Subscription.

#### Windows

It is possible to run Docker and Compose on Windows without installing Docker Desktop. This involves using the [Windows Subsystem
for Linux v2 (WSL2)](https://learn.microsoft.com/en-us/windows/wsl/install#step-2-update-to-wsl-2), where Docker is configured
to run.

This article walks through this procedure in more detail:
[_How to run docker on Windows without Docker Desktop_](https://dev.to/_nicolas_louis_/how-to-run-docker-on-windows-without-docker-desktop-hik).

#### MacOS

With MacOS and [Homebrew](https://brew.sh/), installing Docker and Compose are as simple as:

```shell
brew install docker docker-compose colima
```

Once the install completes, start `colima` (an [open source container runtime](https://github.com/abiosoft/colima)):

```shell
brew services start colima
```

#### Linux

Docker CE (also known as Docker Engine) is how to run Docker and Compose on Linux. Docker provides an
[installation guide for Docker CE](https://docs.docker.com/engine/install/).

### VS Code and Dev Containers extension

VS Code is an open source Integrated Development Environment (IDE) from Microsoft. Check if you already have it installed:

```shell
code -v
```

If installed, output should look similar to:

```console
$ code -v
1.95.3
f1a4fb101478ce6ec82fe9627c43efbf9e98c813
x64
```

Otherwise, [download VS Code](https://code.visualstudio.com/download) for your operating system.

Once installed, open VS Code and enter `Ctrl`/`Cmd` + `P` to open the VS Code Quick Open pane. Then enter:

```console
ext install ms-vscode-remote.remote-containers
```

`ms-vscode-remote.remote-containers` is the Extension ID of the
[Dev Containers extension from Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

## Get the project code

Use Git to clone the repository to your local machine:

```shell
git clone https://github.com/compilerla/pems.git
```

Then change into the `pems` directory and create an environment file from the sample:

```shell
cd pems
cp .env.sample .env
```

Feel free to inspect the environment file, but leave the defaults for now.

## Run the build script

This builds the runtime and devcontainer images:

```shell
bin/build.sh
```

## Run the application

Start the application service with Compose:

```shell
docker compose up -d web
```

Start the streamlit application with Compose:

```shell
docker compose up streamlit
```

The `-d` flag starts the service in "detatched" mode, so your terminal is still available for additional commands. Without this flag, your terminal attaches to the service container's standard output.

The application is now running on `http://localhost:8000`.

Stop the running service with Compose:

```shell
docker compose down
```

## Open the project in a VS Code devcontainer

Still in your terminal, enter the following command to open the project in VS Code:

```shell
code .
```

Once the project is loaded in VS Code, you should see a notification pop-up that will ask if you want to reopen the project in
a devcontainer.

If you don't see this notification, or if you dismissed it, use the VS Code Quick Open pane with `Ctrl`/`Cmd` + `P` and enter:

```md
> Dev Containers: Rebuild and Reopen in Container
```

The VS Code window will reload into the devcontainer.

Once loaded, hit `F5` to start the application in debug mode. The application is now running on `http://localhost:8001`.

## Explore the devcontainer

This section describes other areas to explore within the VS Code devcontainer.

### Debugger

Open a Python file in the `pems/` directory and add a breakpoint by clicking the space next to a line number,
leaving a small red circle where you clicked.

Step through the running application on `http://localhost:8000` to trigger the code path you selected. Execution is paused
and VS Code allows you to inspect the runtime environment, context, etc.

### Integrated terminal

Press `Ctrl` + `~` to bring up the integrated `TERMINAL` window. You are now in a `bash` terminal running inside the
context of the devcontainer.

### Docs site

Open the `PORTS` tab to see port bindings for additional services. Look for the `Forwarded Address` of the `docs` service and
click to open the docs site in your browser, running on `localhost`.

Edit the documentation files in VS Code, and once saved, the local docs site will rebuild with the changes.

### Test runner

Use the VS Code Quick Open pane with `Ctrl`/`Cmd` + `P` and enter:

```md
> Testing: Focus
```

To focus on the `Testing` pane on the left side. Click the play button to run the unit tests.

## Work with the Cloud infrastructure

You can work on the app's Cloud infrastructure in the dev container by using the `aws` and `copilot` AWS CLIs. Successfully running the commands requires the container's host to be configured for authentication with IAM Identity Center by running `aws configure sso` and going through the setup. You can use the following settings:

- `SSO session name (Recommended): pems`
- `SSO start URL [None]: url_provided_by_caltrans`
- `SSO region [None]: us-west-2`
- `SSO registration scopes [None]:`
- `Default client Region [None]: us-west-2`
- `CLI default output format (json if not specified) [None]:`
- `Profile name [123456789011_ReadOnly]: pems`

An active SSO session must be available to run the AWS commands, if it is not, run `aws sso login` inside the container to start a session.

Running thes commands in the dev container is made possible by the mapping defined in the [compose file](https://github.com/compilerla/pems/blob/main/compose.yml#L23) that maps the host's AWS credentials folder to the dev container at `/home/caltrans/.aws`. For convenience, you can also set the default AWS profile that will be used in the dev container to `pems` as shown in [`.env.sample`](https://github.com/compilerla/pems/blob/main/.env.sample#L18).

### Useful commands

Deploying

- `copilot svc deploy -n service-name` to [deploy a service](https://aws.github.io/copilot-cli/docs/commands/svc-deploy/) (local code and configuration) that has already been initialized

Monitoring

- `copilot svc show -n service-name` to [see the environment variables and other information](https://aws.github.io/copilot-cli/docs/commands/svc-show/) associated with a service
- `copilot svc logs -n service-name --since 1h` to [see the logs](https://aws.github.io/copilot-cli/docs/commands/svc-logs/) for the past hour of a deployed service
- `copilot svc exec -a app-name -e environment-name -n service-name` to [gain shell access](https://aws.github.io/copilot-cli/docs/commands/svc-exec/) to a running container
