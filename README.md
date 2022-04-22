# vcsd-car
voice control, self driving car using raspberry pi
## There are three modules
- Self driving AI
- voice control
- obstacle detection

## Self Driving AI
- original picture
  ![Orignial Picture](https://i.imgur.com/RDtfiUl.png)
- masked lanes
  ![Masked Picture](https://imgur.com/hYQteWN.png)
- grayscale
  ![Grayscale Picture](https://imgur.com/s12hP6e.png)
- canny edge
  ![Canny edge Picture](https://imgur.com/C5SDS9D.png)

## Voice Control
There were total of 14 commands
- Start
- Stop
- Change lane
- Turn left
- turn right
- speed up
- speed down
- chalo
- ruk jao
- lane badlo
- bayain muro
- dayain muro
- tez chalo
- ahista chalo

### BiLSTM evaluation for above command
![BiLSTM eval](https://imgur.com/e1OQ1NV.png)
### BiLSTM confusion matrix
![Confusion matrix](https://imgur.com/cTdKmre.png)

## Obstacle Detection
We are using Ultrasonic sensor to detect obstalces
![Ultrasonic sensor](https://imgur.com/FPdrN3f.png)

## Overall architecture
![hardware architecture](https://imgur.com/SfQBGNq.png)

