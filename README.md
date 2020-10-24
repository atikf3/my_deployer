# my_deployer *unfinished*
The main goal of this project is to create a handy, automated deployment tool based on SSH.  
To put it simply, it will have to deploy Docker containers on a remote host, and therefore configure it appropriately beforehand.

Your project will consist of a script providing a CLI with multiple subcommands to manage the services on the remote host:

*   `config`: configure the remote host
*   `build`: build Docker images for the services
*   `deploy`: deploy the services
*   ~~`healthcheck`: ensure the services are running properly~~

The script may be able to import or call other Python scripts you wrote, to implement a form of modularity in your project. The script shall be executed on your machine, and will target a remote server through its IP address (for example, a Debian 10 "Buster" VM running on your workstation).

> The following steps may or may not have interdependencies, do not hesitate to keep on going with the main subject if you ever happen to be stuck at a specific step.

### Restrictions
*   Python 3.7 is mandatory.
*   Use of any existing orchestration / deployment software is prohibited.
*   Everything made by your script must have a local scope, any third-party interaction (SaaS) is strictly forbidden.

### Recommendations
This project will not only evaluate the functional aspect, but also the quality of your delivery.  
Therefore, the following recommendations should be kept in mind during the entire project.

Your project must:

*   Fit-in with the clean Python code principles (use of linters and formatters is encouraged)
*   Be autonomous: once started, the script must not require any additional interaction from the user
*   Be autocorrective: running the same command twice must not generate any warning or error (if there is nothing to do, do nothing)
*   Be thoroughly documented
*   Log detailed, informative data about its execution

## Ysage
```bash
python3 my_deployer.py -h
```

## Additional Data
**Contributors:**
[talamo_a](//www.talamona.com)

**License:**
[MIT](./LICENSE)