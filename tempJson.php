<?php
require __DIR__ . '/vendor/autoload.php';
$serial = new PhpSerial();
//this is the port where my Arduino is. Check from the Arduino IDE to see yours!
$serial->deviceSet("COM3");
$serial->confBaudRate(9600);
$serial->confParity("none");
$serial->confCharacterLength(8);
//$serial->confStopBits(1);
$serial->confFlowControl("none");
$serial->deviceOpen();

echo "Now sending msg\n";
//$serial->sendMessage("msg\n");
$read = $serial->readPort();
sleep(1);
echo "DONE\n" + $read;