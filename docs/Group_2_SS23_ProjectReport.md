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

| Member              | MatrNr. | Uni-Mail                            |
| ------------------- | ------- | ----------------------------------- |
| Vincent Roßknecht   | 1471764 | vincent.rossknecht@stud.fra-uas.de  |
| Jonas Hülsmann      | 1482889 | jonas.huelsman@stud.fra-uas.de      |
| Ekrem Bugday        | 1325425 | ekrem.bugday@stud.fra-uas.de        |
| Marco Tenderra      | 1251463 | tenderra@stud.fra-uas.de            |
| Minh Kien Nguyen    | 1434361 | minh.nguyen4@stud.fra-uas.de        |
| Alexander Atanassov | 1221846 | alexander.atanassov@stud.fra-uas.de |

**Source Code**: [Link](https://github.com/ccfrauasgr2/pet-detection/tree/main)

**Presentation Slides**: [Link](https://docs.google.com/presentation/d/1wE96Q1euAeaRYBAPP1TrVFQCkrlQES2NmLTt2wVjyIs/edit?usp=sharing)

**Hardware**:
- 1 Raspberry Pi 4 Model B with 32 GB MicroSD
- 4 Raspberry Pi 3 Model B with 4x 32 GB MicroSD
- 1 Apple charger with USB-C to USB-C
- 1 Anker PowerPort with 6 Ports
- 2 TP-Link TL-SG105 5 Port Desktop switch
- 6 Lan Cable
- 4 CoolReal USB-C to USB-C Cable

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
    id16[Import\nModel]:::_sensornode
    
    
    id11 --> id12
    id13 & id16 --> id14 --> id15
    end

    subgraph Jonas, Kien, Ekrem
    id21[Set up\nRaspberry Pi 3]:::_cluster
    id22[Set up\nk3s Kubernetes Cluster]:::_cluster
    id23[Set up\nDatabase in Cluster]:::_cluster
    id24[Develop\nREST API]:::_api

    id21 --> id22 --> id23
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

## Set up Raspberry Pi 4
- Insert an empty SD-Card into local PC
- Install then run [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on local PC
- In the Raspberry Pi Imager:
  - For Operating System, select Raspberry Pi OS (32-bit/64-bit)
  - For Storage, select the inserted SD-Card
  - In Advanced options (Cog icon):
    - Set `pi0` as hostname
    - Set `admin` as username
    - Enable `Enable SSH` and `Use password authentication` options. This allows for remote access and control of Raspberry Pi 4 via SSH from local PC. 
    - Enable `Configure wireless LAN` option, then add network details so that Raspberry Pi 4 will automatically connect to the network
  - Write to SD-Card
- [Connect](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3) and [Start up](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/4) Raspberry Pi 4 with SD-Card
- [SSH into Raspberry Pi](https://www.makeuseof.com/how-to-ssh-into-raspberry-pi-remote/#:~:text=SSH%20Into%20Raspberry%20Pi%20From%20Windows&text=In%20the%20PuTTY%20dialog%2C%20select,the%20connection%20details%20in%20PuTTY.) 4 from local PC with the command `ssh admin@pi0.local`
- SSH only provides *terminal* access to Raspberry Pi 4. To *remotely control the desktop interface* of Raspberry Pi 4, we use VNC (Virtual Network Computing). To enable VNC connection:
  - First, enable VNC Server on Raspberry Pi 4. SSH into Raspberry Pi 4 from local PC, then enter `sudo raspi-config`. Now with the arrows select `Interfacing Options`, navigate to `VNC`, choose `Yes`, and select `Ok`.
  - Install [Real VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/) on local PC
  - Open local VNC Viewer, enter `pi0.local:0` or `[IP address of Raspberry Pi 4]`. To find the IP address of Raspberry Pi 4, SSH into Raspberry Pi 4 from local PC, then enter `hostname -I`.
  - Enter login credentials that were set while configuring Raspberry Pi Imager.
  - The VNC session should start, and the Raspberry Pi desktop should be available.

# Cluster

The following questions have to be answered:

- What is the general purpose of the component?
- Which tools/service/tech stacks were used and why?
- How were these used to achieve the general purpose?
- Example Results
- Known problems and improvement suggestions

## Set up Raspberry Pi 3

- Follow the steps listed in [Set up Raspberry Pi 4](#set-up-raspberry-pi-4)
- Set `pi[1|2|3|4].local` as hostname for each of four available Raspberry Pi 3

## Set up k3s Kubernetes Cluster

## Set up Database in Cluster

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



