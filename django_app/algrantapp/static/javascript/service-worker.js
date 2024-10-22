self.addEventListener('push', function(event) {
    console.log('in SERVICE WORKER');
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: data.icon,
    };
    console.log('OPTIONS: ' + options);
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    // Define a URL to open when the notification is clicked
    const targetUrl = '/messages';  // Adjust based on your app's structure
    event.notification.close(); // Close the notification

    // Focus on the existing window if it's already open, or open a new one
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
            for (var i = 0; i < clientList.length; i++) {
                var client = clientList[i];
                if (client.url === targetUrl && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});