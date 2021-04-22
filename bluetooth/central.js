var noble = require('noble');
var allowed_devices = require('./../bt_devices.json');

const OUR_SERVICE_UUID = '7a4bbfe6-999f-4717-b63a-066e06971f59';
const LAMP_UUID = '38CA7A14-1A49-A2F1-EA69-E81D076B2457';
const LAMP_SERVICE = '0001a7d3d8a44fea81741736e808c066';
// const LAMP_SERVICE = '0001a7d3-d8a4-4fea-8174-1736e808c066';

var LampiOnOffCharacteristic = null;

// List of allowed devices
const devices = allowed_devices.devices;

noble.on('discover', function (peripheral) {
  if (devices.indexOf(peripheral.address.toUpperCase()) < 0) return;

  noble.stopScanning();

  peripheral.connect(function (err) {
    console.log('connected!');

    // peripheral.discoverAllServicesAndCharacteristics(function (error, services, characteristics) {
    //   services.forEach(function (service) {
    //     console.log('found service:', service.uuid);
    //   });

    //   characteristics.forEach(function (characteristic) {
    //     console.log('found characteristic:', characteristic.uuid);
    //   });
    // });

    peripheral.discoverServices([LAMP_SERVICE], function (err, services) {
      console.log(services)

      services.forEach(function (service) {
        console.log('found service:', service.uuid);

        service.discoverCharacteristics([], function (err, characteristics) {
          characteristics.forEach(function (characteristic) {
            console.log('found characteristic:', characteristic.uuid);

            if (characteristic.uuid === '0004a7d3d8a44fea81741736e808c066') {
              console.log("works");
              LampiOnOffCharacteristic = characteristic;
              togglePower();
            }
          }); // characterisics
        }); // discover characteristics

      }); //services
    }); // discover services
  }); // connect
});

noble.on('stateChange', function (state) {
  if (state != "poweredOn") {
    noble.stopScanning();
    return;
  }

  console.log("Starting scan...");
  noble.startScanning([], true);
});

noble.on('scanStart', function () {
  console.log("Scanning started.");
});

noble.on('scanStop', function () {
  console.log("Scanning stopped.");
});

function togglePower() {
  var power = new Buffer(1);
  power.writeUInt8(0x1, 0);

  LampiOnOffCharacteristic.write(power, false, function(err) {
    if (!err) {
      console.log("works");
    } else {
      console.log("error");
    }
  })
}