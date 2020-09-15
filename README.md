
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/thegc/gclib/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/gc.svg)](https://badge.fury.io/py/gc)
[![CircleCI](https://img.shields.io/circleci/project/github/thegc/integration_tests/master.svg?label=integration)](https://circleci.com/gh/thegc/integration_tests)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/e3070763b579456380822b2909259070)](https://www.codacy.com/app/gc/gc?utm_source=github.com&utm_medium=referral&utm_content=thegc/gc&utm_campaign=Badge_Coverage) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e3070763b579456380822b2909259070)](https://www.codacy.com/app/gc/gc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=thegc/gc&amp;utm_campaign=Badge_Grade)
[![codebeat badge](https://codebeat.co/badges/5748b416-7398-4d08-8b49-e4285ef9a82d)](https://codebeat.co/projects/github-com-thegc-gc-master)


# GC - BlockChain Ledger 

> Python-based blockchain ledger utilizing hash-based one-time merkle tree signature scheme (XMSS) instead of ECDSA. Proof-of-work block selection via the cryptonight algorithm. Future transition to POS with signed iterative hash chain reveal scheme which is both probabilistic and random.
>
> Hash-based signatures means larger transactions (3kb per tx, binary), longer keypair generation times and the need to record 'state' of transactions as each keypair can only be used once safely. Merkle tree usage enables a single address to be used for signing numerous transactions (up to 2^13 computationally easily enough). Currently XMSS/W-OTS+ are natively supported with extensible support for further cryptographic schemes inbuilt. 

# Documentation


## GC Node


Running a GC node strengthens the network, supports the decentralization and further verifies transactions on the network. This is an essential function of the decentralized architecture GC relies on.This allows you to run a private secure node to communicate with the GC blockchain.You can use the node to connect the explorer, wallet, and ephemeral messaging features to the gRPC GC functions.


> There are various options available for connecting to the API and setup options for the node can be configured through a user set configuration file.

#### Requirements


You can run GC on most operating systems, though Ubuntu 16.04 is recommended.
- Support for AES-NI
- Support for avx2 (Used by keccak library for hashing functions)
- HDD with enough storage for the blockchain as it grows
- Reliable network connection
- Python3.6
- 64 bit processor


Abridged instructions for installing GC on Ubuntu:

```
# Update and Upgrade packagessudo apt update && sudo apt upgrade -y

# Install Required dependenciessudo apt-get -y install swig3.0 python3-dev python3-pip build-essential pkg-config libssl-dev libffi-dev libhwloc-dev libboost-dev

## Install CMAKE version 3.10.3 manuallycd /opt && sudo wget https://github.com/Kitware/CMake/releases/download/v3.10.3/cmake-3.10.3.tar.gz && sudo tar zxvf cmake-3.10.3.tar.gz && cd cmake-3.10.3/ && sudo ./configure && sudo make -j2 && echo -e '## Adding cmake version 3.10.3\nPATH=$PATH:/opt/cmake-3.10.3/bin' >> ~/.bashrc && source ~/.bashrc

# Make sure setuptools is the latest
pip3 install -U setuptools

# Install GC
pip3 install -U gc
```


If things worked correctly you will now find the?start_gc?package and the?gc?package. Adding the?--help?flag to each will print the various function details.



#### Getting Started


Installing GC is simple, and is possible on most modern operating systems. The install relies on?python3.5?or newer and the?pip3?python package install system.


**Update and Dependencies**

You will need to start with a fully updated system. You will also need a few additional packages depending on your setup. See the correct section for your OS and install all of the requirements.


##### Ubuntu


Update your system ensuring you have the latest packages:

```
# Issue the following command to update software
sudo apt update && sudo apt upgrade -y
```


Now install all the required dependencies:

```
# Install the required packages for GC
sudo apt-get -y install swig3.0 python3-dev python3-pip build-essential pkg-config libssl-dev libffi-dev libhwloc-dev libboost-dev
```


GC requires?cmake v3.10.3?to be installed. Ubuntu repositories will install an incompatible version. Please install manually as shown below. If you already have?cmake?installed, please uninstall first.

```
# Install the required packages for GC
cd /opt && sudo wget https://github.com/Kitware/CMake/releases/download/v3.10.3/cmake-3.10.3.tar.gz && sudo tar zxvf cmake-3.10.3.tar.gz && cd cmake-3.10.3/ && sudo ./configure && sudo make -j2 && echo -e '## Adding cmake version 3.10.3\nPATH=$PATH:/opt/cmake-3.10.3/bin' >> ~/.bashrc && source ~/.bashrc
```

##### Redhat/fedora

Update:

```
# Update
dnf update
```

Dependencies:

```
# Install required packages
dnf install swig cmake gcc gcc-c++ redhat-rpm-config python3-devel python-devel hwloc-devel boost-devel
```

You will need to install?cmake v3.10.3?manually.
[Please follow the guide from the cmake documentation](https://cmake.org/install/)

##### MacOS

To build in OSX Please install?brew?if you have not already.

```
# Install brew with
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" 
```

This will prompt you through a few questions while it installs.Having Issues? Please follow the instructions found at the brew main page:?[https://brew.sh/](https://brew.sh/)

```
# Update brew
brew update
brew install python3 swig boost hwloc
```

You will need to install?cmake v3.10.3?manually.

[Please follow the guide from the cmake documantation](https://cmake.org/install/)

##### Windows 10

Windows support in the current version is limited. An alternative is to install Ubuntu using the Linux Subsystem for Windows.

###### Ubuntu on Linux Subsystem for Windows (WSL)


You can run a full node in Windows utilizing the Windows Subsystem for Linux. There are a ton of guides out there on setting this up. Here are a few links to get you going.The Windows Subsystem for Linux (WSL) is a new Windows 10 feature that enables you to run native Linux command-line tools directly on Windows, alongside your traditional Windows desktop and modern store apps.You can [follow?these](https://msdn.microsoft.com/en-us/commandline/wsl/install-win10) instructions?to install Ubuntu using Linux Subsystem,

###### Links - Installing Ubuntu in Windows 10
[Windows Subsystem for Linux Documentation](https://docs.microsoft.com/en-us/windows/wsl/about)

[Google Is Your Friend (install+ubuntu+in+windows+10)](https://www.google.com/search?hl=en&as_q=install+ubuntu+in+windows+10&as_epq=)

[WSL Blog](https://blogs.msdn.microsoft.com/wsl/)


#### Install GC

Now that we have a freshly updated system, the installation of GC is a breeze, GC uses python3 to install. The install is the same for all operating systems after you have installed the requirements. Using the Python3 package installer?pip3?we will install GC.

Before we install GC make sure setupTools is the latest.

```
pip3 install -U setupTools
```

After this completes install GC with:

```
pip3 install -U gc
```

This will install the GC package and any required dependencies.

#### Start GC Node

Now that we have GC installed we can?start_gc?and begin syncing the node. This will begin the node in the foreground of the shell. If you would like to continue using the shell you can either pass the?--quiet?flag or run the command in a?screen?session ( you will need screen installed ).

```
start_gc
```


This will print out the details of the running GC processes. For a more verbose output you can pass the?-l?option with?DEBUG, INFO,WARNING,ERROR,CRITICAL?depending on the level of information you need.

```
start_gc-l DEBUG
```

The node will sync the entire blockchain to your computer, make sure you have enough space. after syncing the chain you will begin seeing blocks added. Congrats, your GC node is working.

###### Help

If you would like to see all of the options you can pass along the command line simply add?--help?to the end of the command above.

```
start_gc--help
```

This will print all of the various options available.

```
usage: start_gc [-h] [--mining_thread_count MINING_THREAD_COUNT] [--quiet]
                 [--gcdir GC_DIR] [--no-colors]
                 [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [--network-type {mainnet,testnet}]
                 [--miningAddress MINING_ADDRESS]
                 [--mockGetMeasurement MEASUREMENT] [--debug] [--mocknet]

GC node

optional arguments:
  -h, --help            show this help message and exit
  --mining_thread_count MINING_THREAD_COUNT, -m MINING_THREAD_COUNT
                        Number of threads for mining
  --quiet, -q           Avoid writing data to the console
  --gcdir GC_DIR, -d GC_DIR
                        Use a different directory for node data/configuration
  --no-colors           Disables color output
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
  --network-type {mainnet,testnet}
                        Runs GC Testnet Node
  --miningAddress MINING_ADDRESS
                        GC Wallet address on which mining reward has to be
                        credited.
  --mockGetMeasurement MEASUREMENT
                        Warning: Only for integration test, to mock
                        get_measurement
  --debug               Enables fault handler
  --mocknet             Enables default mocknet settings
```

#### Configuration


By default when the node is started it will?**NOT**?mine any coins. You will have to enable using a configuration file in the?~/.gc/?directory.

The configuration file is where you will change any options you want GC to observe. You can grab a copy of the file and details about all of the settings in our?Configuration GuideThe defaults can be used to run a GC node, though you may need to change some of the directives for your use.

#### Mining GC
> If you want to mine using a GC node, see the guide for?Mining GC Solo?or the?pool guide?to get started.

## Mining with a GC Node


You can setup a GC mining node on a PC or server. This will allow you to mine GC while also running a node on the GC network. You simply need to enable mining on the GC node in a config file to begin mining GC.

 **Requirements**
 - GC installed and fully synced
 - GC Wallet to send rewards to
 - A little time to set it up
 - Local or remote shell connection (ssh)
 
 
>This write-up assumes that you have a fully functioning GC node running and fully synced with the blockchain. If you need to, see the guide at?docs.thegcorg/node/GCnode


While connected to the computer running gc you can see the state of the node by entering?gc state?into the command line. This will print out the blockheight of the local node as well as some other information. Check that this is the same height as the?GC explorer?shows.Once fully synced you can start mining by editing the config file found in?~/.gc/config.yml?enabling mining.


#### Configuration


To begin mining you will need to create and edit a file located in the default GC directory?~/.gc/config.yml. There are a ton of configurations and settings you can tweak, however for this guide we are only concerned with the mining settings.


> For a complete guide of the configuration settings, please see the?GC Node Configurations?guide.


Create the config file and add these settings to the file if not already created.

```
nano ~/.gc/config.yml 
```

```
# ======================================
#    Mining Configuration
# ======================================
# mining_enabled: False# mining_address: ''
# mining_thread_count: 0  
# 0 auto detect thread count based on number of processors
#
```

These are the default settings the node is currently using. Change the values and remove the # to begin mining.

> You need to enter a valid GC address, change the?False?value to a?True?value, and set the thread count if you want to adjust.


Once you have made your changes the file will look something like this.

> Note the GC address shown needs to be replaced, unless you want to donate some quanta!

```
# ======================================
#    Mining Configuration# ======================================
 mining_enabled: True
 mining_address: 'GC1F2c4stA5qtwL2kWFoVxmqwqzYpn8kjP8P'
 mining_thread_count: 0  # 0 to auto detect thread count based on CPU/GPU number of processors
 #
```

#### Restart GC


Restart the gc node to begin mining with the new changes.

```
start_gc 
```


Once the node re-syncs with the network and catches up it will begin mining the current blocks on the chain You will see the rewards in the wallet you have specified in the configuration file.

You can also enter the following to print the state of the node


```
gc state 
```


* * *
