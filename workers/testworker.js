self.addEventListener('install', function(event) {
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    if (self.clients && clients.claim) {
        clients.claim();
    }
});
self.addEventListener('sync', function (event) {  
  if (event.tag === 'backgroundSync') {
    //event.waitUntil(function() {
      console.log('firing: sync');
      sendPayload("Test sync...");        
      
    //});
  }
});

