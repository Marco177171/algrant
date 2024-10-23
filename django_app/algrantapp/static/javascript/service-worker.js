self.addEventListener('push', function(event) {
    if (event && event.data) {
        console.log('Push event received:', event.data.text());
    } else {
        console.log('No data in the push event.');
    }
    console.log('in SERVICE WORKER');
    const data = event.data.json();
    const options = {
        title: body.title,
        body: data.body,
        icon: data.icon,
    };
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    // Define a URL to open when the notification is clicked
    const targetUrl = '/my_conversations';  // Adjust based on your app's structure
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