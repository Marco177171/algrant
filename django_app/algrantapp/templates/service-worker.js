self.addEventListener('push', function(event) {
    // The data that you send from your server (payload)
    const payload = event.data ? event.data.text() : 'No payload';

    // Customize notification options
    const options = {
        body: payload,
        icon: '../icons/PulsarBlackBorder.png',  // You can set an icon for the notification
        badge: '../icons/PulsarBlackBorder.png', // Optional badge image
    };

    // Show notification
    event.waitUntil(
        self.registration.showNotification('Algrant: new message', options)
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