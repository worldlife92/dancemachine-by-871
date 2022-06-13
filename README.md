# Data analysis
- dancemachine Video Classification
- Description: Goal of the project is to create a deep learning model which can learn a tiktok dance and correctly classify new videos based on whether the taught dance is included in the video or not.
- Data Source: Tiktok Videos / Specifically the jiggle jiggle dance
- Type of analysis: We extract the body poses from the TikTok videos by leveraging the MediaPipe package, specifically it's body pose component to extract the landmarks from the video. Using the landmarks extracted from the body poses we calculcate the angles between key joints to adjust for height differences and as the landmark coordinates are only given relative to the image size. Lastly a tensorflow RNN model is trained based on 120 Tiktok videos (40 correct, 60 incorrect dances).

This project has been created as part of the LeWagon data science bootcamp by @DucVanNgo, @wanliammar, @worldlife92 and @DominiqueSch
