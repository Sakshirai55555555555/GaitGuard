# GaitGuard
This project is a gait classification system that analyzes human walking patterns using video input. It utilizes Deep learning to classify gait types and provides a Flask-based web interface for easy video uploads and result visualization.

# Dataset & Preprocessing

* **Dataset Used:** Custom dataset (MP4 videos)
* **Preprocessing Steps:**
    * Extracted frames from videos.
    * Applied background subtraction and silhouette extraction.
    * Resized and normalized images for uniform input.
    * Augmented data to improve model generalization.

#  Model
* **Model Architecture:**
    * CNN_LSTM
    * CNN_GRU
    * RNN
    * Autoencoder_classifier

# System Workflow overview          
* **The gait classification system follows a structured pipeline to analyze human walking patterns and provide meaningful insights. The key steps are:**
    * Video Input
       * Accepts pre-recorded video footage.
    * Pose Estimation (MediaPipe)
       * Extracts 33 joint positions using the MediaPipe framework
    * Feature Extraction
       * Calculates key gait features such as:
          * Joint Angles
          * Stride Symmetry
          * Torso Tilt & Step Length
    * Preprocessing
       * Cleans and prepares extracted data for model training.
    * Gait Classification Models
       * Uses a combination of CNN-LSTM Model ,  CNN-GRU ModeL , Autoencoder Model ,RNN
    * Majority Voting Mechanism
       * Combines predictions from all models to improve classification accuracy.
    * Gait Classification
       * Determines type of abnomalities (slouch , limping , circumduction , no_arm_swing , normal)
    * Real-Time Visualization & Feedback
       * Displays classification results dynamically.
    * Medical Recommendations
       * Provides guidance such as Physiotherapy Suggestions and Posture Correction

![Gait Classification System Flowchart](images/Gaitgurad_Documentation.jpg)

# Installation & Usage
* **Installation:**
    * Clone the repository:
       ```bash
      git clone https://github.com/Sakshirai55555555555/GaitGuard.git
      cd gait-classification
       ```
    * Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```
* **Usage:**
    ```bash
    python app.py
    ```
    * Open http://127.0.0.1:5000/ in the browser.
    * login / Signup
    * Upload a video file.
    * View result

# Results & Output
  * Sample output images
    ![Gait Classification output](images/deeplearning_output.jpg)
  * Confusion matrix
    ![confusion_matrix_1](images/confusion_matrix_1.png)
    ![confusion_matrix_2](images/confusion_matrix_2.png)
    ![confusion_matrix_3](images/confusion_matrix_3.png)
    ![confusion_matrix_4](images/confusion_matrix_4.png)
    
  * Accuracy/Loss plots
    
    ![accuracy_loss_1](images/accuracy_loss_1.png)
    ![accuracy_loss_2](images/accuracy_loss_2.png)
    ![accuracy_loss_3](images/accuracy_loss_3.png)

# Flask Web App
  * Users can upload gait videos through a simple web interface
  * The backend processes the video and classifies the gait type.
  * Results are displayed on the web app with visualizations.
    ![flask_1](images/flask_1.jpg)
    ![flask_2](images/flask_2.jpg)
    ![flask_3](images/flask_3.jpg)
    ![flask_4](images/flask_4.jpg)
    ![flask_5](images/flask_5.jpg)
    ![flask_6](images/flask_6.png)

# Contributors & Acknowledgments
  * Developer: Sakshi Rai , Ayushi Jaiswal , Chetna Chandra ,  Megha Kushwah    
  * Acknowledgments:
     * Research References:
        * "Classification of gait phases based on a machine learning approach using lower limb muscle synergy features": This study investigates the use of muscle synergy features for accurate gait event classification. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC10230056/)
        * "Gait classification for growing children with Duchenne muscular dystrophy": This research focuses on developing a valid gait classification for children with Duchenne muscular dystrophy.[Link](https://www.mdpi.com/1424-8220/24/17/5571)
        * "Machine Learning Based Abnormal Gait Classification with IMU Sensors Considering Joint Impairments": This study aims to develop an abnormal gait classification algorithm using inertial measurement units and walkway systems.[Link](https://www.mdpi.com/1424-8220/24/17/5571)
  * AI Assistance:
     * Portions of this project were assisted by OpenAI's ChatGPT. For guidelines on citing AI tools like ChatGPT in APA style, refer to the [APA Style Blog](https://apastyle.apa.org/blog/how-to-cite-chatgpt)

# Future Improvements
  * Improve model accuracy with a larger dataset.
  * Add real-time gait classification.
  * Implement user authentication for personalized results.


    
