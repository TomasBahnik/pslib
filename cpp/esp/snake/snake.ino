/******************************************************************* 
*  ESP32 Snake - Version 1.0 - August the 4th 12th, 2019           * 
*                                                                  *
*  ESP32 Snake is a "Snake" clone for VGA monitors, written        *
*  by Roberto Melzi, and based on the FabGL VGA Library,           * 
*  written by Fabrizio Di Vittorio                                 * 
*  For more datails see here:                                      *
*                                                                  * 
*  http://www.fabglib.org/                                         * 
*                                                                  * 
*  See also my other projects on Instructables:                    *
*                                                                  * 
*  http://www.instructables.com/member/Rob%20Cai/instructables/    *
*                                                                  * 
*******************************************************************/ 

#include "fabgl.h" 
#include <canvas.h>

//-------------------- ESP32 pin definition for VGA port -----------------------------
const int redPins[] = {2, 4, 26, 13, 34};
const int greenPins[] = {15, 16, 17, 18, 19};
const int bluePins[] = {21, 22, 23, 27};
/*
const int redPins[] = {2};
const int greenPins[] = {15};
const int bluePins[] = {21};
*/
const int hsyncPin = 17; //32;
const int vsyncPin = 4;  //33;
//------------------------------------------------------------------------------------

//-------------------- button pin definitions -----------------------
byte button_1 = 12; //right - direction 1
byte button_2 = 25; //up    - direction 2
byte button_3 = 14; //left  - direction 3
byte button_4 = 35; //down  - direction 4
//-------------------------------------------------------------------

char str0[] PROGMEM="0"; 
char str1[] PROGMEM="1"; 
char str2[] PROGMEM="2"; 
char str3[] PROGMEM="3"; 
char str4[] PROGMEM="4"; 
char str5[] PROGMEM="5"; 
char str6[] PROGMEM="6"; 
char str7[] PROGMEM="7"; 
char str8[] PROGMEM="8"; 
char str9[] PROGMEM="9"; 
char str10[] PROGMEM="10"; 
char str20[] PROGMEM="ESP32 VGA Snake"; 
char str21[] PROGMEM="by Roberto Melzi"; 
char str22[] PROGMEM="Game Over"; 
char str23[] PROGMEM="Score"; 
char str24[] PROGMEM="Level"; 

boolean button1 = 0;
boolean button2 = 0;
boolean button3 = 0;
boolean button4 = 0;
boolean button; 
byte counterMenu = 0;
byte counterMenu2 = 0; 
byte state = 1;
byte score = 0; 
byte level = 1; 
byte scoreMax = 12; 
int foodX; 
int foodY;
int snakeMaxLength = 199; 
int sx[200];     // > slength + scoreMax*delta + 1 = 40
int sy[200];
int slength = 9; // snake starting length 
int slengthIni = 9; // snake starting length 
int delta = 9;   // snake length increment 
//int wleft = 100; 
int i;
int x; 
int y; 
byte direct = 3; 
int speedDelay = 32; 
int VGAX_WIDTH = 320; 
int VGAX_HEIGHT = 200; 
byte colA, colB, colC; 
int x0Area = 100; 
int y0Area = 20; 
int x1Area = 300; 
int y1Area = 180; 
float cornerStep = 50.; 

//int cancellami; 

void setup() {
  // 8 colors
  VGAController.begin(GPIO_NUM_2, GPIO_NUM_15, GPIO_NUM_21, GPIO_NUM_17, GPIO_NUM_4);
  //VGAController.setResolution(VGA_640x350_70HzAlt1, 640, 350);
  VGAController.setResolution(VGA_320x200_75Hz);
  randomSeed(analogRead(34)); 
  pinMode(button_1,INPUT);
  pinMode(button_2,INPUT);
  pinMode(button_3,INPUT);
  pinMode(button_4,INPUT);
  foodIni(); 
}

void foodIni() {
  do{
     foodX = random(x1Area - x0Area - 4) + x0Area + 2;  
     foodY = random(y1Area - y0Area - 4) + y0Area + 2;  
     // ------------ choose the following for food up to the border ----------------------------------------- 
     //foodX = random(x1Area - x0Area - 2) + x0Area + 1;  
     //foodY = random(y1Area - y0Area - 2) + y0Area + 1; 
  } while ( myGetPixel(foodX, foodY) > 1 ); 
}

void processInputs() {
  button1 = digitalRead(button_1); 
  button2 = digitalRead(button_2);
  button3 = digitalRead(button_3); 
  button4 = digitalRead(button_4);
  button = button1 | button2 | button3 | button4; 
}

void drawMenu() {
  counterMenu2++; 
  delay(10); 
  if (counterMenu2 > 50){
    counterMenu++; 
    smoothRect(60, 60, 210, 60, 20, (counterMenu%5) + 1); 
    vgaPrint(str20, 100, 70, (counterMenu%5) + 2);
    vgaPrint(str21, 100, 92, (counterMenu%5) + 3);
    counterMenu2 = 0; 
  }
}

void drawBorder() {
    myColor(4); 
    Canvas.drawRectangle(x0Area - 1, y0Area - 1, x1Area + 1, y1Area + 1);
}

void drawScore() {
  myColor(2); 
  vgaPrint(str23, 35, 20, 2);
  myColor(5); 
  vgaPrint(str24, 35, 60, 5);
  myColor(0); 
  Canvas.setBrushColor(0, 0, 0);
  Canvas.fillRectangle(20, 40, 70, 52);
  Canvas.setBrushColor(0, 0, 0);
  Canvas.fillRectangle(20, 80, 70, 92);
  vgaPrintNumber(score%10, 55, 40, 4);
  vgaPrintNumber(level%10, 55, 80, 4);
  if (score > 9) {
     vgaPrintNumber(1, 45, 40, 4);
  }
  if (level > 9) {
     vgaPrintNumber(1, 45, 80, 4);
  }
}

// this is for the beginning game window ---------------------------------------------------------------------------------------
void drawStartScreen() {
   Canvas.clear();
   drawBorder(); 
   drawSnakeIni(); 
   drawScore(); 
   button = 0;
   delay(200);
} 

void drawSnakeIni() {
   for (byte i = 0; i < slength ; i++) {
      sx[i] = x0Area + 100 + i;
      sy[i] = y0Area + 70; 
      putBigPixel(sx[i], sy[i], 2);
   }
   //direct = 1; 
   for (byte i = slength; i < snakeMaxLength ; i++) {
     sx[i] = 1;
     sy[i] = 1; 
  }
   //putpixel(foodX, foodY, 1);
   putBigPixel(foodX, foodY, 1);
}

// re-inizialize new match -----------------------------------------------------------------------
void newMatch(){
  score = 0;
  slength = slengthIni; 
  i = slength - 1;  
  for (int i = slength; i < snakeMaxLength; i++){
     sx[i] = 0;
     sy[i] = 0; 
  }
  Canvas.clear();  
  drawBorder();
  drawScore(); 
  //putpixel(foodX, foodY, 1);
  putBigPixel(foodX, foodY, 1);
}

//------------------------------------------------------------------------------------------------------------------------------------------
//----------------------------- This is the main loop of the game --------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------------------------------------------
void loop() {
  
  processInputs(); 
  
  if(state == 1) { //-------------------- start screen --------------------------------------------- 
     drawMenu();
     delay(10);
     processInputs(); 
     if (button == 1){ 
        button = 0;
        Canvas.clear();
        drawStartScreen(); 
        state = 2; 
     }
  }
  
 if(state == 2){ //--------------------- snake waiting for start ------------------------------------------------ 
     if(score == scoreMax || score == 0){
        processInputs(); 
     }
     if (button == 1){ 
        score = 0;
        drawScore(); 
        button = 0;
        button1 = 0;
        button2 = 0;
        button3 = 0;
        button4 = 0;
        direct = 3; 
        x = -1;
        y = 0; 
        i = slength - 1; 
        state = 3; 
     }
  }
  
  if(state == 3) { 
     processInputs(); 
     //-------------------- change direction --------------------------------------------
     if (direct == 1){
        if (button2 == 1){ x = 0; y = -1; direct = 2; button4 = 0;}
        if (button4 == 1){ x = 0; y = +1; direct = 4;}
     }
     else {
        if (direct == 2){
           if (button1 == 1){ x = +1; y = 0; direct = 1; button3 = 0;}
           if (button3 == 1){ x = -1; y = 0; direct = 3;}
        }
        else {
           if (direct == 3){
              if (button2 == 1){ x = 0; y = -1; direct = 2; button4 = 0;}
              if (button4 == 1){ x = 0; y = +1; direct = 4;}
           }
           else { 
              if (direct == 4){
                 if (button1 == 1){ x = +1; y = 0; direct = 1; button3 = 0;}
                 if (button3 == 1){ x = -1; y = 0; direct = 3;}
              }
           }
        }
     }

//----------------------- delete tail --------------------------------------     
     putBigPixel(sx[i], sy[i], 0);
     if (i>0) {
        putBigPixel(sx[i - 1], sy[i - 1], 2); 
     }
     else {
        putBigPixel(sx[slength - 1], sy[slength - 1], 2);
     }
     if ( i == slength - 1){
        sx[i] = sx[0] + x; 
        sy[i] = sy[0] + y; 
     }
     else {
        sx[i] = sx[i + 1] + x; 
        sy[i] = sy[i + 1] + y; 
     }

/*
//--------------------- out from border ------------------------------------    
     if(sx[i] < x0Area + 1) {sx[i] = x1Area - 1;}
     if(sx[i] > x1Area - 1) {sx[i] = x0Area + 1;}
     if(sy[i] < y0Area + 1) {sy[i] = y1Area - 1;}
     if(sy[i] > y1Area - 1) {sy[i] = y0Area + 1;}
*/
   
//--------------------- out from border ------------------------------------    
     if(sx[i] < x0Area + 1) {gameOver();}
     if(sx[i] > x1Area - 1) {gameOver();}
     if(sy[i] < y0Area + 1) {gameOver();}
     if(sy[i] > y1Area - 1) {gameOver();}
     
//--------------------- check eating food -------------------------------------------------------------------------------------------------------------------------
     if ( sx[i] > foodX - 3 && sx[i] < foodX + 3 && sy[i] > foodY - 3 && sy[i] < foodY + 3 ){ 
        putBigPixel(foodX, foodY, 0);
        //putBigPixel(sx[i], sy[i], 2); 
        toneSafe(660,30);  
        foodIni(); 
        drawBorder(); 
        putBigPixel(foodX, foodY, 1);
        if ( sx[i] == foodX || sy[i] == foodY ){ 
           slength = slength + 2*delta; 
           score += 2; 
        }
        else { 
           slength = slength + delta; 
           score++; 
        }
        if (score > scoreMax) {
           speedDelay = int(speedDelay*0.8);
           level += 1; 
           toneSafe(880,30);  
           newMatch();
           drawSnakeIni(); 
           state = 2; 
        }
        drawScore(); 
     }
     putBigPixel(foodX, foodY, 1); 

//----------------------- increase head and Game Over -------------------------------------
     //if (myGetPixel(sx[i], sy[i]) == 2) { 
     if (checkHit(sx[i], sy[i]) == 0) { 
        putBigPixel(sx[i], sy[i], 2); 
     }
     else //-------- Sneke hit himself ----------------------------------------------------
     {
        gameOver(); 
        //putBigPixel(40, 40 + cancellami, 6); 
        //cancellami += 4; 
     }
     putBigPixel(1, 1, 0);
     
     i--;
     if ( i < 0){i = slength - 1;}
     delay(speedDelay); 
  }
} 
//------------------------------------------------------------------------------------------------------------------------------------------
//----------------------------- end of the main loop of the game ---------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------------------------------------------

void toneSafe(int freq, int duration) {
   //vga.tone(freq);  
   delay(duration); 
   //vga.noTone(); 
}

void vgaPrint(char* str, int x, int y, byte color){
   myPrint(str, x, y, color);
}

void vgaPrintNumber(int number, int x, int y, byte color){
   char scoreChar[2];
   sprintf(scoreChar,"%d",number);
   myPrint(scoreChar, x, y, color);
}

void draw_line(int x0, int y0, int x1, int y1, byte color){
   myColor(color); 
   Canvas.drawLine(x0, y0, x1, y1); 
}

void putpixel(int x0, int y0,byte color){
   myColor(color); 
   Canvas.setPixel(x0, y0); 
}

void putBigPixel(int x0, int y0,byte color){
   myColor(color); 
   //Canvas.setPixel(x0, y0); 
   Canvas.setBrushColor(colA, colB, colC);
   Canvas.fillRectangle(x0 - 1, y0 - 1, x0 + 1, y0 + 1);
   Canvas.setBrushColor(0, 0, 0);
}

void myColor(int color){
   if (color == 0){colA = 0; colB = 0; colC = 0;}
   if (color == 1){colA = 1; colB = 0; colC = 0;}
   if (color == 2){colA = 0; colB = 1; colC = 0;}
   if (color == 3){colA = 0; colB = 0; colC = 1;}
   if (color == 4){colA = 1; colB = 1; colC = 0;}
   if (color == 5){colA = 1; colB = 0; colC = 1;}
   if (color == 6){colA = 0; colB = 1; colC = 1;}
   if (color == 7){colA = 1; colB = 1; colC = 1;}
   Canvas.setPenColor(colA, colB, colC);
}

void myPrint(char* str, byte x, byte y, byte color){ 
   Canvas.selectFont(Canvas.getPresetFontInfo(40, 14));
   myColor(color); 
   Canvas.drawText(x, y, str);
}

void gameOver(){
   smoothRect(16, 118, 78, 20, 6, 6); 
   vgaPrint(str22, 20, 121, 6);
   delay(300);
   toneSafe(660, 200); 
   toneSafe(330, 200);
   toneSafe(165, 200); 
   toneSafe(82, 200);
   button == 0; 
   while(button == 0){processInputs();}
   speedDelay = 32; 
   level = 1; 
   newMatch();
   drawSnakeIni();
   state = 2; 
}

void smoothRect(int x0, int y0, int w, int h, int r, int color){  //----- 1.6 comes from the rsolution ratio - 320/200 -------------- 
   myColor(color); 
   draw_line(x0 + 1.6*r, y0 - 1, x0 + w - 1.6*r, y0 - 1, color); 
   draw_line(x0 + 1.6*r, y0 + h, x0 + w - 1.6*r, y0 + h, color); 
   draw_line(x0 - 1, y0 + r, x0 - 1, y0 + h - r, color); 
   draw_line(x0 + w, y0 + r, x0 + w, y0 + h - r, color); 
   for (int i = 0; i <= cornerStep; i++) {
      Canvas.setPixel(x0 + w - r*1.6*(1 - cos(i/cornerStep*3.1415/2.)), y0 + r*(1 - sin(i/cornerStep*3.1415/2.))); 
      Canvas.setPixel(x0 + r*1.6*(1 - cos(i/cornerStep*3.1415/2.)), y0 + r*(1 - sin(i/cornerStep*3.1415/2.))); 
      Canvas.setPixel(x0 + w - r*1.6*(1 - cos(i/cornerStep*3.1415/2.)), y0 + h - r*(1 - sin(i/cornerStep*3.1415/2.))); 
      Canvas.setPixel(x0 + r*1.6*(1 - cos(i/cornerStep*3.1415/2.)), y0 + h - r*(1 - sin(i/cornerStep*3.1415/2.))); 
   }
}

int checkHit(int x, int y){ //--------------------- check if snake hit himself ----------------------------------------------- 
   if (direct == 1){
      if (myGetPixel(x + 1, y) == 2 || myGetPixel(x + 1, y - 1) == 2 || myGetPixel(x + 1, y + 1) == 2) { return 1; }; 
   }
   if (direct == 2){
      if (myGetPixel(x + 1, y - 1) == 2 || myGetPixel(x , y - 1) == 2 || myGetPixel(x - 1, y - 1) == 2) { return 1; }; 
   }
   if (direct == 3){
      if (myGetPixel(x - 1, y) == 2 || myGetPixel(x - 1, y - 1) == 2 || myGetPixel(x - 1, y + 1) == 2) { return 1; }; 
   }
   if (direct == 4){
      if (myGetPixel(x + 1, y + 1) == 2 || myGetPixel(x , y + 1) == 2 || myGetPixel(x - 1, y + 1) == 2) { return 1; }; 
   }
   return 0;
}

int myGetPixel(int x, int y){  
  int red = Canvas.getPixel(x, y).R;
  int green = Canvas.getPixel(x, y).G;
  int blue = Canvas.getPixel(x, y).B;
  if(red == 0 && green == 0 && blue == 0) {return 0;} 
  if(red == 1 && green == 0 && blue == 0) {return 1;} 
  if(red == 0 && green == 1 && blue == 0) {return 2;} 
  if(red == 0 && green == 0 && blue == 1) {return 3;} 
  if(red == 1 && green == 1 && blue == 0) {return 4;} 
  if(red == 1 && green == 0 && blue == 1) {return 5;} 
  if(red == 0 && green == 1 && blue == 1) {return 6;} 
  if(red == 1 && green == 1 && blue == 1) {return 7;} 
}
