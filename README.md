# AICA - FoodTech Project

AICA is an innovative foodtech project that enables users to calculate calorie intake simply by taking a photo of their food. This system leverages computer vision, depth sensing, and machine learning to analyze food volume and estimate calorie content accurately.

---

## System Overview

The AICA system consists of several components: 

1. **Image Capture**: Captures food photos, including depth information when using devices with LiDAR sensors (such as the iPhone).
2. **Preprocessing and Segmentation**: Processes images to segment the food items from the background.
3. **Food Recognition**: Identifies different types of food in the image.
4. **Volume Estimation**: Uses depth data to accurately calculate the volume of food items.
5. **Calorie Estimation**: Estimates calories based on recognized food type and calculated volume.
6. **Result Display**: Presents calorie data and other nutritional information to the user.

---

## ML System Design

### 1. **Image Capture and Depth Sensing**

   - **Input**: User captures an image of the food with a compatible device.
   - **Depth Sensing**: For devices with LiDAR (iPhones), captures depth information to enhance accuracy in volume estimation.

### 2. **Image Preprocessing**

   - **Purpose**: Standardizes the input image and isolates food items.
   - **Steps**:
      - Resize and normalize the image.
      - Apply image filters and denoising.
      - Segment food from the background.

### 3. **Food Segmentation and Classification**

   - **Model**: A deep learning-based food classification model (e.g., ResNet, Inception).
   - **Process**:
      - Detects individual food items in the segmented image.
      - Classifies each item based on a predefined food category list.

### 4. **Volume Estimation**

   - **LiDAR Integration**: For iPhones, uses LiDAR depth information to estimate food volume accurately.
   - **Alternative Devices**: For devices without LiDAR, approximates volume based on image dimensions and assumed standard distances.

### 5. **Calorie Estimation**

   - **Food Database**: Contains average calorie content and nutrition information for various foods.
   - **Calculation**:
      - Retrieves calorie density (calories per unit volume) for each identified food item.
      - Combines calorie density with volume estimates to calculate total calorie content.

### 6. **User Interface and Display**

   - **Output**: Displays the estimated calorie count and nutritional breakdown.
   - **Customization**: Allows users to adjust serving sizes or add ingredients for more accurate tracking.

---

## ML System Design Diagram

Below is a system design diagram for the AICA calorie estimation process:

![ML System Design for AICA](diagram.png)

---

### Diagram Breakdown

1. **User Input**: The user takes a photo of their food.
2. **Preprocessing**: The system cleans, resizes, and segments the image.
3. **Segmentation and Classification**: Identifies food types in the image.
4. **Volume Estimation**: Calculates the volume of each food item using depth data.
5. **Calorie Estimation**: Combines food type and volume for calorie estimation.
6. **Result Display**: Shows calorie and nutrition info on the user’s screen.

---

## Future Enhancements

- **Database Expansion**: Add more food types and calorie density data.
- **Multi-language Support**: Expand the user base with localization.
- **Integration with Health Apps**: Sync data with other health-tracking apps.

---

This README provides an overview of the AICA ML system design for developers and contributors. It covers the major components, their functions, and a visual diagram for a quick reference to the calorie estimation workflow.

---
