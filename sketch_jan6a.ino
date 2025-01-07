#include <EEPROM.h>
#include <ThreadController.h>
#include <TimerOne.h>
#include <Thread.h>

ThreadController controll = ThreadController();

Thread getserial_Thread = Thread();
Thread brk_check_Thread = Thread();

int encoderPin = A1;
int brk_pin = 4;                      
int dir_pin = 6;
int pwm_pin = 8;
int tail_light = 9;                   
int white_pin = 7;
int brk_button = 11;                  
int photo_pin = 13;                   
int test_pin = 11;
char c1='9';                              
float digitalValue;
short pwm =0;
short state=1;
float analogVoltage;                 

float START_VOLTAGE = 3.5; 
float END_VOLTAGE = 4.1; 

bool show = false;

void setup()
{       
  Serial.begin(9600);
  Serial1.begin(9600);
  
  pinMode(brk_pin, OUTPUT);
  pinMode(pwm_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);

  pinMode(white_pin, OUTPUT);
  pinMode(tail_light, INPUT);
  pinMode(brk_button, INPUT);
  pinMode(photo_pin, INPUT);
  pinMode(test_pin, INPUT);  
  
  digitalWrite(brk_pin, HIGH);
  digitalWrite(dir_pin, HIGH);
  digitalWrite(photo_pin, HIGH);
  digitalWrite(white_pin, LOW);

  EEPROM.get(0, START_VOLTAGE);
  EEPROM.get(sizeof(float), END_VOLTAGE);
  
  Serial.println("System ready. Enter commands to modify voltages:");
  Serial.println("START:<value> - Update START_VOLTAGE");
  Serial.println("END:<value> - Update END_VOLTAGE");
  Serial.println("SHOW - Display current voltages");
  Serial.println("STOP - STOP Display current voltages");

  getserial_Thread.onRun(getserial);
  controll.add(&getserial_Thread);

}




void loop()
{
  pwm=100;

  getserial();      

  if (c1 == '0') {
    release_pedal();
  }
  else if (c1 == '1') {
    push_pedal();
  }
  
  controll.run();
}

void encoder_voltage()                
{
  digitalValue = analogRead(encoderPin);
  analogVoltage = 5.0 - (digitalValue*5.00)/1023.00;
}

void encoder_voltage2()                
{
  digitalValue = analogRead(encoderPin);
  analogVoltage = 5.0 - (digitalValue*5.00)/1023.00;
  Serial.println(analogVoltage); 
}

void getserial()                     
{
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');  // 사용자 입력 읽기
    input.trim();  // 공백 제거

    if (input.startsWith("START:")) {
      START_VOLTAGE = input.substring(6).toFloat();  // 값 추출
      EEPROM.put(0, START_VOLTAGE);  // EEPROM에 저장
      Serial.print("START_VOLTAGE updated to: ");
      Serial.println(START_VOLTAGE);
    } else if (input.startsWith("END:")) {
      END_VOLTAGE = input.substring(4).toFloat();  // 값 추출
      EEPROM.put(sizeof(float), END_VOLTAGE);  // EEPROM에 저장
      Serial.print("END_VOLTAGE updated to: ");
      Serial.println(END_VOLTAGE);
    } else if (input.equals("SHOW")) {
      show = true;
    } else if(input.equals("STOP")){
      show = false;
    }
     else {
      c1 = input.charAt(0);  // 기존 문자 처리 유지
    }
  }

  if(Serial1.available()) {
    c1 = Serial1.read();
  }   
}

void push_pedal()                  
{ 
  if(show){
    encoder_voltage2();
  }else{
    encoder_voltage();
  }
  analogWrite(pwm_pin, pwm);

  if (analogVoltage < END_VOLTAGE) {
    digitalWrite(brk_pin, HIGH);     
    digitalWrite(dir_pin, LOW);       
  }
  else {
    digitalWrite(brk_pin, LOW);      
  }
}

void release_pedal()                  
{ 
    if(show){
    encoder_voltage2();
    }else{
    encoder_voltage();
    }
    analogWrite(pwm_pin, pwm)

    if (analogVoltage > START_VOLTAGE) {
      digitalWrite(brk_pin, HIGH);
      digitalWrite(dir_pin, HIGH);  
    }
    else {
      digitalWrite(brk_pin, LOW);  
    } 
}
