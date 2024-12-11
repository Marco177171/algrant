self.addEventListener('push', function(event) {
	console.log('Push event received:', event);
	try {
		const data = event.data.json();
		console.log('Push data:', data);
		const options = {
			body: data.body,
			icon: data.icon,
		};
		event.waitUntil(
			self.registration.showNotification(data.title, options)
		);
	} catch (error) {
		console.error('Error in push event:', error);
	}
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

self.addEventListener('install', function(event) {
	console.log('Service Worker installing.');
	// Perform install steps
});

self.addEventListener('activate', function(event) {
	console.log('Service Worker activating.');
	// Perform activate steps
});

self.addEventListener('fetch', function(event) {
	console.log('Fetching:', event.request.url);
	// Perform fetch steps
});