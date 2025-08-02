# IoT-gemios-digitais

Trabalho de Graduação desenvolvido para a obtenção do diploma de Engenheiro Electrico da Universidade Zambeze (UZ), no qual consiste na construção de um Gêmeo Digital para motores elétricos. Os arquivos aqui presentes são os códigos para a IDE do Arduino, utilizados para a leitura dos dados dos sensores conectados a um microcontrolador, e os dados do projeto desenvolvido no ScadaBR, o sistema supervisório responsável por monitorar as variáveis tanto dos sensores quanto do inversor de frequência CFW-08 que realiza o acionamento/controle de velocidade e torque do motor.

Leitura de Dados
Apesar do inversor de frequência conseguir disponibilizar diversas informações dos motores, existem outros dados que não são possíveis de serem obtidos por meio dele. Por isso, definiu-se controladores e atuadores para capturar estes valores. Entretanto, primeiramente, era necessário definir quais informações além das que o inversor fornece seriam necessárias para a construção do modelo virtual de um motor. Chegou-se à conclusão de que 3 informações importantes para a modelagem do motor estavam faltando, sendo elas a temperatura externa da carcaça, o ruído emitido pelo motor e a vibração nos 3 eixos.

O microcontrolador utilizado neste trabalho foi o ESP32, juntamente com o sensor de temperatura DS18B20, o módulo sensor de som KY-038 e o acelerômetro MPU-6050. O código arduino aqui disposto usa as bibliotecas modbus-esp8266, Adafruit_MPU6050, Adafruit_Sensor e DS18B20. Portanto, você precisará instalá-los usando o Library Manager no Arduino IDE ou baixar a versão mais recente do GitHub. Porteriormente, para funcionar o código basta conectar o ESP32 juntamente com os sensores ao computador via cabo USB, compilar e executar.

A conexão entre o ESP32 e os sensores segue conforme mostrado no diagrama esquemático a seguir

<img width="1509" height="801" alt="image" src="https://github.com/user-attachments/assets/a697bd40-a325-4e5a-a17d-2e4b4f85aa4a" />
