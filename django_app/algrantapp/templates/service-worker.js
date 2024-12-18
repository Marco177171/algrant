let cacheName = 'Algrant_0.2'

const cachedAssets = [
	// javascript
	'/static/javascript/main.js',
	'/static/javascript/messenger.js',
	'/static/webmanifest/algrant.webmanifest',
    // css
	'/static/css/CarbonDesignSystem.css',
    // pics anf fonts
	'/static/icons/PulsarBlackBorder.png',
	'/static/fonts/ChakraPetch/ChakraPetch-Light.ttf',
	'/static/fonts/Urbanist/Urbanist-Light.ttf',
];

self.addEventListener('install', (event) => {
	event.waitUntil(
		caches.open(cacheName)
		.then(cache => {
			console.log('Service worker: caching files...');
			cache.addAll(cachedAssets);
		})
		.catch(err => console.error(`Error while caching files: ${err}`))
	)
})

// call activation
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activated');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    console.log(`Cycling caches. Cache: ${cache}`);
                    if (cache !== cacheName) {
                        console.log('Service Worker: Clearing old cache');
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim(); // Immediately take control of all pages
});

// // call fetch
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
