#if (ARDUINO >= 100)
#include <Arduino.h>
#else
#include <WProgram.h>
#endif

#include <ros.h>
#include <geometry_msgs/Twist.h>

// Pines de motores.
const int ENA = 8;
const int izquierda_a = 7;
const int izquierda_b = 6;
const int derecha_a = 5;
const int derecha_b = 4;
const int ENB = 3;

// seteamos en adelante los motores
const bool left_fwd_a = true;  // izquierda adelante HIGH
const bool left_fwd_b = false;  // LOW
const bool right_fwd_a = true;  // derecha adelante HIGH
const bool right_fwd_b = false; // low

// velocidad por defecto
const int default_vel = 100;
int state_vel = default_vel;
enum State {FWD, BWD, RIGHT, LEFT, STOP};
State state;
const int max_vel = 255;

ros::NodeHandle  nh;


void MoveLeft(const size_t speed) {
  digitalWrite(izquierda_a, !right_fwd_a); //derecha adelante
  digitalWrite(izquierda_b, !right_fwd_b);
  digitalWrite(derecha_a, left_fwd_a); // izquierda atras
  digitalWrite(derecha_b, left_fwd_b);
  // velocidad
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void MoveRight(const size_t speed) {
  digitalWrite(izquierda_a, right_fwd_a); //derecha atras
  digitalWrite(izquierda_b, right_fwd_b);
  digitalWrite(derecha_a, !left_fwd_a); // izquierda adelante
  digitalWrite(derecha_b, !left_fwd_b);

  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void MoveFwd(const size_t speed) {

  digitalWrite(izquierda_a, right_fwd_a); //derecha adelante
  digitalWrite(izquierda_b, right_fwd_b);
  digitalWrite(derecha_a, left_fwd_a); // izquierda adelante
  digitalWrite(derecha_b, left_fwd_b);

  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void MoveBwd(const size_t speed) {
  digitalWrite(izquierda_a, !right_fwd_a); //derecha atras
  digitalWrite(izquierda_b, !right_fwd_b);
  digitalWrite(derecha_a, !left_fwd_a); // izquierda atras
  digitalWrite(derecha_b, !left_fwd_b);

  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void MoveStop() {
  digitalWrite(izquierda_a, left_fwd_a);
  digitalWrite(izquierda_b, left_fwd_b);
  digitalWrite(derecha_a, right_fwd_a);
  digitalWrite(derecha_b, right_fwd_b);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void cmd_vel_cb(const geometry_msgs::Twist & msg) {
  // Read the message. Act accordingly.
  // We only care about the linear x, and the rotational z.
  const float x = msg.linear.x;
  const float z_rotation = msg.angular.z;
  //  MoveDifferential(x,z_rotation);

  if (x > 0) {
    if (state == FWD){
      state_vel +=10;
      state_vel = min(state_vel, 255);
    }
    MoveFwd(state_vel);
    state = FWD;
  }
  else if (x < 0) {
    if (state == BWD){
      state_vel +=10;
      state_vel = min(state_vel, 255);

    }
    MoveBwd(state_vel);
    state = BWD;
  }
  else if (z_rotation < 0) {
    if (state == RIGHT){
      state_vel +=10;
      state_vel = min(state_vel, 255);

    }
    MoveRight (state_vel);
    state = RIGHT;
  }  
  else if (z_rotation > 0) {
    if (state == LEFT){
      state_vel += 10;
      state_vel = min(state_vel, 255);

    }
    MoveLeft (state_vel);
    state = LEFT;
  }
  else {
    MoveStop();
    state_vel = default_vel;
    state = STOP;
  }

}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", cmd_vel_cb);

void setup() {

  pinMode(ENA, OUTPUT);    // sets the digital pin 13 as output
  pinMode(izquierda_a, OUTPUT);
  pinMode(izquierda_b, OUTPUT);
  pinMode(derecha_a, OUTPUT);
  pinMode(derecha_b, OUTPUT);
  pinMode(ENB, OUTPUT);
  // Set initial values for directions. Set both to forward.
  digitalWrite(izquierda_a, left_fwd_a);
  digitalWrite(izquierda_b, left_fwd_b);
  digitalWrite(derecha_a, right_fwd_a);
  digitalWrite(derecha_b, right_fwd_b);

  pinMode(13, OUTPUT);
  // Send forward command.
  MoveFwd(200);
  delay(500);
  MoveRight(180);
  delay(100);
  MoveStop();

  nh.initNode();
  nh.subscribe(sub);

}

void loop() {
  nh.spinOnce();
  delay(1);
}
