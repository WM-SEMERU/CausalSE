<<<<<<< HEAD
FROM tensorflow/tensorflow:2.3.0-gpu-jupyter

# ADD ./requirements.txt .

# RUN pip install -r requirements.txt
ENV PATH="/.local/bin:${PATH}"

RUN mkdir .cache
RUN apt-get update -y && apt-get install git wget -y
=======
FROM tensorflow/tensorflow:2.4.0-gpu-jupyter

# ADD ./requirements.txt .

ENV PATH="/.local/bin:${PATH}"

RUN mkdir .cache
RUN apt-get update -y && apt-get install git wget python3.7 -y
RUN pip install nbdev pre-commit
>>>>>>> 4140f24734dc43a0cec843110b40849f867f6944

EXPOSE 8888 6006
