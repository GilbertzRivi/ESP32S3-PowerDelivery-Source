# Accessories

Everything on the board that isn't USB PD itself.
Most of it started as "it would be nice to see what's going on" and then got out of hand :P

## Display

- 4" ILI9488 (480x320, SPI) with an XPT2046 touch panel.
- Pages:
  - **Charge:** VBUS, current, power, contract, cable, device name, battery state, session time and energy.
  - **Telemetry:** converter voltage, target, DAC, current limit, total energy, temperature.
  - **Events:** PD and power events with time.
  - **Settings:** fan mode, touch calibration, WiFi.
- Touch calibration and settings are kept in flash, so they survive a reset.

<img src="../images/45w_samsung.jpg" alt="Charge page: Samsung on PPS 10 V, 4.35 A, 43.5 W" width="600">

*The Charge page with the Samsung on PPS 10 V / 4.35 A and a 5 A e-marked cable.*

## Web page

`http://ladowarka.local` on the local network ("ladowarka" is Polish for "charger").

- **Status:** the same values as the display, the PD contract, Current Limit state, temperature and
  fan, total energy, and a live list of PD messages (RX/TX, SOP, type, MessageID, first data
  object).
- **Log:** the text log, with Save. Also the raw defmt log, with Save.
- **System:** firmware version and OTA slot, uptime, last reset reason, heap and stack use of both
  cores, watchdog gaps, INA219 bad reads, faults, ADC calibration with a chart.

## WiFi setup

- With no saved network the board opens its own WiFi called "Ladowarka", with a setup page at `http://192.168.4.1/`.
- To forget the network, tap the WIFI tile on the display twice within 5 s.
- The clock is set from NTP.

## Logs

- defmt log over TCP: `nc ladowarka.local 19021 | defmt-print -e <elf>`
- Every PD message gets logged as `PD rx/tx SOP <name> id <n> <first object>`, and every Hard Reset
  of mine comes with a reason. This saved me more times than I can count.

## OTA updates

- `./ota.sh ladowarka.local` builds, signs and sends the firmware over WiFi.
- `./ota.sh keygen` makes a new Ed25519 key pair.
  The public key is built into the firmware, so flash once over USB after you change it.
  Make your own pair, keys don't go into the repository.
- The board checks an Ed25519 signature over the version and the SHA-256 of the image, and refuses
  an older version than the one installed.
- The update is refused while a sink is attached.
  Updating a charger that's charging something sounded like a bad idea.

## Safety

- Hardware watchdog (TIMG1, 3 s). It only gets fed while both the PD core and the display/WiFi side are alive.
  A reset drops GPIO15, which opens the VBUS switch, so a hung firmware can't leave 20 V on the port.
- Power supervisor: overvoltage, undervoltage, overload, VBUS with the switch open, temperature.
  Repeated faults latch the output off until the BOOT button is pressed.

## Fan and energy

- Fan on PWM, automatic from the converter temperature, or always on.
- Energy counter for the session and in total.
  The total gets saved to flash after a detach, not while charging, to save the flash.
