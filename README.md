# Varimi
# BitMari Smart Farm Contracts 

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/lightningnetwork/lnd/blob/master/LICENSE) 


A platform for agriculture [smart contracts](https://en.wikipedia.org/wiki/Smart_contract) based on the [NEO blockchain](https://neo.org/) . 
[BitMari](https://www.bitmari.com) is building an infrastructure to support smart contracts  in agriculture as well as lower barrier for developers to code blockchain smart contracts. This comes after over 2 years of research work and working with women farmers in Zimbabwe, Africa.

## Proposed system architecture 

<img src="https://github.com/BitMari/varimi/blob/master/assets/proposed%20system%20architecture.png" alt="BitMari Smart Farm Contracts" width="620">

[Demo Farm Project Listing UI](https://www.bitmari.com/smartfarmcontract/public/project)

## Getting Started

To test develop and deploy your NEO python smart contracts on your local machine you will have to setup the environment by following the tutorial link below.
This will setup a private network of the neo blockchain and a wallet with NEO and GAS to test with.

## Installation

1. [NEO Dev Environment Setup Tutorial](https://medium.com/@nickfujita/neo-dev-environment-setup-tutorial-e495f5364ada)
2. [NEO Smart Contracts Tutorial: Creating your first helloWorld](https://medium.com/@nickfujita/neo-smart-contracts-tutorial-helloworld-13ecc19b31fe)

## Usage

Compiling the contract into an .avm file 

```build smartContracts/helloWorld.py```

Importing the contract .avm file 

```import contract ./smartContracts/helloWorld.avm "" 01 False False```

Invoking the contract

```contract search CONTRACT_NAME```

In our case 
```contract search helloWorld```

Run a testinvoke on the contract
```testinvoke CONTRACT_HASH```

## Roadmap 

[Press Release](https://medium.com/@bitmari_/bitmari-to-launch-smart-farm-contracts-to-aid-in-agricultural-funding-in-africa-based-on-the-neo-8df26f0b3347)
 

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.


## Acknowledgments

[@nickfujita](https://medium.com/@nickfujita) for NEO Setup Tutorials 


