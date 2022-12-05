/*
  Created by Fabrizio Di Vittorio (fdivitto2013@gmail.com) - <http://www.fabgl.com>
  Copyright (c) 2019 Fabrizio Di Vittorio.
  All rights reserved.

  This file is part of FabGL Library.

  FabGL is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  FabGL is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with FabGL.  If not, see <http://www.gnu.org/licenses/>.
 */


#pragma once



/**
 * @file
 *
 * @brief This file contains fabgl::KeyboardClass definition and the Keyboard instance.
 */


#include "freertos/FreeRTOS.h"

#include "fabglconf.h"
#include "ps2device.h"
#include "fabui.h"


namespace fabgl {


// ASCII control characters
#define ASCII_NUL  0x00   // Null
#define ASCII_SOH  0x01   // Start of Heading
#define ASCII_STX  0x02   // Start of Text
#define ASCII_ETX  0x03   // End Of Text
#define ASCII_EOT  0x04   // End Of Transmission
#define ASCII_ENQ  0x05   // Enquiry
#define ASCII_ACK  0x06   // Acknowledge
#define ASCII_BELL 0x07   // Bell
#define ASCII_BS   0x08   // Backspace
#define ASCII_HT   0x09   // Horizontal Tab
#define ASCII_LF   0x0A   // Line Feed
#define ASCII_VT   0x0B   // Vertical Tab
#define ASCII_FF   0x0C   // Form Feed
#define ASCII_CR   0x0D   // Carriage Return
#define ASCII_SO   0x0E   // Shift Out
#define ASCII_SI   0x0F   // Shift In
#define ASCII_DLE  0x10   // Data Link Escape
#define ASCII_DC1  0x11   // Device Control 1
#define ASCII_XON  0x11   // Transmission On
#define ASCII_DC2  0x12   // Device Control 2
#define ASCII_DC3  0x13   // Device Control 3
#define ASCII_XOFF 0x13   // Transmission Off
#define ASCII_DC4  0x14   // Device Control 4
#define ASCII_NAK  0x15   // Negative Acknowledge
#define ASCII_SYN  0x16   // Synchronous Idle
#define ASCII_ETB  0x17   // End-of-Transmission-Block
#define ASCII_CAN  0x18   // Cancel
#define ASCII_EM   0x19   // End of Medium
#define ASCII_SUB  0x1A   // Substitute
#define ASCII_ESC  0x1B   // Escape
#define ASCII_FS   0x1C   // File Separator
#define ASCII_GS   0x1D   // Group Separator
#define ASCII_RS   0x1E   // Record Separator
#define ASCII_US   0x1F   // Unit Separator
#define ASCII_SPC  0x20   // Space
#define ASCII_DEL  0x7F   // Delete





/**
 * @brief Associates scancode to virtualkey.
 */
struct VirtualKeyDef {
  uint8_t      scancode;    /**< Raw scancode received from the Keyboard device */
  VirtualKey   virtualKey;  /**< Real virtualkey (non shifted) associated to the scancode */
};


/**
 * @brief Associates a virtualkey and various shift states (ctrl, alt, etc..) to another virtualkey.
 */
struct AltVirtualKeyDef {
  VirtualKey reqVirtualKey; /**< Source virtualkey translated using VirtualKeyDef. */
  struct {
    uint8_t ctrl     : 1;   /**< CTRL needs to be down. */
    uint8_t alt      : 1;   /**< ALT needs to be down. */
    uint8_t shift    : 1;   /**< SHIFT needs to be down (OR-ed with capslock). */
    uint8_t capslock : 1;   /**< CAPSLOCK needs to be down (OR-ed with shift). */
    uint8_t numlock  : 1;   /**< NUMLOCK needs to be down. */
  };
  VirtualKey virtualKey;  /**< Generated virtualkey. */
};


/** @brief All in one structure to fully represent a keyboard layout */
struct KeyboardLayout {
  const char *             name;                /**< Layout name. */
  KeyboardLayout const *   inherited;           /**< Inherited layout. Useful to avoid to repeat the same scancode-virtualkeys associations. */
  VirtualKeyDef            scancodeToVK[92];    /**< Direct one-byte-scancode->virtualkey associations. */
  VirtualKeyDef            exScancodeToVK[32];  /**< Direct extended-scancode->virtualkey associations. Extended scancodes begin with 0xE0. */
  AltVirtualKeyDef         alternateVK[64];     /**< Virtualkeys generated by other virtualkeys and shift combinations. */
};


/** @brief Predefined US layout. Often used as inherited layout for other layouts. */
extern const KeyboardLayout USLayout;

/** @brief UK keyboard layout */
extern const KeyboardLayout UKLayout;

/** @brief German keyboard layout */
extern const KeyboardLayout GermanLayout;

/** @brief Italian keyboard layout */
extern const KeyboardLayout ItalianLayout;


/**
 * @brief The PS2 Keyboard controller class.
 *
 * KeyboardClass connects to one port of the PS2 Controller class (fabgl::PS2ControllerClass) and provides the logic
 * that converts scancodes to virtual keys or ASCII (and ANSI) codes.<br>
 * It optionally creates a task that waits for scan codes from the PS2 device and puts virtual keys in a queue.<br>
 * The PS2 controller uses ULP coprocessor and RTC slow memory to communicate with the PS2 device.<br>
 * <br>
 * It is possible to specify an international keyboard layout. The default is US-layout.<br>
 * There are three predefined kayboard layouts: US (USA), UK (United Kingdom), DE (German) and IT (Italian). Other layout can be added
 * inheriting from US or from any other layout.
 *
 * Applications do not need to create an instance of KeyboardClass because an instance named Keyboard is created automatically.
 *
 * Example:
 *
 *     // Setup pins GPIO33 for CLK and GPIO32 for DATA
 *     Keyboard.begin(GPIO_NUM_33, GPIO_NUM_32);  // clk, dat
 *
 *     // Prints name of received virtual keys
 *     while (true)
 *       Serial.printf("VirtualKey = %s\n", Keyboard.virtualKeyToString(Keyboard.getNextVirtualKey()));
 *
 */
class KeyboardClass : public PS2DeviceClass {

public:

  KeyboardClass();

  /**
   * @brief Initialize KeyboardClass specifying CLOCK and DATA GPIOs.
   *
   * A reset command (KeyboardClass.reset() method) is automatically sent to the keyboard.<br>
   * This method also initializes the PS2ControllerClass to use port 0 only.
   *
   * @param clkGPIO The GPIO number of Clock line
   * @param dataGPIO The GPIO number of Data line
   * @param generateVirtualKeys If true creates a task which consumes scancodes to produce virtual keys,
   *                            so you can call KeyboardClass.isVKDown().
   * @param createVKQueue If true creates a task which consunes scancodes and produces virtual keys
   *                      and put them in a queue, so you can call KeyboardClass.isVKDown(), KeyboardClass.virtualKeyAvailable()
   *                      and KeyboardClass.getNextVirtualKey().
   *
   * Example:
   *
   *     // Setup pins GPIO33 for CLK and GPIO32 for DATA
   *     Keyboard.begin(GPIO_NUM_33, GPIO_NUM_32);  // clk, dat
   */
  void begin(gpio_num_t clkGPIO, gpio_num_t dataGPIO, bool generateVirtualKeys = true, bool createVKQueue = true);

  /**
   * @brief Initialize KeyboardClass without initializing the PS/2 controller.
   *
   * A reset command (KeyboardClass.reset() method) is automatically sent to the keyboard.<br>
   * This method does not initialize the PS2ControllerClass.
   *
   * @param generateVirtualKeys If true creates a task which consumes scancodes and produces virtual keys,
   *                            so you can call KeyboardClass.isVKDown().
   * @param createVKQueue If true creates a task which consunes scancodes to produce virtual keys
   *                      and put them in a queue, so you can call KeyboardClass.isVKDown(), KeyboardClass.virtualKeyAvailable()
   *                      and KeyboardClass.getNextVirtualKey().
   * @param PS2Port The PS/2 port to use (0 or 1).
   *
   * Example:
   *
   *     // Setup pins GPIO33 for CLK and GPIO32 for DATA on port 0
   *     PS2Controller.begin(GPIO_NUM_33, GPIO_NUM_32); // clk, dat
   *     Keyboard.begin(true, true, 0); // port 0
   */
  void begin(bool generateVirtualKeys, bool createVKQueue, int PS2Port);

  // to use this generateVirtualKeys must be true in begin()
  void setUIApp(uiApp * app) { m_uiApp = app; }

  /**
   * @brief Send a Reset command to the keyboard.
   *
   * @return True if the keyboard is correctly initialized.
   */
  bool reset();

  /**
   * @brief Check if keyboard has been detected and correctly initialized.
   *
   * isKeyboardAvailable() returns a valid value only after KeyboardClass.begin() or KeyboardClass.reset() has been called.
   *
   * @return True if the keyboard is correctly initialized.
   */
  bool isKeyboardAvailable() { return m_keyboardAvailable; }

  /**
   * @brief Set keyboard layout.
   *
   * It is possible to specify an international keyboard layout. The default is US-layout.<br>
   * There are three predefined kayboard layouts: US (USA), UK (United Kingdom), DE (German) and IT (Italian). Other layout can be added
   * inheriting from US or from any other layout.
   *
   * @param layout A pointer to the layout structure.
   *
   * Example:
   *
   *     // Set German layout
   *     setLayout(&fabgl::GermanLayout);
   */
  void setLayout(KeyboardLayout const * layout);

  /**
   * @brief Get current keyboard layout.
   *
   * @return The default or last set keyboard layout.
   */
  KeyboardLayout const * getLayout() { return m_layout; }

  /**
   * @brief Get the virtual keys status.
   *
   * This method allows to know the status of each virtual key (Down or Up).<br>
   * Virtual keys are generated from scancodes only if generateVirtualKeys parameter of KeyboardClass.begin() method is true (default).
   *
   * @param virtualKey The Virtual Key to test.
   *
   * @return True if the specified virtual key is down.
   */
  bool isVKDown(VirtualKey virtualKey);

  /**
   * @brief Get the number of virtual keys available in the queue.
   *
   * Virtual keys are generated from scancodes only if generateVirtualKeys parameter is true (default)
   * and createVKQueue parameter is true (default) of KeyboardClass.begin() method.
   *
   * @return The number of virtual keys available to read.
   */
  int virtualKeyAvailable();

  /**
   * @brief Get a virtual key from the queue.
   *
   * Virtual keys are generated from scancodes only if generateVirtualKeys parameter is true (default)
   * and createVKQueue parameter is true (default) of KeyboardClass.begin() method.
   *
   * @param keyDown A pointer to boolean variable which will contain if the virtual key is depressed (true) or released (false).
   * @param timeOutMS Timeout in milliseconds. -1 means no timeout (infinite time).
   *
   * @return The first virtual key of the queue (VK_NONE if no data is available in the timeout period).
   */
  VirtualKey getNextVirtualKey(bool * keyDown = NULL, int timeOutMS = -1);

  /**
   * @brief Convert virtual key to ASCII.
   *
   * This method converts the specified virtual key to ASCII, if possible.<br>
   * For example VK_A is converted to 'A' (ASCII 0x41), CTRL  + VK_SPACE produces ASCII NUL (0x00), CTRL + letter produces
   * ASCII control codes from SOH (0x01) to SUB (0x1A), CTRL + VK_BACKSLASH produces ASCII FS (0x1C), CTRL + VK_QUESTION produces
   * ASCII US (0x1F), CTRL + VK_LEFTBRACKET produces ASCII ESC (0x1B), CTRL + VK_RIGHTBRACKET produces ASCII GS (0x1D),
   * CTRL + VK_TILDE produces ASCII RS (0x1E) and VK_SCROLLLOCK produces XON or XOFF.
   *
   * @param virtualKey The virtual key to convert.
   *
   * @return The ASCII code of virtual key or -1 if virtual key cannot be translated to ASCII.
   */
  int virtualKeyToASCII(VirtualKey virtualKey);

  /**
   * @brief Get the number of scancodes available in the queue.
   *
   * Scancodes are always generated but they can be consumed by the scancode-to-virtualkeys task. So, in order to use this
   * method KeyboardClass.begin() method should be called with generateVirtualKeys = false and createVKQueue = false.<br>
   * Alternatively it is also possible to suspend the conversion task calling KeyboardClass.suspendVirtualKeyGeneration() method.
   *
   * @return The number of scancodes available to read.
   */
  int scancodeAvailable();

  /**
   * @brief Get a scancode from the queue.
   *
   * Scancodes are always generated but they can be consumed by the scancode-to-virtualkeys task. So, in order to use this
   * method KeyboardClass.begin() method should be called with generateVirtualKeys = false and createVKQueue = false.<br>
   * Alternatively it is also possible to suspend the conversion task calling KeyboardClass.suspendVirtualKeyGeneration() method.
   *
   * @param timeOutMS Timeout in milliseconds. -1 means no timeout (infinite time).
   * @param requestResendOnTimeOut If true and timeout has expired then asks the keyboard to resend the scancode.
   *
   * @return The first scancode of the queue (-1 if no data is available in the timeout period).
   */
  int getNextScancode(int timeOutMS = -1, bool requestResendOnTimeOut = false);

  /**
   * @brief Suspend or resume the virtual key generation task.
   *
   * Use this method to temporarily suspend the scancode to virtual key conversion task. This is useful when
   * scancode are necessary for a limited time.
   *
   * @param value If true conversion task is suspended. If false conversion task is resumed.
   */
  void suspendVirtualKeyGeneration(bool value);

  /**
   * @brief Set keyboard LEDs status.
   *
   * Use this method to switch-on or off the NUMLOCK, CAPSLOCK and SCROLLLOCK LEDs.
   *
   * @param numLock When true the NUMLOCK LED is switched on.
   * @param capsLock When true the CAPSLOCK LED is switched on.
   * @param scrollLock When true the SCROLLLOCK LED is switched on.
   *
   * @return True if command has been successfully delivered to the keyboard.
   */
  bool setLEDs(bool numLock, bool capsLock, bool scrollLock) { return send_cmdLEDs(numLock, capsLock, scrollLock); }

  /**
   * @brief Get keyboard LEDs status.
   *
   * Use this method to know the current status of NUMLOCK, CAPSLOCK and SCROLLLOCK LEDs.
   *
   * @param numLock When true the NUMLOCK LED is switched on.
   * @param capsLock When true the CAPSLOCK LED is switched on.
   * @param scrollLock When true the SCROLLLOCK LED is switched on.
   */
  void getLEDs(bool * numLock, bool * capsLock, bool * scrollLock);

  /**
   * @brief Set typematic rate and delay.
   *
   * If the key is kept pressed down, after repeatDelayMS keyboard starts periodically sending codes with frequency repeatRateMS.
   *
   * @param repeatRateMS Repeat rate in milliseconds (in range 33 ms ... 500 ms).
   * @param repeatDelayMS Repeat delay in milliseconds (in range 250 ms ... 1000 ms, steps of 250 ms).
   *
   * @return True if command has been successfully delivered to the keyboard.
   */
  bool setTypematicRateAndDelay(int repeatRateMS, int repeatDelayMS) { return send_cmdTypematicRateAndDelay(repeatRateMS, repeatDelayMS); }

#if FABGLIB_HAS_VirtualKeyO_STRING
  static char const * virtualKeyToString(VirtualKey virtualKey);
#endif

private:

  VirtualKey scancodeToVK(uint8_t scancode, bool isExtended, KeyboardLayout const * layout = NULL);
  VirtualKey VKtoAlternateVK(VirtualKey in_vk, KeyboardLayout const * layout = NULL);
  void updateLEDs();
  VirtualKey blockingGetVirtualKey(bool * keyDown);
  static void SCodeToVKConverterTask(void * pvParameters);


  bool                      m_keyboardAvailable;  // self test passed and support for scancode set 2

  // these are valid after a call to generateVirtualKeys(true)
  TaskHandle_t              m_SCodeToVKConverterTask; // Task that converts scancodes to virtual key and populates m_virtualKeyQueue
  QueueHandle_t             m_virtualKeyQueue;

  uint8_t                   m_VKMap[(int)(VK_LAST + 7) / 8];

  KeyboardLayout const *    m_layout;

  uiApp *                   m_uiApp;

  bool                      m_CTRL;
  bool                      m_ALT;
  bool                      m_SHIFT;
  bool                      m_CAPSLOCK;
  bool                      m_NUMLOCK;
  bool                      m_SCROLLLOCK;

  // store status of the three LEDs
  bool                      m_numLockLED;
  bool                      m_capsLockLED;
  bool                      m_scrollLockLED;
};





} // end of namespace



extern fabgl::KeyboardClass Keyboard;






