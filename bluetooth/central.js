var noble = require('noble');
var allowed_devices = require('./../bt_devices.json');

// List of allowed devices
const devices = allowed_devices.devices;
// last advertising data received
var lastAdvertising = {
};

function onDeviceChanged(addr, data) {
  console.log("Device ",addr,"changed data",JSON.stringify(data));
}

function onDiscovery(peripheral) {
  // do we know this device?
  if (devices.indexOf(peripheral.address.toUpperCase())<0) return;

  console.log("Connected!");
//   // does it have manufacturer data with Espruino/Puck.js's UUID
//   if (!peripheral.advertisement.manufacturerData ||
//       peripheral.advertisement.manufacturerData[0]!=0x90 ||
//       peripheral.advertisement.manufacturerData[1]!=0x05) return;
//   // get just our data
//   var data = peripheral.advertisement.manufacturerData.slice(2);
//   // check for changed services
//   if (lastAdvertising[peripheral.address] != data.toString())
//     onDeviceChanged(peripheral.address, data);
//   lastAdvertising[peripheral.address] = data;
}

noble.on('stateChange',  function(state) {
  if (state!="poweredOn") return;
  console.log("Starting scan...");
  noble.startScanning([], true);
});
noble.on('discover', onDiscovery);
noble.on('scanStart', function() { console.log("Scanning started."); });
noble.on('scanStop', function() { console.log("Scanning stopped.");});