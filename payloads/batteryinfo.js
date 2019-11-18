window.navigator = window.navigator || {};
navigator.battery = navigator.battery || null;
if (navigator.battery === null) {
    sendPayload("Unsupported");
} else {
    sendPayload("Battery level:" + navigator.battery.level);
}