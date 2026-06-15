# Farm-Wide Wind Field Reconstruction from Sparse LiDAR Measurements via a Physics-Aware Spatiotemporal Diffusion Model

## 📖 Introduction
This repository contains the official implementation of our farm-wide wind field reconstruction framework. The framework is designed to reconstruct accurate, farm-wide spatiotemporal wind fields of wind farms using highly sparse measurements from long-range LiDARs.



## 🗄️ Dataset
The Large Eddy Simulation (LES) data of the wind farm were obtained from the Johns Hopkins Turbulence Database (JHTDB). 

The dataset is publicly accessible at: 
🔗 [https://turbulence.idies.jhu.edu/datasets/windfarms/diurnalWindfarm](https://turbulence.idies.jhu.edu/datasets/windfarms/diurnalWindfarm)

### Data Preparation
The complete pipeline for downloading, cleaning, and transforming the raw JHTDB data into formats ready for model training is provided in the `dataset_preparation/` directory. 

A sample of the processed dataset is available in the `dataset/` directory.



## 🎥 Demonstration
A demonstration video which illustrates the reconstruction process can be viewed at: 🔗 [https://datazyh.oss-cn-beijing.aliyuncs.com/wind-farm-recon-demo.mp4](https://datazyh.oss-cn-beijing.aliyuncs.com/wind-farm-recon-demo.mp4)

![image-20260615120211681](https://datazyh.oss-cn-beijing.aliyuncs.com/image-20260615120211681.png)



## 📊 Results

Below are dynamic visualizations of the wind fields reconstructed by our method using sparse LiDAR observations.

![sample1](https://datazyh.oss-cn-beijing.aliyuncs.com/sample1.gif)

![sample2](https://datazyh.oss-cn-beijing.aliyuncs.com/sample2.gif)



## 🚀 Future Updates

The code will be made available in this repository upon the acceptance of the manuscript. 