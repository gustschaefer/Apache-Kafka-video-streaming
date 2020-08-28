# Kafka-distributed-video-streaming

Transmissão de vídeo utilizando kafka/zookeeper e fazendo seu processamento com opencv-python.
O Kafka producer é responsável por efetuar a conversão das frames do video para o formato de imagem .jpg,  enviá-los para algum determinado tópico e publicar o vídeo (formato base64). O consumer, acessa o tópico e cria o app web para mostrar a tranmissão do vídeo. Além disso, o ele também decodifica cada frame para o formato original e, utilizando o algoritimo de detecção de faces haar cascades, classifica cada frame contendo face ou não. Se o frame contém um rosto, ele é salvo no banco de dados mongodb junto com:

- Bounding Box
- Timestamp
- Número do frame

A estrutura do elemento no mongodb segue o molde:

 ```python
 {
	"face": b64_img,
	"frame": frame,
	"boundingbox": boundingbox_coords,
	"timestamp": timestamp
} 
``` 

## Instalação

Para utilizar o projeto é importante que você esteja em uma **maquina Linux**.

1. Instação do kafka

2. Instalção do mongodb
3. Bibliotecas python necessárias

## Como o projeto funciona

O algoritimo haar cascades utilizado funciona com maior precisão em rostos detectados **frontalmente**. Após detectar um rosto, o seu bounding box é gravado na imagem, como mostrado abaixo.

<p align="center">
  <img src="./screenshot/fronta_face_haar_ex.jpeg">
</p>

Enquanto o kafka consumer está lendo o vídeo, as funções do programa **haarcascade_mongo.py** interpretam os frames e classificando se possue um rosto ou não. Se um rosto for detectado na imagem, imediatamente a data e hora em que o evento ocorreu são salvas (timestamp), juntamente com seu boundingbox e número do frame. O mais importante de tudo é salvar a imagem e suas informações no banco de dados, entretanto elas também são salvas em uma pasta apenas para obter uma visualização mais estética do desempenho do programa. 

<p align="center">
  <img src="./screenshot/faces_folder_ex.jpeg">
</p>

Frames sem rostos detectados são apenas salvos na pasta "not_face", porém é um processo opicinal.

<p align="center">
  <img src="./screenshot/not_face_folder.jpeg">
</p>

Utilizando o programa **extract_from_database.py** é possível visualizar às imagens no mongodb. Uma opção é visualizar quais são os frames com faces que foram detectados, juntamente com o seu formato dentro do mongodb (base64) e seu formato após o ser decodificada. ```python from extract_from_database import decode_img```

<p align="center">
  <img src="./screenshot/types_extract.jpeg">
</p>

Também é possível ver o elemento no mongodb em seu format 'raw'.

<p align="center">
  <img src="./screenshot/elementoNomongo.jpeg">
</p>


