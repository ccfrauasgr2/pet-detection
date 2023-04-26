TODO: Table of contents

# Overview

**Introduction**: The project *Automatic Pet Detection With Edge Computing* is part of the Cloud Computing SS23 module of Prof. Dr. Christian Baun at the Frankfurt University of Applied Sciences. Further information about the module can be found [here](https://www.christianbaun.de/CGC23/index.html).

**Objective**: This project aims to develop an edge computing solution for the automatic detection of cats, dogs, golden hamster. General steps to achieve the project goal are:
- Set up a Sensor Node (Raspberry Pi 4) with Camera Modules
- Train a Model to Detect Pets
- Deploy the Trained Model on the Sensor Node
- Set up a Cluster of Raspberry Pi 3 Nodes
- Set up a Database for Storing Detection Results 
- Develop a WebApp for Displaying Detection Results
- Develop API Connection Between the Sensor Node, Cluster & WebApp
- Test Full System

**Duration**: 12.04.2023 - 05.07.2023

**Group 2**:

| Member              | MatrNr. | Uni-Mail                     |
| ------------------- | ------- | ---------------------------- |
| Vincent Roßknecht   |         |                              |
| Jonas Hülsmann      |         |                              |
| Ekrem Bugday        |         |                              |
| Marco Tenderra      |         |                              |
| Minh Kien Nguyen    | 1434361 | minh.nguyen4@stud.fra-uas.de |
| Alexander Atanassov |         |                              |

**Source Code**: [Link](https://github.com/ccfrauasgr2/pet-detection/tree/main)

**Presentation Slides**: [Link](https://docs.google.com/presentation/d/1wE96Q1euAeaRYBAPP1TrVFQCkrlQES2NmLTt2wVjyIs/edit?usp=sharing)

**Hardware**:

**System Architecture**:

**System Behavior**:

TODO: Sequence Diagram

**Project Plan & Task Distribution**:
```mermaid
flowchart TD
    
    subgraph Marco & Vincent
    id11[Set up\nRaspberry Pi 4]:::_sensornode
    id12[Set up\nCamera Modules]:::_sensornode
    id13[Prepare\nTraining Data]:::_sensornode
    id14[Train & Validate\nModel]:::_sensornode
    id15[Deploy\nTrained Model]:::_sensornode
    
    
    id11 --> id12
    id13 --> id14 --> id15
    end

    subgraph Jonas, Kien, Ekrem
    id21[Set up\nCluster of Raspberry Pi 3]:::_cluster
    id22[Set up\nDatabase in Cluster]:::_cluster
    id23[Develop\nREST API]:::_api

    id21 --> id22
    end

    subgraph Alex
    id31[Develop\nWebApp]:::_webapp
    end
   
 

    subgraph Topics
    id01[Sensor Node]:::_sensornode
    id02[API]:::_api
    id03[Cluster]:::_cluster
    id04[WebApp]:::_webapp
    end
   

    classDef _sensornode fill:#ea4335,color:#ffffff,stroke-width:2px,stroke:#000000
    classDef _cluster fill:#4285f4,color:#ffffff,stroke-width:2px,stroke:#000000
    classDef _api fill:#fbbc05,color:#ffffff,stroke-width:2px,stroke:#000000
    classDef _webapp fill:#34a853,color:#ffffff,stroke-width:2px,stroke:#000000
```




# Sensor Node

The following questions have to be answered:

- What is the general purpose of the component?
- Which tools/service/tech stacks were used and why?
- How were these used to achieve the general purpose?
- Example Results
- Known problems and improvement suggestions

# Cluster

The following questions have to be answered:

- What is the general purpose of the component?
- Which tools/service/tech stacks were used and why?
- How were these used to achieve the general purpose?
- Example Results
- Known problems and improvement suggestions

# Database

The following questions have to be answered:

- What is the general purpose of the component?
- Which tools/service/tech stacks were used and why?
- How were these used to achieve the general purpose?
- Example Results
- Known problems and improvement suggestions

# WebApp

The following questions have to be answered:


- What is the general purpose of the component?
- Which tools/service/tech stacks were used and why?
- How were these used to achieve the general purpose?
- Example Results
- Known problems and improvement suggestions

##SetUp Raspberry Pi
- Install PI-Imager
- Insert SD-Card into SD-Card reader
- Select Operating System Raspberry Pi OS(32-bit/64-bit)  and SD-Card in PI-Imager
- Configure PI-Name as pi[none/1/2/3/4]
- Configure User name as Admin
- Select create SSH option
- Configure WiFi to AndroidAP
- Write to SD-Card
- Start Raspberry Pi with SD-Card
- ssh from Windows into the PI with admin@[ip-adress or pi-name.local]
- sudo raspi-config -> interface -> VNC -> Enable
- Install VNC view on Windows
- Create new connection with IP adress from PI
- Connect and first time accept certificate

